<#
.SYNOPSIS
    full-autonomous v2 协议遵循度看门狗（五层强制保障的 Layer 2）
.DESCRIPTION
    独立进程扫描模型输出日志，检测是否遵循 full-autonomous v2 协议。
    检测项: [Auto] 前缀、task() 调用、Phase 门禁、MANDATORY_SCRIPT 步骤、
    心跳间隔、输出格式、违例模式学习。
.PARAMETER LogPath
    要扫描的日志文件路径
.PARAMETER MessageCount
    检查最近多少条消息（默认 10）
.PARAMETER Continuous
    是否持续监控（每 30 秒扫描一次）
#>

param(
    [Parameter(Mandatory = $false)]
    [string]$LogPath = "",

    [Parameter(Mandatory = $false)]
    [int]$MessageCount = 10,

    [Parameter(Mandatory = $false)]
    [switch]$Continuous = $false
)

$violations = @()
$currentPhase = $null
$currentStep = $null
$violationHistory = @()   # 违例历史记录
$heartbeatTimestamps = @() # 心跳时间戳
$errorPatterns = @{}      # 违例模式计数
$autoPrefixCount = 0      # [Auto] 前缀计数

# 配置路径
$errorPatternsPath = "$env:USERPROFILE\.config\opencode\error_patterns.json"
$violationLogPath = "$env:TEMP\opencode\watchdog_violations.json"

function Test-HasAutoPrefix {
    param([string[]]$Messages)
    $lastFew = $Messages[-5..-1] | Where-Object { $_ }
    foreach ($msg in $lastFew) {
        if ($msg -match '^\s*\[Auto\]') { return $true }
    }
    return $false
}

function Test-HasHeartbeatPrefix {
    param([string[]]$Messages)
    $lastFew = $Messages[-5..-1] | Where-Object { $_ }
    foreach ($msg in $lastFew) {
        if ($msg -match '^\s*\[心跳\]') { return $true }
    }
    return $false
}

function Test-HasTaskCall {
    param([string[]]$Messages)
    foreach ($msg in $Messages) {
        if ($msg -match 'task\(') { return $true }
    }
    return $false
}

function Test-PhasePassed {
    param([string[]]$Messages)
    foreach ($msg in $Messages) {
        if ($msg -match '=== Phase \d PASSED ===') { return $true }
    }
    return $false
}

function Test-HasDangerLabel {
    param([string[]]$Messages)
    foreach ($msg in $Messages) {
        if ($msg -match '<danger>') { return $true }
    }
    return $false
}

function Test-DangerousCommand {
    param([string]$msg)
    $dangerPatterns = @(
        'Remove-Item\s+-Recurse',
        'rm\s+-rf',
        'DROP\s+TABLE',
        'git\s+push\s+--force',
        'Invoke-WebRequest.*-Method\s+Delete',
        'Format-Volume',
        'Clear-Host'
    )
    foreach ($pattern in $dangerPatterns) {
        if ($msg -match $pattern) { return $true }
    }
    return $false
}

