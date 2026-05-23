---
name: ralph
description: "Use when the user explicitly asks to use Ralph mode for persistent plan-execute-check-retry loops that keep going until the target outcome is achieved."
displayName: Ralph - 不达目标不罢休
emoji: "🔨"
summary: 持续循环执行任务直到目标完成。当用户说"使用Ralph完成XX"时触发，自动规划→执行→检查→重试，不达目标不停止。
aliases:
  - ralph
  - 使用ralph
  - ralph模式
  - 用ralph
  - ralph完成
---

> ⚠️ **此 skill 已标记为 OpenCode 遗产**。Reasonix 中请用 `full-autonomous` v2.1 + `task-executor` 替代持久循环执行。详情见 `full-autonomous/SKILL.md`。

<MANDATORY_EXECUTION_SCRIPT>
你必须严格按照以下步骤执行，每完成一步输出 [√] 并附简要结果。
禁止跳过、合并、改变顺序。未输出 [√] 的步骤视为未执行。

## Gate 1: 目标锁定 + 计划
STEP 1.1: 输出 `[Ralph] === Ralph 模式启动 ===` → [√]
STEP 1.2: 明确定义目标、完成标准（可验证的条件列表）、拆解子步骤 → [√]
         🎯 目标: {一句话}
         ✅ 标准: {条件列表}
         📋 步骤: {拆解清单}
STEP 1.3: 估算总步骤数 N，输出 `[Ralph] 📋 计划: N 步` → [√]
=== Gate 1 PASSED（计划完成）===

## Gate 2: 执行当前步骤
STEP 2.1: 取出当前待执行步骤 → [√] 当前: {步骤名} (尝试 1/{N})
STEP 2.2: 执行 — 调用工具 / 写代码 / 派子代理 → [√]
STEP 2.3: 验证结果 — 检查是否达到该步骤的完成标准 → [√] {通过/失败}
=== Gate 2 PASSED（当前步骤执行完成）===

## Gate 3: 失败处理 + 重试
STEP 3.1: 若 STEP 2.3 通过 → 标记完成，回到 Gate 2 取下一步
STEP 3.2: 若 STEP 2.3 失败 → 分析原因，按顺序切换策略:
         ① 重试（临时问题）
         ② 换参数
         ③ 换方法（完全不同路径）
         ④ 搜方案（web/论坛/GitHub）
         ⑤ 找 skill → [√] 策略切换: 方法 {X}
STEP 3.3: 同一步骤失败 ≥5 次 → escalate: 标记阻塞，继续其他步骤 → [√]
=== Gate 3 PASSED（失败已处理）===

## Gate 4: 收尾 + 自检
STEP 4.1: 所有步骤处理完毕 → 输出完成报告 → [√]
          `🔨 Ralph 完成 | ✅ N 完成 | ❌ M 失败 | ⏱ Xm | 🔄 Y 次重试`
STEP 4.2: 若有步骤始终失败 → 记录到 error_patterns.json → [√]
STEP 4.3: 自检 — 检查是否有跳过未处理的步骤 → [√]
=== Gate 4 PASSED（Ralph 完成）===
</MANDATORY_EXECUTION_SCRIPT>

---

## 五层强制保障

| 层 | 机制 | 位置 |
|----|------|------|
| 1 | 剧本化指令 — MANDATORY 脚本，不可跳过 | 本文件顶部 |
| 2 | 合规看门狗 | `run_skill("compliance-guard")` + `opencode-core-rules` 全局记忆 |
| 3 | 周期性自检 — Gate 4 强制自检 | 本文件 Gate 4 |
| 4 | 最小化上下文 — 本文件仅保留执行必须信息 | 详细设计移至 `details.md` |
| 5 | 违例自学习 — 失败步骤自动记录 | `opencode-error-patterns` 全局记忆 |

---

## 硬门禁清单

### Gate 1 出口
- [ ] 目标已定义: {一句话}
- [ ] 完成标准已列出: {N} 条
- [ ] 子步骤已拆解: {N} 步
- [✓] 本门禁所有项已勾选

全部满足后输出：`=== Gate 1 PASSED ===`

### Gate 2 出口
- [ ] 当前步骤 {名称} 已执行
- [ ] 验证结果: {通过/失败}
- [✓] 本门禁所有项已勾选

全部满足后输出：`=== Gate 2 PASSED ===`

### Gate 3 出口
- [ ] 失败已分析并切换策略（如有）
- [ ] 阻塞已标记（5 次失败）
- [✓] 本门禁所有项已勾选

全部满足后输出：`=== Gate 3 PASSED ===`

### Gate 4 出口
- [ ] 完成报告已输出
- [ ] 错误已记录（如有）
- [ ] 自检通过
- [✓] 本门禁所有项已勾选

全部满足后输出：`=== Gate 4 PASSED ===`

---

## 输出格式模板

所有外部输出必须使用以下模板。

### 启动
```
[Ralph] === Ralph 模式启动 ===
[Ralph] 🎯 目标: 完成XXX
[Ralph] ✅ 标准: 条件1, 条件2
[Ralph] 📋 步骤: 6 步
```

### 进度
```
[Ralph] ✅ (3/6) 步骤3: XXX — 完成 | 尝试: 2 次
[Ralph] 🔄 (3/6) 步骤3: 失败 → 换方法C
[Ralph] ⏸ (3/6) 步骤3: 阻塞 — 已尝试5种方法
```

### 错误
```
[Ralph] ❌ 步骤3: 失败原因...
[Ralph] 🔄 策略切换: 方法 ③ 换方法 C
```

### 自检
```
[Ralph 自检] Gate 1 ✅ | Gate 2 ✅ | Gate 3 ✅ | Gate 4 ✅
[Ralph 自检] 步骤全部处理? [是/否] | 错误已记录? [是/否]
```

### 汇总
```
🔨 Ralph 完成 | ✅ 5/6 | ❌ 1 阻塞 | ⏱ 12m | 🔄 3 次重试
```

---

## 关键规则

### 失败策略顺序（每步最多 5 次尝试）
1. **重试** — 同样方法再试一次
2. **换参数** — 调整参数/超时
3. **换方法** — 完全不同的实现路径
4. **搜方案** — web_fetch 搜索 GitHub/论坛
5. **找 skill** — 搜索是否有现成 skill 能解决

### 安全边界
- 单步最多重试 5 次
- 涉及金钱操作 → 暂停确认
- 不可逆操作（删除/发布）→ 输出 `<danger>` 标签
- 总执行超 30 分钟 → 汇报状态

---

See `details.md` for full reference: 执行流程图、协作模式、示例。