---
name: reasonix-roadmap
description: Reasonix 技术路线图 — 已生效/已规划/未来方向
type: reference
scope: global
created: 2026-05-24
---
# Reasonix 技术路线图

## 已生效
- ✅ 路由权重自调 — error_pattern confidence → routing_weights penalty（0.7/0.8/0.9 阈值）
- ✅ 多策略重试 — Phase 3.5 ralph 最多 3 种策略后标记阻塞
- ✅ 项目规则自检 — Phase 0 检查 project-rules.md，无则生成模板
- ✅ 成本预算检查 — Phase 0 加载 usage.jsonl 计算平均消耗，超阈值则警告
- ✅ 路由表自检 — Phase 1 扫描路由表 vs 实际技能目录，报缺失/未引用

## 已规划
- 📅 记忆整合 — Phase 5C.5：experiences >20 条时 self-improving 合并去重
- 📅 路由表全量验证 — Phase 5C.6 定期校验路由表技能引用完整性

## 未来方向
- 跨会话记忆自动摘要（旧经验合并为 patterns）
- routing_weights 可视化面板
- 技能依赖自动解析（加载技能时检查依赖链）
