# Experience: reasonix 深度分析复盘 v2

## 日期
2026-05-24

## 分析结果
对 586 条 usage.jsonl 记录进行分析：
- 27% 的调用 completionTokens < 200（浪费调用）
- 91% 的调用 promptTokens > 100K（严重上下文膨胀）
- skill_performance.json 只有 1 条记录（自学习闭环断了）
- sessions/ 膨胀到 4.05 MB（无自动轮转）

## 改进措施
1. P0: Phase 5 复盘必须写 skill_performance，不写 = 违例
2. P0: 每次 error_pattern 追加时自动联动 skill_performance
3. P1: sessions/*.jsonl > 500KB 自动轮转
4. P2: project-rules.md 模板已自动生成（已实现）
5. P3: completionTokens < 200 且无 tool call 的不记入 usage.jsonl

## 标签
analysis, reasonix, self-improvement, memory-loop