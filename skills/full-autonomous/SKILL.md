---

name: full-autonomous
description: 五阶段全自动开发剧本 — Phase 0→5，自适应路径 + task-executor 并行 + compliance-guard 审计
version: 3.1.0
builtin-skills: brainstorming, grill-me, grill-with-docs, zoom-out, writing-plans, improve-codebase-architecture, security-best-practices, diagnose, self-improving, ralph-planner, ralph-loop, ralph, no-confirm-silent, proactive-agent, handoff, memory-manager, gitnexus-auto, using-git-worktrees, finishing-a-development-branch

---

<MANDATORY_EXECUTION_SCRIPT>
每完成一步输出 [√]。
**跳过规则**: 允许跳过，但必须输出 `[√] ⏭️ 跳过理由: {一句话}`。无理由跳过 = 违例。追加前检查是否已有同类模式 → 有则合并（提升 confidence），无则新增。
**违例记录**: 每次违例记录到 `error_patterns.json` 时必须包含 `skill_id`（当前 Phase 运行的技能名），格式：`{"error": "...", "confidence": N, "skill_id": "full-autonomous", "phase": N}`。
**权重回调**: 每次追加 error_pattern 后，自动更新 `routing_weights.json`：
  - `confidence >= 0.9` → 对应 skill 的 weight_penalty = 0.3
  - `confidence >= 0.8` → 对应 skill 的 weight_penalty = 0.2
  - `confidence >= 0.7` → 对应 skill 的 weight_penalty = 0.1
  - 同一 skill 的多个 error → 取最高 penalty（非累加，避免反复犯错直接归零）
  - 🔴 **full-autonomous 自身**不受权重惩罚（它的错误是自报告，不是外部验证）
  - 权重自然衰减：若 7 天内无该 skill 的新 error，penalty 减半；14 天无新 error → 归零
  - 技能路由器加载时检查 `routing_weights.json`：weight_penalty > 0 的技能自动降级到备选列表末尾

## 🔴 执行前检查
> **默认开启**：AGENTS.md MANDATORY_SCRIPT STEP 3 已做复杂度评估，此文件从 Phase 1 或直接 Phase 3 开始执行。
> **触发词后备**：用户说"全自动"时强制 Full 路径。
> **快速跳过**：用户说"直接回答/快速回答"时强制 Quick 路径（跳过整个 Phase 流程，直接执行）。

1. 递归深度检测：上下文 `[Auto] === full-autonomous` 出现 ≤2 次 → 继续；否则中止 → [√]
2. 看门狗已在 AGENTS.md STEP 1 启动，此处仅初始化 state.json：`write_file` state.json → [√]
3. 输出启动标记 → [Auto] === full-autonomous v3.1 启动 === 时间 → [√]

## Phase 0: 分类
<超快速路径入口> 若复杂度 ≤ 3 且 类型为 analysis/explore/diagnose → 输出类型后直接跳 Phase 3，跳过其余 → [√]
- 加载 skill-router → 若类型已明确则走快速路径（跳过全扫描/匹配/冲突检测）→ [√] 类型: {类型}
- STEP 0.2: 检测模式标志 → 若检测到 silent/静默/无确认意图则加载 `no-confirm-silent`；检测到 proactive/自动/主动意图则加载 `proactive-agent` → [√] 模式: {normal|silent|proactive}
- 评估复杂度 (1-10) → [√] 复杂度:N → {Quick|Standard|Full}
- **分析/评估/探索类任务自动降级为 Quick 路径**（跳过 Phase 2 全套设计流程，直接进入 Phase 3 并行读取）→ [√]
- 技能缺口检测 → 有则触发 write-a-skill → [√]
- 启动看门狗 + 加载 `memory-manager` 做启动时压缩检测 → [√]
**格式自检**: 检查最近 3 步是否均含 [√] → ✅
=== Phase 0 PASSED ===

## Phase 1: 装配
- 查 rules/01-skill-routing-table.md → 获取技能组合包 → 加载 → [√] N 个
- Quick → 跳 Phase 3 | Standard → Phase 2a | Full → Phase 2b
=== Phase 1 PASSED ===

