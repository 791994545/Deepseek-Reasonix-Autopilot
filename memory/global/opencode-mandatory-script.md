---
name: opencode-mandatory-script
description: 强制启动脚本 — 压缩版 3 步启动 + full-autonomous 桥接
type: reference
scope: global
created: 2026-05-23
priority: high
---
# 强制启动脚本

> 🔴 **任务型消息第一动作：执行 AGENTS.md 中的 Phase 0 流程**
> `submit_plan` 不优先使用（审批门与 Phase gate 重叠），`ask_choice`/`todo_write` 保留
> Phase 0 = `[Auto] === 启动 ===` + 复杂度评估 + 路径选择 + 直接执行。
> 权威 MANDATORY 脚本：`AGENTS.md` 中的 `<MANDATORY_EXECUTION_SCRIPT>`。
> 全自动流程详情：`skills/full-autonomous/SKILL.md`。

**默认开启模式**：full-autonomous 默认加载，不再需要触发词。
- 每次会话自动执行 Phase 0 复杂度评估
- Quick (≤3) → 跳过 Phase 1-2，直接 init→3→complete
- Standard (4-7) → init→1→2a→3→4→complete
- Full (≥8) → init→1→2b→3→4→complete
- `全自动` → 强制 Full
- `直接回答/快速回答` → 强制 Quick

🔴 `submit_plan` 全自动模式下不优先使用，`ask_choice`/`todo_write` 保留

## 全局记忆索引
| 文件名 | 优先级 | 内容 |
|--------|--------|------|
| opencode-tool-reference | 高 | 工具映射表 |
| opencode-core-rules | 高 | 12 条原则 |
| opencode-mandatory-script | 高 | 本文件 |
| opencode-error-patterns | 中 | 错误模式库 |
| opencode-unattended-mode | 中 | 无人值守 |
| opencode-session-mgmt | 中 | 会话管理 |
| opencode-self-evolution | 中 | 自我改进 |
| opencode-subagent-proto | 中 | 子代理协议 |
| opencode-skill-catalog | 低 | 技能清单 |
