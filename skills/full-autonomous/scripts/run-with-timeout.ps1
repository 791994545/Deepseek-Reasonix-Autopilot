<#
.SYNOPSIS
    通用超时执行器 — 解决命令挂起导致全自动流程卡死的问题
.DESCRIPTION
    以超时保护运行任意命令。支持：
    - Process 模式：启动进程，超时未退出则 Kill
    - Condition 模式：启动进程，等待日志/端口的就绪条件
    - Capture 模式：运行短命令，超时无输出则终止
.PARAMETER Command
    要执行的命令（字符串）
.PARAMETER TimeoutSeconds
    超时秒数（默认 30）
.PARAMETER Mode
    执行模式: Process|Condition|Capture（默认 Capture）
.PARAMETER ReadyPattern
    Condition 模式下监听的日志关键字（正则）
.PARAMETER ReadyPort
    Condition 模式下监听的端口号
.PARAMETER LogFile
    输出日志文件路径
.PARAMETER ErrorFile
    错误日志文件路径
.PARAMETER WorkingDirectory
    工作目录
.EXAMPLE
    # Capture 模式：运行短命令，最多等 10 秒
    .\run-with-timeout.ps1 -Command "python -c 'print(1+1)'" -TimeoutSeconds 10

    # Process 模式：启动服务器，30 秒后强制 Kill
    .\run-with-timeout.ps1 -Command "python main.py" -Mode Process -TimeoutSeconds 30 -LogFile server.log -ErrorFile server.err

    # Condition 模式：启动服务器，等端口 8080 就绪
    .\run-with-timeout.ps1 -Command "python main.py" -Mode Condition -ReadyPort 8080 -TimeoutSeconds 30 -LogFile server.log
#>

param(
    [Parameter(Mandatory = $true)]
    [string]$Command,

    [Parameter(Mandatory = $false)]
    [int]$TimeoutSeconds = 30,

    [Parameter(Mandatory = $false)]
    [ValidateSet("Process", "Condition", "Capture")]
    [string]$Mode = "Capture",

    [Parameter(Mandatory = $false)]
    [string]$ReadyPattern = "",

    [Parameter(Mandatory = $false)]
    [int]$ReadyPort = 0,

    [Parameter(Mandatory = $false)]
    [string]$LogFile = "",

    [Parameter(Mandatory = $false)]
    [string]$ErrorFile = "",

    [Parameter(Mandatory = $false)]
    [string]$WorkingDirectory = ""
)

$startTime = Get-Date
$timedOut = $false
$exitCode = -1
$output = ""

Write-Host "[超时执行器] 启动 | 模式: $Mode | 命令: $($Command.Substring(0, [Math]::Min(80, $Command.Length)))... | 超时: ${TimeoutSeconds}s"

function Write-TimedOutput {
    param([string]$Message)
    $elapsed = [math]::Round(((Get-Date) - $startTime).TotalSeconds, 1)
    Write-Host "[${elapsed}s] $Message"
}

# --- Capture 模式：运行短命令，直接等结果 ---
if ($Mode -eq "Capture") {
    $job = Start-Job -ScriptBlock {
        param($cmd, $wd)
        if ($wd) { Set-Location $wd }
        try {
            $result = Invoke-Expression $cmd 2>&1
            return $result | Out-String
        } catch {
            return "ERROR: $_"
        }
    } -ArgumentList $Command, $WorkingDirectory

    $completed = $job | Wait-Job -Timeout $TimeoutSeconds

    if (-not $completed) {
        $job | Stop-Job -ErrorAction SilentlyContinue
        $job | Remove-Job -ErrorAction SilentlyContinue
        Write-TimedOutput "⚠️ 超时 (${TimeoutSeconds}s)，已终止"
        exit 124  # 标准超时退出码
    }

    $output = $job | Receive-Job -ErrorAction SilentlyContinue
    $exitCode = 0
    $job | Remove-Job -ErrorAction SilentlyContinue
    Write-Host "[超时执行器] ✅ 完成 | 耗时: $([math]::Round(((Get-Date) - $startTime).TotalSeconds, 1))s"
    Write-Host $output
    exit $exitCode
}

