---
name: brainstorming
description: "You MUST use this before any creative work - creating features, building components, adding functionality, or modifying behavior. Explores user intent, requirements and design before implementation."
---

<MANDATORY_EXECUTION_SCRIPT>
你必须严格按照以下步骤执行，每完成一步输出 [√] 并附简要结果。
禁止跳过、合并、改变顺序。未输出 [√] 的步骤视为未执行。

## Gate 1: 上下文探索 + 澄清问题
STEP 1.1: 输出 `[Brainstorm] === Brainstorming 启动 ===` → [√]
STEP 1.2: 探索项目上下文（文件/文档/最近提交）→ [√] 上下文: {关键发现}
STEP 1.3: 判断是否涉及视觉问题 → 是则提供 Visual Companion 邀请（单独一条消息，不含其他内容）→ [√]
STEP 1.4: 逐个问澄清问题（一次一个），理解目的/约束/成功标准 → [√] 已澄清 {N} 个问题
=== Gate 1 PASSED（需求理解完成）===

## Gate 2: 方案 + 设计 + 审批
STEP 2.1: 提出 2-3 种方案，含折中和推荐 → [√] 推荐: {方案名}
STEP 2.2: 按模块呈现设计，每模块后等待用户确认 → [√] 设计已展示
STEP 2.3: 用户审批通过？→ 是则继续 / 否则返回 STEP 2.2 → [√] {已通过/待修改}
<HARD-GATE>
🔴 硬闸：在用户审批设计之前，禁止调用任何实现类 skill（frontend-design/mcp-builder/等），禁止写代码，禁止搭建项目。
</HARD-GATE>
=== Gate 2 PASSED（设计已审批）===

## Gate 3: 写 Spec + 自审
STEP 3.1: 将审批通过的设计写入 `docs/superpowers/specs/YYYY-MM-DD-<topic>-design.md` → [√] 已保存
STEP 3.2: 执行 Spec 自审：
         - 占位符检查（TBD/TODO/未完成）→ 修复
         - 内部一致性（前后矛盾）→ 修复
         - 范围检查（是否适合单一计划）→ 修复
         - 歧义检查（是否可多种解读）→ 修复 → [√] 自审通过
STEP 3.3: 提交 spec 到 git（如适用）→ [√]
STEP 3.4: 请用户审阅已保存的 spec → [√] {已批准/需修改}
         → 需修改则返回 STEP 3.1
=== Gate 3 PASSED（Spec 完成）===

## Gate 4: 转交 writing-plans
STEP 4.1: 调用 writing-plans skill 创建实施计划 → [√]
STEP 4.2: 输出汇总 `[Brainstorm] 🏁 设计完成 | 方案: {N} 个 | spec 已保存` → [√]
=== Gate 4 PASSED（Brainstorming 完成）===
</MANDATORY_EXECUTION_SCRIPT>

---

## 五层强制保障

| 层 | 机制 | 位置 |
|----|------|------|
| 1 | 剧本化指令 — MANDATORY 脚本，不可跳过 | 本文件顶部 |
| 2 | Gate 2 `<HARD-GATE>` — 禁止未经审批写代码 | 本文件 Gate 2 |
| 3 | Gate 3 自审 — 强制 spec 质量检查 | 本文件 Gate 3 |
| 4 | 仅保留执行必须信息 | 详细设计参考本文件下方 |
| 5 | 用户审批不通过自动记录 | 依赖 compliance-check |

---

## 硬门禁清单

### Gate 1 出口
- [ ] 项目上下文已探索
- [ ] 澄清问题已完成: {N} 个
- [ ] Visual Companion 已处理（如适用）
- [✓] 本门禁所有项已勾选

全部满足后输出：`=== Gate 1 PASSED ===`

### Gate 2 出口
- [ ] 2-3 种方案已提出
- [ ] 设计已展示并获审批
- [ ] `<HARD-GATE>` 未违规
- [✓] 本门禁所有项已勾选

全部满足后输出：`=== Gate 2 PASSED ===`

### Gate 3 出口
- [ ] Spec 已保存到 {路径}
- [ ] 自审通过（无占位符/矛盾/歧义）
- [ ] 已提交 git（如适用）
- [ ] 用户已批准
- [✓] 本门禁所有项已勾选

全部满足后输出：`=== Gate 3 PASSED ===`

### Gate 4 出口
- [ ] writing-plans 已调用
- [ ] 汇总已输出
- [✓] 本门禁所有项已勾选

全部满足后输出：`=== Gate 4 PASSED ===`

---

## 输出格式模板

### 启动
```
[Brainstorm] === Brainstorming 启动 ===
[Brainstorm] 上下文: 发现 {N} 个相关文件
```

### 澄清
```
[Brainstorm] ❓ 我想先了解一下：{问题}
```

### 方案
```
[Brainstorm] 💡 推荐方案: {方案名} — 因为 {理由}
[Brainstorm] 📋 备选: {方案A}(折中), {方案B}(折中)
```

### 设计审批
```
[Brainstorm] 📐 模块: {名称}
[Brainstorm] ✅ 用户已审批
```

### 自审
```
[Brainstorm] 🔍 自审: 占位符修复 {N} 处 | 矛盾修复 {M} 处 | 歧义修复 {K} 处
[Brainstorm] ✅ 自审通过
```

### 汇总
```
[Brainstorm] 🏁 设计完成 | 方案: 3 个 | spec: docs/specs/xxx.md
```

---

## 关键规则

### HARD-GATE（不可违反）
在用户审批设计之前，**禁止**：
- 调用 frontend-design / mcp-builder / 任何实现类 skill
- 写任何代码
- 搭建项目脚手架
- 唯一可调用的后续 skill：writing-plans

### 原则
- **一次一个问题** — 不一次抛多个
- **选择题优先** — 多选比开放题好答
- **YAGNI** — 删除设计中不必要的功能
- **模块化验证** — 逐模块展示，逐模块审批

---

本文件其余内容保留原有参考。See below for full reference.