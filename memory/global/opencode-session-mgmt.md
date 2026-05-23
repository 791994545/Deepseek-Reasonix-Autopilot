---
name: opencode-session-mgmt
description: 会话管理/冲突消解/健康检查规则
type: reference
scope: global
created: 2026-05-23
priority: medium
---
# 会话管理、冲突消解、健康检查

> **Reasonix 适配**: 此规则源自 OpenCode，已在 Reasonix 平台生效。

## 会话管理
不设人为上限 — 跑满为止，中间做好保存。
- 尽早开启压缩：每步只输出结果，不展开解释
- 每完成 1 个子任务 → 更新 TodoWrite
- 每 3 个子任务 → 写 checkpoint（已完成/进行中/待办）
- 新会话读取 checkpoint → 继续
- 禁止静默丢弃中间结果 / 跨会话不交接

## 冲突消解
| 冲突 | 裁决 |
|------|------|
| 无人值守 vs 追问确认 | 无人值守优先，跳过确认 |
| 无人值守 vs 禁止静默失败 | 失败→分析→换策略重试，不设上限 |
| caveman vs brainstorm | 需追问时暂停压缩 |
| 功能重叠的两个技能 | 选 description 更相关那个 |

## 搜索路径优先级
`~/.reasonix/skills/` > builtin skills > 当前 session