function Test-HangingCommand {
    <#
    .SYNOPSIS
        检测会导致 bash 工具挂起的命令模式
    #>
    param([string]$msg)

    # 模式1: Start-Process -NoNewWindow 无 -RedirectStandardOutput
    $spNoRedirect = 'Start-Process.*-NoNewWindow(?!.*-RedirectStandardOutput)'
    if ($msg -match $spNoRedirect) {
        return "Start-Process -NoNewWindow 缺少 -RedirectStandardOutput（输出喷到控制台导致 bash 工具挂起）"
    }

    # 模式2: Start-Process -FilePath "python" ... -ArgumentList "main.py" ... -PassThru（无重定向）
    $spPython = 'Start-Process.*python.*main'
    if ($msg -match $spPython -and $msg -notmatch '-RedirectStandardOutput') {
        return "直接 Start-Process python main.py 无输出重定向（Uvicorn/FastAPI 日志会阻塞 bash 工具）"
    }

    # 模式3: 裸启动服务器命令（无 Start-Process 包装）
    $bareServerPatterns = @(
        'python\s+main\.\w+',
        'uvicorn\s+\w+:\w+',
        'node\s+server\.\w+',
        'npm\s+start',
        'npm\s+run\s+dev',
    )
    foreach ($pattern in $bareServerPatterns) {
        if ($msg -match $pattern -and $msg -notmatch 'Start-Process') {
            return "裸启动服务器命令 `"$($Matches[0])`" 未用 Start-Process 包装（会阻塞 bash 工具直到进程退出）"
        }
    }

    # 模式4: Start-Process -FilePath *server* 无重定向
    $spServer = 'Start-Process.*(python|node|npm).*(-ArgumentList|start|dev)'
    if ($msg -match $spServer -and $msg -notmatch '-RedirectStandardOutput') {
        return "Start-Process 启动了可能持续输出的进程但无 -RedirectStandardOutput"
    }

    return $null
}

function Get-CurrentPhase {
    param([string[]]$Messages)
    foreach ($msg in $Messages[-5..-1]) {
        if ($msg -match 'Phase\s+(\d)') { return [int]$Matches[1] }
    }
    return $null
}

function Get-CurrentStep {
    param([string[]]$Messages)
    foreach ($msg in $Messages[-3..-1]) {
        if ($msg -match 'STEP\s+(\d+\.\d+)') { return $Matches[1] }
        if ($msg -match 'STEP\s+(\d+)') { return $Matches[1] }
    }
    return $null
}

function Write-ViolationEvent {
    param([string]$Type, [string]$Detail, [string]$Severity)
    $event = @{
        timestamp = (Get-Date -Format "yyyy-MM-dd HH:mm:ss")
        type = $Type
        detail = $Detail
        severity = $Severity
        phase = $currentPhase
        step = $currentStep
    }
    $violationHistory += $event
    # 更新模式计数
    $key = "$Type|$([math]::Max(0, $currentPhase ?? 0))"
    if ($errorPatterns.ContainsKey($key)) {
        $errorPatterns[$key]++
    } else {
        $errorPatterns[$key] = 1
    }
    # 持久化违例日志
    try {
        $existing = @()
        if (Test-Path $violationLogPath) {
            $existing = Get-Content $violationLogPath -Raw -ErrorAction SilentlyContinue | ConvertFrom-Json
        }
        $existing += $event
        $existing | ConvertTo-Json -Depth 3 | Set-Content $violationLogPath -Force
    } catch {
        # 静默失败，不影响主流程
    }
}

function Test-HeartbeatInterval {
    param([string[]]$Messages)
    $heartbeatLines = $Messages | Where-Object { $_ -match '^\s*\[心跳\]' }
    if ($heartbeatLines.Count -ge 2) {
        return $true  # 有心跳
    }
    return $false
}

# 主检查逻辑
function Invoke-WatchdogCheck {
    param([string[]]$Messages)
    
    $violations = @()
    $alerts = @()

    if ($Messages.Count -eq 0) {
        Write-Host "[看门狗] ⚠️ 无消息可检查"
        return @()
    }

    Write-Host "[看门狗] 开始检查 ($($Messages.Count) 条消息)"

    # 更新当前状态
    $currentPhase = Get-CurrentPhase -Messages $Messages
    $currentStep = Get-CurrentStep -Messages $Messages
    if ($currentPhase) { Write-Host "[看门狗] 当前 Phase: $currentPhase" }
    if ($currentStep) { Write-Host "[看门狗] 当前 STEP: $currentStep" }

    # Layer 1: 格式检查 — [Auto] 前缀
    if (-not (Test-HasAutoPrefix -Messages $Messages)) {
        $violations += "L1:最近5条消息中无 [Auto] 前缀"
        Write-ViolationEvent -Type "missing_auto_prefix" -Detail "最近5条无 [Auto] 前缀" -Severity "L1"
    }

    # Layer 1: 格式检查 — Phase PASSED 标记
    if ($currentPhase -and $currentPhase -gt 0) {
        if (-not (Test-PhasePassed -Messages $Messages)) {
            $violations += "L1:Phase $currentPhase 已开始但无 PASSED 标记"
        }
    }

    # Layer 2: 执行检查 — task() 调用
    if ($currentPhase -eq 3) {
        if (-not (Test-HasTaskCall -Messages $Messages)) {
            $violations += "L2:Phase 3 但未检测到 task() 调用（Level 0 可能未并行派发）"
            Write-ViolationEvent -Type "missing_task_call" -Detail "Phase 3 无 task() 调用" -Severity "L2"
        }
    }

    # Layer 3: 心跳检查
    if ($currentPhase -ge 2 -and $currentPhase -le 4) {
        if (-not (Test-HeartbeatInterval -Messages $Messages)) {
            if ($Messages.Count -ge 10) {
                $violations += "L3:长时间运行但无心跳（可能注意力衰减）"
                Write-ViolationEvent -Type "missing_heartbeat" -Detail "长时间运行无心跳" -Severity "L3"
            }
        }
    }

    # Layer 2: 挂起命令检查 — Start-Process 无重定向 / 裸启动服务器
    $hasPhase3 = ($currentPhase -eq 3) -or ($Messages -match 'Phase 3')
    if ($hasPhase3) {
        foreach ($msg in $Messages) {
            $hangReason = Test-HangingCommand -msg $msg
            if ($hangReason) {
                # 检查它是否已被 scripts/run-with-timeout.ps1 替代
                $surrounding = $Messages[$([Math]::Max(0, $Messages.IndexOf($msg) - 2))..$([Math]::Min($Messages.Count - 1, $Messages.IndexOf($msg) + 2))]
                $hasTimeoutScript = ($surrounding -join ' ') -match 'run-with-timeout'
                if (-not $hasTimeoutScript) {
                    $violations += "L2-挂起:$hangReason"
                    Write-ViolationEvent -Type "hanging_command" -Detail $hangReason -Severity "L2"
                }
            }
        }
    }

    # Layer 2: 危险操作检查
    foreach ($msg in $Messages) {
        if (Test-DangerousCommand -msg $msg) {
            # 检查前2条消息是否有 <danger> 标签
            $idx = $Messages.IndexOf($msg)
            $preceding = $Messages | Select-Object -First ([Math]::Max(0, $idx))
            $lastTwo = $preceding[-2..-1] | Where-Object { $_ }
            $hasDanger = Test-HasDangerLabel -Messages $lastTwo
            if (-not $hasDanger) {
                $violations += "L2:危险命令前无 <danger> 标签! 命令: $($msg.Substring(0, [Math]::Min(100, $msg.Length)))"
                Write-ViolationEvent -Type "missing_danger_label" -Detail "危险命令前无 danger 标签" -Severity "L2"
            }
        }
    }

    # Layer 5: 违例模式分析
    foreach ($key in $errorPatterns.Keys) {
        if ($errorPatterns[$key] -ge 2) {
            $alerts += "⚠️ 历史违例模式: $key 已发生 $($errorPatterns[$key]) 次，建议强化对应指令"
        }
    }

    # 输出结果
    if ($violations.Count -gt 0) {
        Write-Host "[看门狗] ⚠️ 发现 $($violations.Count) 项协议偏离："
        foreach ($v in $violations) {
            Write-Host "  - $v"
        }
    }
    if ($alerts.Count -gt 0) {
        Write-Host "[看门狗] 📊 违例模式预警："
        foreach ($a in $alerts) {
            Write-Host "  $a"
        }
    }
    if ($violations.Count -eq 0 -and $alerts.Count -eq 0) {
        Write-Host "[看门狗] ✅ 协议遵循度检查通过"
    }

    # 更新 error_patterns.json
    if ($violations.Count -gt 0) {
        try {
            $patterns = @{}
            if (Test-Path $errorPatternsPath) {
                $content = Get-Content $errorPatternsPath -Raw -ErrorAction SilentlyContinue
                if ($content) { $patterns = $content | ConvertFrom-Json -ErrorAction SilentlyContinue }
            }
            $key = "ProtocolViolation"
            if (-not $patterns.$key) { $patterns.$key = @() }
            $newEntry = @{
                timestamp = (Get-Date -Format "yyyy-MM-dd HH:mm:ss")
                count = $violations.Count
                details = $violations
            }
            $patterns.$key += $newEntry
            $patterns | ConvertTo-Json -Depth 5 | Set-Content $errorPatternsPath -Force
        } catch {
            # 静默
        }
    }

    return $violations
}

# ---- 主入口 ----

$messages = @()

# 尝试从日志文件读取
if ($LogPath -and (Test-Path $LogPath)) {
    $content = Get-Content -Path $LogPath -Raw -ErrorAction SilentlyContinue
    if ($content) {
        $lines = $content -split "`n"
        $currentMsg = ""
        foreach ($line in $lines) {
            if ($line -match '^\[' -and $currentMsg.Length -gt 0) {
                $messages += $currentMsg.Trim()
                $currentMsg = $line.Trim()
            } elseif ($line -match '^\[') {
                $currentMsg = $line.Trim()
            } else {
                $currentMsg += "`n" + $line
            }
        }
        if ($currentMsg.Trim().Length -gt 0) {
            $messages += $currentMsg.Trim()
        }
    }
}

# 备用: 尝试从临时文件读取
if ($messages.Count -eq 0) {
    $altPath = "$env:TEMP\opencode\watchdog_input.txt"
    if (Test-Path $altPath) {
        $messages = Get-Content -Path $altPath -ErrorAction SilentlyContinue
    }
}

if ($messages.Count -eq 0) {
    Write-Host "[看门狗] ℹ️ 没有日志输入，跳过检查"
    Write-Host "[看门狗] 使用 -LogPath 指定日志文件"
    Write-Host "[看门狗] 或向 $env:TEMP\opencode\watchdog_input.txt 写入日志"
    exit 0
}

# 单次或持续运行
if ($Continuous) {
    Write-Host "[看门狗] 持续监控模式启动 (每30秒检查一次)"
    while ($true) {
        $result = Invoke-WatchdogCheck -Messages $messages
        Start-Sleep -Seconds 30
        # 重新读取日志以获取新消息
        if ($LogPath -and (Test-Path $LogPath)) {
            $messages = Get-Content -Path $LogPath -Raw -ErrorAction SilentlyContinue
        }
    }
} else {
    $result = Invoke-WatchdogCheck -Messages $messages
    if ($result.Count -gt 0) {
        exit 1
    }
    exit 0
}
