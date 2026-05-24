---
type: experience
date: 2026-05-24
task: full-autonomous v2.0 全系统自审
assessment: success
path: Full
lessons: 定期自审找到的 bug 比被动等待多得多
---

# 2026-05-24: full-autonomous v2.0 全系统自审

## 做了什么
用全自动 Full 路径深度审计了 full-autonomous 系统本身。

## 发现问题 & 修复
| 问题 | 修复 |
|------|------|
| 版本号混乱 (v1.0/v2.0/v3.2) | 统一为 v2.0 |
| 路由表 5 个幽灵技能名 | 全部移除/更正 |
| compliance-watchdog.ps1 死代码 | 已删除 |
| routing_weights 3 条幽灵记录 | 已清理 |
| AGENTS.md 引用 2 个不存在的文件 | 已移除 |
| 3 个无用 demo 经验文件 | 已删除 |
| AGENTS.md vs SKILL.md 不一致 | 已同步 |
| 02-gate-checklists.md v3.2 | 已改为 v2.0 |

## 学到了什么
- 定期自审找到的 bug 比被动等待多得多
- 幽灵引用（路由表、权重表）是无用膨胀的主要来源
- 外部 auditor 比系统自查更严格