## Phase 2a: 需求打磨（Standard）— 每步独立 [√]
- [√/⏭️] STEP 2a.1: brainstorming (探索需求)
- [√/⏭️] STEP 2a.2: grill-me (压力测试)
- [√/⏭️] STEP 2a.3: zoom-out (架构评估)
- [√/⏭️] STEP 2a.4: writing-plans (实施计划)
→ Phase 2.3

## Phase 2b: 深度设计（Full）— 每步独立 [√]
- [√/⏭️] STEP 2b.1: brainstorming
- [√/⏭️] STEP 2b.2: grill-with-docs
- [√/⏭️] STEP 2b.3: zoom-out
- [√/⏭️] STEP 2b.4: improve-codebase-architecture
- [√/⏭️] STEP 2b.5: security-best-practices
- [√/⏭️] STEP 2b.6: 输出实施计划
→ Phase 2.3
**格式自检**: 检查最近 3 步是否均含 [√] → ✅
=== Phase 2 PASSED ===

## Phase 2.3: 任务规划细化（Standard/Full）
<Quick> 跳过 → [√]
- [√/⏭️] STEP 2.3.1: Standard/Full 路径 → 调用 `ralph-planner` 做细粒度任务拆分 + 依赖编排，补充 writing-plans 的粗粒度计划 → [√] 任务: {N} 个子任务
- [√/⏭️] STEP 2.3.2: 检查计划中是否有代码修改类任务 → 有则标记"需 gitnexus 影响分析" → [√]
**格式自检** → ✅
=== Phase 2.3 PASSED ===

## Phase 2.5: 前置检查 — 每步独立 [√/⏭️]
- [√/⏭️] Full 路径 → 强制调用 `using-git-worktrees` 创建隔离工作区
- [√/⏭️] Standard 路径 → 按需询问是否需要 worktree
**格式自检** → ✅
=== Phase 2.5 PASSED ===

## Phase 3: 执行 — 每步独立 [√]
<HARD-GATE-TOOL>
### 工具选择规则
🟢 **读 1-5 个文件** → `read_file`（同轮次并发调，不等返回再调下一个），**跳过审计**
🟡 **读 6-10 个文件** → 拆 2 批 `read_file` 或用 `explore`，**跳过审计**
🟡 **理解代码逻辑/架构流** → `explore`，**跳过审计**
🔴 **≥10 个文件批量统计** → 禁止 read_file 逐个，必须拆成 explore 分批
🔴 **编码/修改** → 先 `gitnexus-auto` 做影响分析，再用 `multi_edit` 批量写入（不要串行 edit_file），最后 task-executor 收尾，**强制 compliance-guard 审计** + `[ToolDeclare]`
🟡 **独立命令** → `run_command` 同轮次并发（互不依赖的命令同时发），不等一个返回再发下一个
🟡 **批量编辑** → `multi_edit`（所有编辑验证通过后才写磁盘，失败则全部回滚），禁止串行 `edit_file`
**子代理类型**: explore(只读) / task-executor(写操作) / task-executor + ralph-loop(复杂多步骤)
</HARD-GATE-TOOL>
- [√] STEP 3.1: 拆分依赖图 + Level 0 并行派发
- [√] STEP 3.2: **代码修改类子任务前置** — 调用 `gitnexus-auto` 做索引→上下文→影响分析→改代码→变化检测全流程 → [√] 影响级别: {LOW/MEDIUM/HIGH}
- [√] STEP 3.3: Level 0 并行派发 → Standard/Full 路径默认启用 `ralph-loop` 模式（红-绿-重构循环）；Quick 路径单次执行 → [√] 模式: {ralph-loop|单次}
- [√] STEP 3.4: 聚合结果 → 下一层依赖
- [√] STEP 3.5: 子任务重试 → 连续失败时加载 `ralph` 做计划→执行→检查→重试循环（最多 3 种不同策略后标记阻塞）→ [√]
- [√] STEP 3.6: 自检 rules/04-self-check.md
**格式自检**: 检查最近 3 步是否均含 [√] → ✅
=== Phase 3 PASSED ===