# --- Process 模式：启动进程，等它退出或超时 ---
if ($Mode -eq "Process") {
    $psArgs = @{
        FilePath = "powershell"
        ArgumentList = "-NoProfile", "-Command", $Command
        NoNewWindow = $true
        PassThru = $true
    }
    if ($LogFile) { $psArgs.RedirectStandardOutput = $LogFile }
    if ($ErrorFile) { $psArgs.RedirectStandardError = $ErrorFile }
    if ($WorkingDirectory) { $psArgs.WorkingDirectory = $WorkingDirectory }

    try {
        $proc = Start-Process @psArgs
    } catch {
        Write-Host "[超时执行器] ❌ 启动失败: $_"
        exit 1
    }

    $proc.WaitForExit($TimeoutSeconds * 1000) | Out-Null

    if (-not $proc.HasExited) {
        $proc.Kill()
        Write-TimedOutput "⚠️ 超时 (${TimeoutSeconds}s)，已 Kill 进程 (PID: $($proc.Id))"
        exit 124
    }

    $exitCode = $proc.ExitCode
    $elapsed = [math]::Round(((Get-Date) - $startTime).TotalSeconds, 1)

    Write-Host "[超时执行器] ✅ 进程退出 | 退出码: $exitCode | 耗时: ${elapsed}s"

    if ($LogFile -and (Test-Path $LogFile)) {
        Write-Host "[超时执行器] 日志输出 (tail 10):"
        Get-Content $LogFile -Tail 10 | ForEach-Object { Write-Host "  $_" }
    }

    exit $exitCode
}

# --- Condition 模式：启动进程，等待就绪条件 ---
if ($Mode -eq "Condition") {
    $logPath = if ($LogFile) { $LogFile } else { "$env:TEMP\opencode\condition_$(Get-Random).log" }
    $errPath = if ($ErrorFile) { $ErrorFile } else { "$env:TEMP\opencode\condition_$(Get-Random).err" }

    $psArgs = @{
        FilePath = "powershell"
        ArgumentList = "-NoProfile", "-Command", $Command
        NoNewWindow = $true
        PassThru = $true
        RedirectStandardOutput = $logPath
        RedirectStandardError = $errPath
    }
    if ($WorkingDirectory) { $psArgs.WorkingDirectory = $WorkingDirectory }

    try {
        $proc = Start-Process @psArgs
    } catch {
        Write-Host "[超时执行器] ❌ 启动失败: $_"
        exit 1
    }

    $ready = $false
    $elapsed = 0

    while ($elapsed -lt $TimeoutSeconds) {
        if ($proc.HasExited) {
            Write-TimedOutput "进程已退出 (码: $($proc.ExitCode))"
            break
        }

        # 检查日志中的就绪模式
        if ($ReadyPattern -and (Test-Path $logPath)) {
            $logContent = Get-Content $logPath -Raw -ErrorAction SilentlyContinue
            if ($logContent -match $ReadyPattern) {
                Write-TimedOutput "✅ 就绪条件满足 (日志匹配: $ReadyPattern)"
                $ready = $true
                break
            }
        }

        # 检查端口就绪
        if ($ReadyPort -gt 0) {
            $portCheck = netstat -an 2>$null | Select-String "LISTENING" | Select-String ":$($ReadyPort)\s"
            if ($portCheck) {
                Write-TimedOutput "✅ 就绪条件满足 (端口 $ReadyPort 已监听)"
                $ready = $true
                break
            }
        }

        Start-Sleep -Milliseconds 500
        $elapsed = [math]::Round(((Get-Date) - $startTime).TotalSeconds, 1)
    }

    if (-not $ready) {
        if (-not $proc.HasExited) {
            $proc.Kill()
            Write-TimedOutput "⚠️ 超时 (${TimeoutSeconds}s)，进程已 Kill")
        }
        Write-Host "[超时执行器] ❌ 就绪条件未满足"
        if (Test-Path $logPath) {
            Write-Host "[超时执行器] 日志输出 (tail 10):"
            Get-Content $logPath -Tail 10 | ForEach-Object { Write-Host "  $_" }
        }
        exit 124
    }

    Write-Host "[超时执行器] ✅ 条件满足 | 耗时: $elapsed`s"
    if (Test-Path $logPath) {
        Write-Host "[超时执行器] 日志输出 (tail 5):"
        Get-Content $logPath -Tail 5 | ForEach-Object { Write-Host "  $_" }
    }

    # 在 Condition 模式下，进程继续在后台运行
    # 返回 PID 供后续管理
    Write-Host "[超时执行器] 进程 PID: $($proc.Id) (后台运行中)"
    exit 0
}
