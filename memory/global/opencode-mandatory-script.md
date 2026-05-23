---
name: opencode-mandatory-script
description: 强制启动脚本 — 压缩版 3 步启动 + full-autonomous 桥接
type: reference
scope: global
created: 2026-05-23
priority: high
---
# 强制启动脚本

> 🧊 **此文件为索引参考，不定义执行步骤。**
> 权威 MANDATORY 脚本请参见 `AGENTS.md` 中的 `<MANDATORY_EXECUTION_SCRIPT>`。
> 全自动流程详情参见 `skills/full-autonomous/SKILL.md`。

**默认开启模式**：full-autonomous 默认加载，不再需要触发词。
- 每次会话自动执行 Phase 0 复杂度评估（STEP 3）
- Quick (≤3) → 直接执行
- Standard (4-7) → 标准流程
- Full (≥8) → 完整流程
- `全自动` → 强制 Full
- `直接回答/快速回答` → 强制 Quick

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