## Phase 4: 验证 — 每步独立 [√]
- [√] STEP 4.1: 运行测试 → N/M（或分析类任务的质量自检）
- [√] STEP 4.2: 失败 → diagnose → 修复 → 重跑
- [√] STEP 4.3: Full 路径 → security-best-practices 最终审查
- [√/⏭️] STEP 4.4: **分析类质量自检**: 聚合结果是否覆盖全部提问点？有无文件读失败？输出是否结构化？→ ✅
**格式自检**: 检查最近 3 步是否均含 [√] → ✅
=== Phase 4 PASSED ===

## Phase 4.5: 分支收尾检查 — 每步独立 [√/⏭️]
<Quick> 跳过 → [√]
- [√/⏭️] Standard 路径 → 询问合并/PR/保留/丢弃
- [√/⏭️] Full 路径 → 强制调用 `finishing-a-development-branch`
**格式自检** → ✅
=== Phase 4.5 PASSED ===

## Phase 5: 交付 — 每步独立 [√]
- [√/⏭️] STEP 5.1: git-commit（如适用）
- [√] STEP 5.2: 停看门狗：`stop_job(watchdog_job_id)`
- [√/⏭️] STEP 5.3: **主动归档** — 若任务未完成或后续需续做 → 调用 `handoff` 生成交接文档 → [√] {已生成/无需交接}
- [√/⏭️] STEP 5.4: **交付报告** — 默认标准格式；若 Phase 0 检测到 silent 模式则输出精简版 → [√]
- [√/⏭️] STEP 5.5: **memory 清理** — 调用 `memory-manager` 做 session 结束清理 → [√]
- [√] **STEP 5.6: 强制复盘 + 经验写入**（必须写，不写 = 违例）
  a) 追加复盘记录到 `skill_performance.json`，格式：
    ```json
    {
      "timestamp": "{ISO时间}",
      "skill": "full-autonomous",
      "action": "{任务描述}",
      "assessment": "success|partial|failure",
      "reason": "{一句话评价}",
      "next_time": "{下次改进}",
      "duration_seconds": {N},
      "phases_completed": [0,1,2,3,4,5],
      "violations_count": {N},
      "skills_used": ["{skill1}"],
      "skills_skipped": ["{skill3}"]
    }
    ```
  b) 写入经验到 `memory/experiences/` — 文件名 `{ISO日期}-{任务摘要}.md`，包含：做了什么、遇到什么问题、如何解决的、下次注意什么
  c) learnings/ 超过 20 条时删除最旧文件
  d) 验证写入是否成功：`read_file skill_performance.json` 最后一条应为刚写的记录 → [√] {已写入/N 条}
- [√] STEP 5.7: 清理当前会话日志（`.jsonl` / `.meta.json` / `checkpoints/`），保留 `.bak` 备份
- [√] STEP 5.8: 通知用户
**格式自检**: 检查最近 3 步是否均含 [√] → ✅
[State] 删除 state.json
=== Phase 5 PASSED ===
</MANDATORY_EXECUTION_SCRIPT>

## 引用文件
| 路径 | 内容 | 何时看 |
|------|------|--------|
| rules/01-skill-routing-table.md | 路由表（类型→技能组合） | Phase 1 |
| rules/02-gate-checklists.md | Phase 出口检查清单 | 每 Phase 结束时 |
| rules/03-output-format.md | 输出模板（[Auto]/自检/危险操作） | 首次使用时 |
| rules/04-self-check.md | 周期性自检流程 | Phase 3 |
| docs/execution-flow.md | 执行流程详解 | 需要时 |
| docs/extension-mechanisms.md | 扩展机制（**DRAFT** — 尚未实现） | 不应引用 |
| scripts/watchdog.py | 外部看门狗进程 | STEP 1 自动启动（AGENTS.md 管理）|
