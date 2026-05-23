---
name: executing-plans
description: Use when you have a written implementation plan to execute in a separate session with review checkpoints.
---

<MANDATORY_EXECUTION_SCRIPT>
你必须严格按照以下步骤执行，每完成一步输出 [√] 并附简要结果。
禁止跳过、合并、改变顺序。未输出 [√] 的步骤视为未执行。

## Gate 1: 加载 Plan
STEP 1.1: 输出 `[Exec] === Executing Plans 启动 ===` → [√]
STEP 1.2: 读取 plan 文件 → [√] Plan: {路径} | 任务: {N} 个
STEP 1.3: 初始化 TodoWrite 跟踪所有任务 → [√]
=== Gate 1 PASSED（Plan 已加载）===

## Gate 2: 执行任务
STEP 2.1: 取下一个待办任务 → [√] 当前: {任务名} ({N}/{M})
STEP 2.2: 执行该任务的所有步骤（写代码/跑测试/提交）→ [√]
STEP 2.3: 验证结果 — 测试通过 / lint 通过 / 类型检查通过 → [√] {通过/失败}
         → 失败则修复后重试（最多 3 次）
STEP 2.4: 标记任务完成 → TodoWrite 更新 → [√]
STEP 2.5: 每 3 个任务写 checkpoint → `_checkpoint.md` → [√]
STEP 2.6: 回到 STEP 2.1 取下一任务
=== Gate 2 PASSED（执行完成）===

## Gate 3: 收尾 + 自检
STEP 3.1: 所有任务完成后输出汇总 → [√]
          `[Exec] 🏁 DONE: {N} | FAILED: {M} | ⏱ {X}m`
STEP 3.2: 执行最终验证（全部测试/全部 lint）→ [√]
STEP 3.3: 自检 — 检查是否有遗漏任务或失败的验证 → [√]
=== Gate 3 PASSED（执行完毕）===
</MANDATORY_EXECUTION_SCRIPT>

---

## 五层强制保障

| 层 | 机制 | 位置 |
|----|------|------|
| 1 | 剧本化指令 — MANDATORY 脚本 | 本文件顶部 |
| 3 | 周期性自检 — 每 3 任务 checkpoint + Gate 3 最终自检 | 本文件 Gate 2/3 |
| 4 | 最小化上下文 | 参考移至 `details.md` |
| 5 | 失败任务自动记录 | 依赖 full-autonomous 的 error_patterns |

---

## 硬门禁清单

### Gate 1 出口
- [ ] Plan 已读取: {N} 个任务
- [ ] TodoWrite 已初始化
- [✓] 本门禁所有项已勾选

全部满足后输出：`=== Gate 1 PASSED ===`

### Gate 2 出口
- [ ] 所有任务已执行
- [ ] 验证通过 / 失败已标记
- [ ] Checkpoint 已写入（每 3 任务）
- [✓] 本门禁所有项已勾选

全部满足后输出：`=== Gate 2 PASSED ===`

### Gate 3 出口
- [ ] 最终验证通过
- [ ] 汇总已输出
- [ ] 自检通过
- [✓] 本门禁所有项已勾选

全部满足后输出：`=== Gate 3 PASSED ===`

---

## 输出格式模板

### 启动
```
[Exec] === Executing Plans 启动 ===
[Exec] Plan: docs/plans/xxx.md | 任务: 12 个
```

### 进度
```
[Exec] ✅ (3/12) Task 3: 组件A — DONE
[Exec] 🔄 (4/12) Task 4: 组件B — 重试 2/3
[Exec] ❌ (4/12) Task 4: 组件B — FAILED
```

### Checkpoint
```
[Checkpoint] 完成: 3 | 剩余: 9 | 失败: 0 | 耗时: 15m
```

### 自检
```
[Exec 自检] 全部任务已执行? [是/否] | 最终验证? [通过/失败]
```

### 汇总
```
[Exec] 🏁 DONE: 10 | FAILED: 2 | ⏱ 45m
```

---

## 关键规则

- **每任务最多重试 3 次** — 仍失败则标记 FAILED，继续下一个
- **每 3 任务写 checkpoint** — 断点恢复用
- **执行中不修改 plan** — 只执行，不改计划
- **任务间 0 确认** — 全自动推进

---

See `details.md` for full documentation.