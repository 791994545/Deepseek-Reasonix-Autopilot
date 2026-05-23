---
name: tdd
description: Test-Driven Development — RED-GREEN-REFACTOR cycle. Write failing tests first, then implement minimum code, then refactor. Use when building new features or fixing bugs that need test coverage.
allowed-tools: run_command
---

> **Reasonix 注意**: 此 skill 功能等价于内置 `test` skill。运行测试直接用测试命令。此 skill 提供 TDD 三阶段完整流程。

<MANDATORY_EXECUTION_SCRIPT>
你必须严格按照以下步骤执行，每完成一步输出 [√] 并附简要结果。
禁止跳过、合并、改变顺序。未输出 [√] 的步骤视为未执行。

## Gate 1: RED — 写失败测试
STEP 1.1: 输出 `[TDD] === TDD 启动 ===` → [√]
STEP 1.2: 写一个最小测试，验证一个行为 → [√] 测试: {测试名}
STEP 1.3: 确认测试名清晰、只测一件事、使用真实代码（除非不可避免否则不用 mock）→ [√]
=== Gate 1 PASSED（RED 完成）===

## Gate 2: 验证 RED — 确认测试失败
STEP 2.1: 运行该测试 → `npm test path/to/test` → [√]
STEP 2.2: 确认:
         - 测试失败（不是报错）
         - 失败信息符合预期（"feature missing"，不是 typo）
         - 失败原因正确 → [√] 失败正确? [是/否]
STEP 2.3: 如果测试通过了 → 测试的是已有行为 → 回头修测试 → 回到 STEP 1.2
         如果测试报错了 → 修错误 → 回到 STEP 2.1
=== Gate 2 PASSED（验证 RED 完成）===

## Gate 3: GREEN — 写最小代码
STEP 3.1: 写刚好能让测试通过的最小代码 → [√] 代码: {改动简述}
STEP 3.2: 不加功能、不重构、不"顺便改进" → [√]
=== Gate 3 PASSED（GREEN 完成）===

## Gate 4: 验证 GREEN — 确认通过
STEP 4.1: 运行该测试 → `npm test` → [√] {通过/失败}
STEP 4.2: 如果失败 → 修代码（不是修测试）→ 回到 STEP 4.1
STEP 4.3: 确认其他测试也全部通过 → [√]
=== Gate 4 PASSED（验证 GREEN 完成）===

## Gate 5: REFACTOR — 清理
STEP 5.1: 仅在 GREEN 状态下重构 → [√]
STEP 5.2: 去除重复、改善命名、提取辅助函数 → [√]
STEP 5.3: 不添加行为 → [√]
STEP 5.4: 重构后再次运行全部测试 → [√] {全部通过}
=== Gate 5 PASSED（REFACTOR 完成）===

## Gate 6: 自检 + 循环
STEP 6.1: 检查是否还有下一个待实现的行为 → [√] {是/否 → TDD 完成}
STEP 6.2: 若是 → 回到 Gate 1 写下一个测试
STEP 6.3: 若完成 → 输出汇总 `[TDD] 🏁 RED-GREEN-REFACTOR 循环完成 | 测试: {N} 个` → [√]
=== Gate 6 PASSED（TDD 完成）===
</MANDATORY_EXECUTION_SCRIPT>

---

## 五层强制保障

| 层 | 机制 | 位置 |
|----|------|------|
| 1 | 剧本化指令 — MANDATORY 脚本，不可跳过 | 本文件顶部 |
| 2 | 合规看门狗 | `run_skill("compliance-guard")` + `opencode-core-rules` 全局记忆 |
| 3 | 周期性自检 — Gate 6 强制检查 | 本文件 Gate 6 |
| 4 | 最小化上下文 — 执行指令在上，参考在下 | 详细参考见下方 |
| 5 | 违例自学习 — 违规模式记录 | `opencode-error-patterns` 全局记忆 |

---

## 硬门禁清单

