---
name: grill-me
description: Relentless questioning of a plan or design until every branch of the decision tree is resolved. Use when the user needs to stress-test an idea before committing, or when requirements are unclear.
---

> **Reasonix 注意**: 此 skill 功能等价于内置 `review` 工具。变更审查直接用 `review()` 更轻量。

<MANDATORY_EXECUTION_SCRIPT>
你必须严格按照以下步骤执行，每完成一步输出 [√] 并附简要结果。
禁止跳过、合并、改变顺序。未输出 [√] 的步骤视为未执行。

## Gate 1: 加载设计 + 识别分支
STEP 1.1: 输出 `[Grill] === Grill Me 启动 ===` → [√]
STEP 1.2: 加载当前设计/计划 → [√] 设计: {描述}
STEP 1.3: 遍历设计决策树，识别所有未解决的分支 → [√] 分支: {N} 个
=== Gate 1 PASSED（设计已理解）===

## Gate 2: 逐个追问
STEP 2.1: 取下一个未解决的分支 → [√] 当前: {分支描述}
STEP 2.2: 提出该分支的核心问题（可附你的推荐答案）→ [√]
STEP 2.3: 一次只问一个问题，等用户回复后再继续 → [√]
STEP 2.4: 若问题可通过代码库回答 → 用 explore 工具查，不问用户 → [√]
STEP 2.5: 挑战每个假设，显性化折中 → [√]
=== Gate 2 PASSED（追问完成）===

## Gate 3: 汇总 + 记录
STEP 3.1: 汇总所有已解决的分支 → [√] `[Grill] 📋 已解决: {N} 个分支`
STEP 3.2: 若有未解决的分支 → 标记为待定 → [√] 待定: {N} 个
STEP 3.3: 输出汇总 `[Grill] 🏁 追问完成 | 已解决 {N} | 待定 {M}` → [√]
=== Gate 3 PASSED（Grill 完成）===
</MANDATORY_EXECUTION_SCRIPT>

---

## 五层强制保障

| 层 | 机制 | 位置 |
|----|------|------|
| 1 | 剧本化指令 — MANDATORY 脚本 | 本文件顶部 |
| 3 | Gate 3 强制汇总 — 确认无遗漏分支 | 本文件 Gate 3 |
| 4 | 最小化上下文 | 参考移至 `details.md` |
| 5 | 待定分支记录 | 待定项传递至下一环节 |

---

## 硬门禁清单

### Gate 1 出口
- [ ] 设计已加载
- [ ] 决策分支已识别: {N} 个
- [✓] 本门禁所有项已勾选

全部满足后输出：`=== Gate 1 PASSED ===`

### Gate 2 出口
- [ ] 所有分支已追问
- [ ] 一次一问
- [✓] 本门禁所有项已勾选

全部满足后输出：`=== Gate 2 PASSED ===`

### Gate 3 出口
- [ ] 汇总已输出
- [ ] 待定分支已标记
- [✓] 本门禁所有项已勾选

全部满足后输出：`=== Gate 3 PASSED ===`

---

## 输出格式模板

### 启动
```
[Grill] === Grill Me 启动 ===
[Grill] 设计: {描述} | 分支: {N} 个
```

### 追问
```
[Grill] ❓ 分支: {描述}
[Grill] 💡 我的推荐: {推荐答案}
```

### 汇总
```
[Grill] 📋 已解决: 5 个分支
[Grill] ⏸ 待定: 1 个 — {原因}
[Grill] 🏁 追问完成 | 已解决 5 | 待定 1
```

---

## 关键规则

- **一次一个问题** — 等回复再继续
- **能查代码的不问** — 优先用 explore 工具
- **挑战假设** — 每个"显而易见"的决策都要深挖
- **永远给出推荐答案** — 让用户说"是/否/换一个"

---

See `details.md` for full documentation.