---
name: auto-trigger
description: 🔴 每条消息先 Phase 0 → 评估复杂度 → Quick/Std/Full 路径 → 直接执行
type: reference
scope: global
priority: high
---
# 全自动触发规则

> 🔴 **收到任何消息后，第一件事是 Phase 0 评估。**
> Phase 0 = 复杂度(1-10) + 路径选择 + `[Auto] === 启动 ===`。
> 用户说"全自动" → 强制 Full 路径。
>
> 详情见 `skills/full-autonomous/SKILL.md`
