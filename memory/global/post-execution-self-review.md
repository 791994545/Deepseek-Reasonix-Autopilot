---
name: post-execution-self-review
description: 每次全自动执行后自我回顾与进化 — Phase 5 统一回顾流程 A→E
type: reference
scope: global
created: 2026-05-24
priority: medium
---
# 自我回顾与进化机制

**适用范围**: 每次 full-autonomous 执行结束后（所有路径 Quick/Standard/Full）

## 流程概述
```
Phase 5 统一回顾
├── 阶段 A: 执行过程回顾 (Standard/Full)
│   ├── 扫描执行记录 → 输出了什么、卡在哪儿
│   ├── 检查违例 → 无理由跳过记 error_patterns
│   └── 对比预期 vs 实际 → 校准复杂度评估
├── 阶段 B: 错误模式分析 (Standard/Full)
│   ├── 扫描本次所有问题 → 列清单
│   ├── 交叉比对 error_patterns.json → 命中提升 / 新增记录
│   └── 更新 routing_weights.json
├── 阶段 C: 经验写入 (所有路径 🔴 必须)
│   ├── 追加 skill_performance.json
│   ├── 写入 memory/experiences/{日期}-{摘要}.md
│   └── 验证写入成功
├── 阶段 D: 进化建议 (Standard/Full)
│   ├── 输出 1-3 条进化建议
│   └── 可泛化的规则 → AGENTS.md / remember
└── 阶段 E: 系统清理 (所有路径)
```

## 关键原则
- Quick 路径至少执行阶段 C+D（保底学习），不可完全跳过
- 新发现的错误模式立即记入 error_patterns.json → 下次命中
- 进化建议可泛化为全局规则 → 写入 AGENTS.md 或全局记忆
