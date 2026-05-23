---
name: writing-plans
description: Use when you have a spec or requirements for a multi-step task, before touching code.
---

<MANDATORY_EXECUTION_SCRIPT>
你必须严格按照以下步骤执行，每完成一步输出 [√] 并附简要结果。
禁止跳过、合并、改变顺序。未输出 [√] 的步骤视为未执行。

## Gate 1: 范围 + 文件结构
STEP 1.1: 输出 `[Plan] === Writing Plans 启动 ===` → [√]
STEP 1.2: 加载 spec/需求 → 审查范围：如果包含多个独立子系统，建议拆分为多个计划 → [√] 范围: {单一/需拆分}
STEP 1.3: 映射文件结构：确认创建/修改的每个文件及职责 → [√] 文件: {N} 个
=== Gate 1 PASSED（结构已确定）===

## Gate 2: 写任务
STEP 2.1: 按依赖顺序写出任务列表 → [√] 任务: {N} 个
STEP 2.2: 每个任务粒度控制在 2-5 分钟（写测试→跑测试→实现→跑测试→提交）→ [√]
STEP 2.3: 每个步骤包含：完整代码、精确文件路径、确切命令及预期输出 → [√]
STEP 2.4: 禁止占位符：无 TBD/TODO/"类似任务N"/"添加错误处理"等 → [√]
=== Gate 2 PASSED（任务已写完）===

## Gate 3: 自审
STEP 3.1: 对照 spec 逐条检查覆盖度 → 每个需求都可指向具体任务 → [√]
STEP 3.2: 扫描占位符违例 → 修复 → [√]
STEP 3.3: 检查类型/签名一致性（前文定义的类型在后文一致使用）→ [√]
STEP 3.4: 保存到 `docs/superpowers/plans/YYYY-MM-DD-<feature-name>.md` → [√]
=== Gate 3 PASSED（自审通过）===

## Gate 4: 交付出行选择
STEP 4.1: 输出 plan 已保存路径 → [√]
STEP 4.2: 提供两种执行方式供用户选择：
         ① Subagent-Driven（推荐）— 每任务一个子代理，任务间审查
         ② Inline Execution — 当前会话批量执行，checkpoint 断点 → [√]
STEP 4.3: 根据选择调用 executing-plans 或触发子代理模式 → [√]
=== Gate 4 PASSED（Plan 完成）===
</MANDATORY_EXECUTION_SCRIPT>

---

## 五层强制保障

| 层 | 机制 | 位置 |
|----|------|------|
| 1 | 剧本化指令 — MANDATORY 脚本 | 本文件顶部 |
| 3 | Gate 3 强制自审 — 覆盖度+占位符+一致性 | 本文件 Gate 3 |
| 4 | 仅保留执行必须信息 | 详细参考见下方 |
| 5 | 缺失覆盖自动标记 | Gate 3 覆盖度检查 |

---

## 硬门禁清单

### Gate 1 出口
- [ ] 范围已确认: {单一/需拆分}
- [ ] 文件结构已映射: {N} 个文件
- [✓] 本门禁所有项已勾选

全部满足后输出：`=== Gate 1 PASSED ===`

### Gate 2 出口
- [ ] 任务已写出: {N} 个
- [ ] 粒度 2-5 分钟
- [ ] 每步含完整代码+路径+命令
- [ ] 无占位符违例
- [✓] 本门禁所有项已勾选

全部满足后输出：`=== Gate 2 PASSED ===`

### Gate 3 出口
- [ ] 覆盖度检查通过
- [ ] 占位符已修复
- [ ] 类型一致性已检查
- [ ] Plan 已保存
- [✓] 本门禁所有项已勾选

全部满足后输出：`=== Gate 3 PASSED ===`

### Gate 4 出口
- [ ] 执行方式已选择: {Subagent/Inline}
- [ ] 对应 skill 已调用
- [✓] 本门禁所有项已勾选

全部满足后输出：`=== Gate 4 PASSED ===`

---

## 输出格式模板

### 启动
```
[Plan] === Writing Plans 启动 ===
[Plan] 范围: {单一/需拆分} | 文件: {N} 个
```

### 任务
```
[Plan] 📋 Task {N}/{M}: {名称}
[Plan] 📁 创建: path/to/file.py
[Plan] 📁 修改: path/to/existing.py:42-56
```

### 自审
```
[Plan] 🔍 覆盖度: 需求 {N} 条 → 任务 {M} 个
[Plan] 🔍 占位符: 修复 {K} 处
[Plan] 🔍 一致性: ✅ 通过
```

### 交付
```
[Plan] 💾 已保存: docs/superpowers/plans/2026-05-21-xxx.md
[Plan] 🏁 Plan 完成 | 任务: {N} 个 | 等待选择执行方式
```

---

## 关键规则

### 粒度标准
每步 = 一次动作（2-5 分钟）：
- 写测试 → 跑测试验证失败 → 实现 → 跑测试验证通过 → 提交

### 禁止绝的占位符
- ❌ "TBD", "TODO", "implement later"
- ❌ "Add appropriate error handling"（没有具体代码）
- ❌ "Write tests for the above"（没有测试代码）
- ❌ "Similar to Task N"（别人可能乱序读）
- ❌ 引用未定义的函数/类型

### 结果
```
每次 task 都是自包含的改动，可独立理解、独立测试。
```

---

## Plan 模板

```markdown
# [功能名] Implementation Plan

**Goal:** [一句话]

**Architecture:** [2-3 句]

**Tech Stack:** [关键技术]

---

### Task N: [组件名]

**Files:**
- Create: `path/to/file.py`
- Modify: `path/to/existing.py:123-145`
- Test: `tests/path/to/test.py`

- [ ] **Step 1: Write the failing test**
  ```python
  def test_specific_behavior():
      ...
  ```

- [ ] **Step 2: Run test to verify it fails**
  Run: `pytest tests/path/test.py -v`
  Expected: FAIL

- [ ] **Step 3: Write minimal implementation**
  ```python
  def function(input):
      return expected
  ```

- [ ] **Step 4: Run test to verify it passes**
  Run: `pytest tests/path/test.py -v`
  Expected: PASS

- [ ] **Step 5: Commit**
```
