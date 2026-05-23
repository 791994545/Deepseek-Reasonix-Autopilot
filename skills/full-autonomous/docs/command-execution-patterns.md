# 命令执行模式 — 避免挂起卡死

## 问题

全自动流程中执行命令（如启动 Python 服务器、运行构建脚本）可能挂起，导致 bash 工具等待超时阻塞整个流程。

## 根因

Python (Uvicorn/FastAPI)、Node.js、npm dev server 等进程启动后持续向 **stdout/stderr** 输出日志。如果不用 `-RedirectStandardOutput` 把输出重定向到文件，这些日志会直接喷到 bash 工具的控制台。bash 工具看到输出流一直活跃，就认为命令还没结束，于是一直等待不返回。

## 禁止模式（看门狗会自动检测）

以下写法会导致 bash 工具**挂起**，MANDATORY 脚本 Phase 3 STEP 3.4 明确禁止：

```powershell
# 🔴 禁止：Start-Process 无输出重定向
Start-Process -FilePath "python" -ArgumentList "main.py" -NoNewWindow -PassThru

# 🔴 禁止：裸启动服务器命令（无 Start-Process 包装）
python main.py
uvicorn main:app --reload
node server.js
npm start
npm run dev

# 🔴 禁止：Start-Process 启动了会持续输出的进程但无重定向
Start-Process -FilePath "node" -ArgumentList "server.js" -NoNewWindow -PassThru
```

## 正确模式

```powershell
# 🟢 正确：有输出重定向的 Start-Process（不会挂起）
Start-Process -FilePath "python" -ArgumentList "main.py" -NoNewWindow -PassThru `
    -RedirectStandardOutput "backend.log" -RedirectStandardError "backend.err"

# 🟢 正确：使用 run-with-timeout.ps1（自动处理重定向和超时）
& "scripts\run-with-timeout.ps1" -Command "python main.py" -Mode Condition -ReadyPort 8000 -TimeoutSeconds 60
```

`run-with-timeout.ps1` 内部会自动添加 `-RedirectStandardOutput` 和 `-RedirectStandardError`，确保控制台不会被日志污染。

## 解决方案：三种安全模式

### 1. Capture 模式（默认）—— 短命令

命令应在几秒内执行完毕并退出。工具自动等待完成或超时终止。

```powershell
# 使用超时执行器（推荐）
& "scripts\run-with-timeout.ps1" -Command "node build.js" -TimeoutSeconds 30

# 直接 bash 工具（设置 timeout 参数）
# 注意：bash 工具有默认 120s 超时
```

| 适用场景 | 示例 |
|---------|------|
| 编译/构建 | `npm run build` |
| 短脚本 | `python -c "print(1+1)"` |
| 文件操作 | `Copy-Item src dist -Recurse` |

---

### 2. Process 模式 —— 长进程，需等其退出

进程启动后会在后台一直运行（如 dev server）。工具会超时后自动 Kill。

```powershell
& "scripts\run-with-timeout.ps1" -Command "python main.py" -Mode Process -TimeoutSeconds 30 -LogFile server.log -ErrorFile server.err
```

| 适用场景 | 示例 |
|---------|------|
| CLI 工具 | `python main.py` |
| 批处理 | `ffmpeg -i input.mp4 output.mp4` |
| 一次性服务器 | 运行完毕后退出 |

---

### 3. Condition 模式 —— 后台服务，等就绪信号

启动进程后不等待退出，而是等待**就绪条件**（日志关键字/端口监听）。条件满足后进程继续运行，工具返回。

```powershell
# 等日志中包含 "Server started" 或端口 8080 就绪
& "scripts\run-with-timeout.ps1" -Command "npm start" -Mode Condition -ReadyPattern "Server started" -TimeoutSeconds 60 -LogFile server.log

# 等端口就绪
& "scripts\run-with-timeout.ps1" -Command "python -m http.server 8080" -Mode Condition -ReadyPort 8080 -TimeoutSeconds 30
```

| 适用场景 | 示例 |
|---------|------|
| Web 服务器 | `npm start` → 等端口 3000 |
| API 服务 | `uvicorn main:app` → 等 "Uvicorn running" |
| 数据库 | `mongod` → 等端口 27017 |

---

## 选择指南

```
命令是否快速退出（< 5s）？
  ├── 是 → Capture 模式（默认）
  └── 否 → 是否需要它一直在后台运行？
        ├── 是 → Condition 模式（等就绪后不管）
        │       需要 Kill 时：Stop-Process -Id $PID -Force
        └── 否 → Process 模式（等退出或超时后 Kill）
```

## 后台进程管理

Condition 模式启动的进程在后台持续运行。在后续步骤中需要管理它：

```powershell
# 查找进程（假设已知端口）
$proc = netstat -ano | Select-String ":8080" | ForEach-Object { $_ -split '\s+' | Select-Object -Last 1 } | Get-Unique

# Kill 进程
Stop-Process -Id $proc -Force -ErrorAction SilentlyContinue

# 或通过已知 PID
# 上一步输出了 "进程 PID: 1234 (后台运行中)"
Stop-Process -Id 1234 -Force -ErrorAction SilentlyContinue
```

## 内置 bash 工具的 timeout 参数

直接使用 bash 工具时，可传 `timeout` 参数：

```
工具调用：
  bash(command="python main.py", timeout=30000)  ← 30秒超时
```

但 Condition 模式**无法通过 bash 工具实现**（因为需要主动监听条件），必须用上述脚本。

---

## 快速参考

| 场景 | 推荐写法 |
|------|---------|
| 快速命令 | 直接 bash 工具 + timeout 参数 |
| 有超时保护的短命令 | `run-with-timeout.ps1 -Command "..." -TimeoutSeconds 30` |
| 后台服务器 | `run-with-timeout.ps1 -Command "..." -Mode Condition -ReadyPort 8080` |
| 有日志等待的后台进程 | `run-with-timeout.ps1 -Command "..." -Mode Condition -ReadyPattern "ready"` |
| 一定要退出的长进程 | `run-with-timeout.ps1 -Command "..." -Mode Process -TimeoutSeconds 60` |