### Gate 1 出口
- [ ] 测试已写入: {测试名}
- [ ] 只测一件事: {是}
- [ ] 测试名清晰: {是}
- [✓] 本门禁所有项已勾选

全部满足后输出：`=== Gate 1 PASSED ===`

### Gate 2 出口
- [ ] 测试已运行: {通过/失败}
- [ ] 失败原因正确: {是/否}
- [✓] 本门禁所有项已勾选

全部满足后输出：`=== Gate 2 PASSED ===`

### Gate 3 出口
- [ ] 最小代码已写入
- [ ] 无额外功能
- [✓] 本门禁所有项已勾选

全部满足后输出：`=== Gate 3 PASSED ===`

### Gate 4 出口
- [ ] 测试全部通过
- [ ] 输出无错误/警告
- [✓] 本门禁所有项已勾选

全部满足后输出：`=== Gate 4 PASSED ===`

### Gate 5 出口
- [ ] 重构在 GREEN 状态下完成
- [ ] 无行为变更
- [ ] 全部测试仍通过
- [✓] 本门禁所有项已勾选

全部满足后输出：`=== Gate 5 PASSED ===`

### Gate 6 出口
- [ ] 下一行为已确认: {有/无}
- [ ] 汇总已输出（完成时）
- [✓] 本门禁所有项已勾选

全部满足后输出：`=== Gate 6 PASSED ===`

---

## 输出格式模板

所有外部输出必须使用以下模板。

### 启动
```
[TDD] === TDD 启动 ===
[TDD] 🔴 RED: 写测试 — {测试名}
```

### RED
```
[TDD] 🔴 测试: test('rejects empty email')
[TDD] 🔴 验证: npm test → FAIL (expected 'Email required', got undefined)
[TDD] 🔴 ✅ 失败正确
```

### GREEN
```
[TDD] 🟢 代码: 添加 email 空值检查
[TDD] 🟢 验证: npm test → PASS
[TDD] 🟢 ✅ 全部测试通过
```

### REFACTOR
```
[TDD] 🔵 重构: 提取 validateField 函数
[TDD] 🔵 验证: npm test → PASS
```

### 自检
```
[TDD 自检] Gate 1 ✅ | Gate 2 ✅ | Gate 3 ✅ | Gate 4 ✅ | Gate 5 ✅
[TDD 自检] 还有下一个行为? [是 → 回到 RED | 否 → 完成]
```

### 汇总
```
[TDD] 🏁 RED-GREEN-REFACTOR 循环完成 | 测试: 5 个 | 重构轮次: 2
```

---

## 核心规则（铁律）

```
NO PRODUCTION CODE WITHOUT A FAILING TEST FIRST
```

- 写代码前没有失败测试？删掉。重新 TDD。
- 没看到测试失败过？你不知道它是不是测对了。
- 测试通过立即上线？你没见过它抓 bug 的样子。

### 需要 TDD 的场景
- ✅ 新功能
- ✅ Bug 修复
- ✅ 重构
- ✅ 行为变更

### 例外（问你的搭档）
- ❌ 一次性原型
- ❌ 生成代码
- ❌ 配置文件

---

## 常见借口对照表

| 借口 | 真相 |
|------|------|
| "太简单了不用测" | 简单代码也会坏。30 秒写个测试。 |
| "我测完了再写" | 事后测试立刻通过 = 什么也没证明。 |
| "已经手动测过了" | 临时 ≠ 系统。没记录，没法复跑。 |
| "删掉 N 小时工作是浪费" | 沉没成本。保留 = 技术债。 |
| "TDD 太教条了" | TDD 更快。事后调 bug 更慢。 |
| "先保留当参考" | 你会改它。那是事后测试。删就是删。 |

## 红旗 — 立刻停止并重来

- 先写了代码
- 实现后才写测试
- 测试立刻通过
- 说不清为什么失败
- "仅此一次"的合理化作
- "已经手动测过了"
- "精神到了就行，仪式不重要"

---

See `details.md` if needed for expanded reference (currently self-contained).