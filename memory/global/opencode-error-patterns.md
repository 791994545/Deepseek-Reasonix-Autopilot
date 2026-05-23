---
name: opencode-error-patterns
description: 已知错误模式库 — Flask/Python/CJK/交互问题及修复
type: reference
scope: global
created: 2026-05-23
priority: medium
---
# 已知错误模式库

> **Reasonix 适配**: 此规则源自 OpenCode，已在 Reasonix 平台生效。工具名已映射（Read→read_file, Bash→run_command 等），行为规则保持不变。

## Flask/Server 类
1. ConnectionResetError when testing Flask via http.client — Fix: Set debug=False when running bg
2. Start-Job python process silently exits — Fix: Use Start-Process -NoNewWindow instead of Start-Job
3. Flask watchdog restart kills connection — Fix: app.run(debug=False)

## Python/编码类
4. str.isalnum() returns True for CJK characters — Fix: Check CJK range BEFORE isalnum()
5. sqlite3.ProgrammingError: thread sharing violation — Fix: check_same_thread=False on connect()

## 交互类
6. User correction: did not load matching skill at session start — Fix: scan available_skills and auto-load

## 规则
- 每条模式有 confidence (0.0~1.0): 初始0.5, 成功+0.1, 用户纠正同模式2次则-0.3
- 低于 0.2 自动归档
- 遇到新错误 → 记录: `[ErrorPattern] {command}→{error}→{fix}`
- 用户纠正 → 记录: `[Correction] {context}→{what user said}→{what to do}`
