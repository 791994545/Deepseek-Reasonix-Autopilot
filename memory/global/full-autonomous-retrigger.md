---
name: full-autonomous-retrigger
description: 全自动模式应对所有任务型消息触发，不限于第一条
type: feedback
scope: global
created: 2026-05-24
priority: high
---
# Phase 5 完成后重新触发的规则

**错误**：我完成了 Phase 0→5 全自动流程后，下一条用户消息如果是新任务（"修复这个"、"帮git"、"按建议改"），我没有重新触发 Phase 0，而是直接回答。

**为什么错**：AGENTS.md 规定的是"收到消息后"判断任务类型，不是"只对第一条消息"。

**修正**：Phase 5 的清理步骤（删 state.json、停 watchdog）之后，我必须回到"等待消息"状态，下一条消息如果是任务型就重新走 Phase 0→5。

**如何判断**：
- 如果用户消息包含任务关键词（做/建/写/改/修/跑/部署/分析/审计/优化/修复/创建/推/提交/git/push 等）→ 新任务，重启 Phase 0
- 如果只是追问/讨论/确认→ 当前任务上下文继续
