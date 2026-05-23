---
name: diagnose
description: Rigorous debugging loop — reproduce, minimize, hypothesize, instrument, fix, regression test. Use when debugging errors, crashes, or unexpected behavior.
allowed-tools: read_file,write_file,run_command,search_content,search_files
---

<MANDATORY_EXECUTION_SCRIPT>
你必须严格按照以下步骤执行，每完成一步输出 [√] 并附简要结果。
禁止跳过、合并、改变顺序。未输出 [√] 的步骤视为未执行。

## Gate 1: 重现 + 最小化
STEP 1.1: 输出 `[Diagnose] === Diagnose 启动 ===` → [√]
STEP 1.2: 创建可靠的复现步骤 → [√] 复现: {步骤简述}
STEP 1.3: 剥离非本质因素，隔离根因范围 → [√] 最小化: 根因范围缩小至 {模块/行号}
=== Gate 1 PASSED（重现+最小化完成）===

## Gate 2: 假设 + 仪器化
STEP 2.1: 形成具体假设（"原因是 X，因为 Y"）→ [√] 假设: {X} 因为 {Y}
STEP 2.2: 添加日志/print/测试来验证假设 → [√] 仪器: {添加内容}
STEP 2.3: 运行仪器化代码验证假设 → [√] {假设成立/假设不成立}
         → 不成立则返回 STEP 2.1 换假设
=== Gate 2 PASSED（假设已验证）===

## Gate 3: 修复
STEP 3.1: 确认根因后，应用最小修复 → [√] 修复: {改动简述}
STEP 3.2: 验证修复后 bug 不再重现 → [√] {复现通过/复现失败}
         → 失败则返回 STEP 3.1
=== Gate 3 PASSED（修复完成）===

## Gate 4: 回归 + 记录
STEP 4.1: 运行完整测试集，确认没有行为变化 → [√] {N passed / M failed}
STEP 4.2: 若有测试失败 → 修复 → 回到 STEP 4.1
STEP 4.3: 记录学到的东西到 error_patterns.json（根因+修复+confidence）→ [√]
STEP 4.4: 输出汇总 `[Diagnose] 🏁 根因: {X} | 修复: {Y} | 学习已记录` → [√]
=== Gate 4 PASSED（诊断完成）===
</MANDATORY_EXECUTION_SCRIPT>

---

## 五层强制保障

| 层 | 机制 | 位置 |
|----|------|------|
| 1 | 剧本化指令 — MANDATORY 脚本，不可跳过 | 本文件顶部 |
| 2 | 合规看门狗 | `run_skill("compliance-guard")` + `opencode-core-rules` 全局记忆 |
| 3 | 周期性自检 — Gate 4 强制回归验证 | 本文件 Gate 4 |
| 4 | 最小化上下文 — 本文件仅保留执行必须信息 | 详细设计移至 `details.md` |
| 5 | 违例自学习 — 根因+修复自动记录 | `opencode-error-patterns` 全局记忆 |

---

## 硬门禁清单

### Gate 1 出口
- [ ] 复现步骤已建立
- [ ] 根因范围已最小化
- [✓] 本门禁所有项已勾选

全部满足后输出：`=== Gate 1 PASSED ===`

### Gate 2 出口
- [ ] 假设已形成
- [ ] 仪器化已添加
- [ ] 假设已验证: {成立/不成立}
- [✓] 本门禁所有项已勾选

全部满足后输出：`=== Gate 2 PASSED ===`

### Gate 3 出口
- [ ] 最小修复已应用
- [ ] Bug 不再重现
- [✓] 本门禁所有项已勾选

全部满足后输出：`=== Gate 3 PASSED ===`

### Gate 4 出口
- [ ] 回归测试全部通过
- [ ] 学习已记录到 error_patterns.json
- [ ] 汇总已输出
- [✓] 本门禁所有项已勾选

全部满足后输出：`=== Gate 4 PASSED ===`

---

## 输出格式模板

所有外部输出必须使用以下模板。

### 启动
```
[Diagnose] === Diagnose 启动 ===
[Diagnose] 错误: {错误信息}
```

### 重现
```
[Diagnose] 🔬 复现: 执行命令 X → 触发错误 Y
[Diagnose] 📐 最小化: 范围缩小至 function Z 第 42 行
```

### 假设
```
[Diagnose] 💡 假设: 空指针因为未检查返回值
[Diagnose] 🔧 仪器: 添加 console.log 在 Z 函数入口
[Diagnose] ✅ 假设成立 / ❌ 假设不成立 → 换假设
```

### 修复
```
[Diagnose] 🩹 修复: 添加 null check 在 Z 函数第 42 行
[Diagnose] ✅ 复现验证通过
```

### 汇总
```
[Diagnose] 🏁 根因: 未检查返回值导致空指针
[Diagnose] 🏁 修复: 添加 null check | 学习已记录 (conf:0.5)
```

---

## 关键规则

- **不猜修复** — 必须先仪器化验证假设，再修
- **一次只变一个变量** — 不同时改多个东西
- **学到的必须记** — 每次诊断结束都写入 `opencode-error-patterns`

---

See `details.md` for full reference.