---

name: full-autonomous
description: 五阶段全自动开发剧本 — Phase 0→5，自适应路径 + task-executor 并行 + compliance-guard 审计
version: 3.4.0

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
> **技能发现**：不维护硬编码技能列表。所有技能由 skill-router 在 Phase 0 动态扫描 `~/.reasonix/skills/` 发现加载。
> **触发词后备**：用户说"全自动"时强制 Full 路径。
> **快速跳过**：用户说"直接回答/快速回答"时强制 Quick 路径（跳过整个 Phase 流程，直接执行）。

1. 递归深度检测：上下文 `[Auto] === full-autonomous` 出现 ≤2 次 → 继续；否则中止 → [√]
2. 🔴 **启动看门狗**：`run_background("python ~/.reasonix/scripts/watchdog.py")` → [√] PID:{N}（若已运行则跳过）
3. 初始化 state.json：`write_file state.json {"phase":0,"step":0,"startedAt":"{ISO时间}"}` → [√]
3. 输出启动标记 → [Auto] === full-autonomous v3.4 启动 === 时间 → [√]

## Phase 0: 分类
<超快速路径入口> 若复杂度 ≤ 3 且 类型为 analysis/explore/diagnose → 输出类型后直接跳 Phase 3，跳过其余 → [√]
- 加载 skill-router → 若类型已明确则走快速路径（跳过全扫描/匹配/冲突检测）→ [√] 类型: {类型}
- STEP 0.2: 检测模式标志 → 若检测到 silent/静默/无确认意图则加载 `no-confirm-silent`；检测到 proactive/自动/主动意图则加载 `proactive-agent` → [√] 模式: {normal|silent|proactive}
- 评估复杂度 (1-10) → [√] 复杂度:N → {Quick|Standard|Full}
- **分析/评估/探索类任务自动降级为 Quick 路径**（跳过 Phase 2 全套设计流程，直接进入 Phase 3 并行读取）→ [√]
- 技能缺口检测 → 有则触发 write-a-skill → [√]
- 加载 `memory-manager` 做启动时压缩检测 → [√]
- [√] **合规预检** — 调用 `compliance-check` 验证 Rule 0（技能预检）/ Rule 2（简洁性）/ Rule 8（读后写）→ [√]
**格式自检**: 检查最近 3 步是否均含 [√] → ✅
=== Phase 0 PASSED ===
- 更新 state.json：`write_file state.json {"phase":1,"step":"PASS","startedAt":"{ISO时间}"}` → [√]

## Phase 1: 装配
- 查 rules/01a-routing-quick-index.md → 匹配任务类型获取 Core 技能包 → 需要扩展技能时回查 rules/01-skill-routing-table.md 取 Enhanced/Extended/Testing → 加载 → [√] N 个
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
- [√] **STEP 3.0: 错误模式预检** — 在编码/测试前先加载 `error_patterns.json`，匹配当前场景的已知错误模式 → 有则输出 `[ErrorPattern] {已知模式} → apply prevention` 并遵循 prevention 策略 → [√] {匹配 N 条/无匹配}
- [√] STEP 3.1: 拆分依赖图 + Level 0 并行派发
- [√] STEP 3.2: **代码修改类子任务前置** — 调用 `gitnexus-auto` 做索引→上下文→影响分析→改代码→变化检测全流程 → [√] 影响级别: {LOW/MEDIUM/HIGH}
- [√] STEP 3.3: Level 0 并行派发 → Standard/Full 路径默认启用 `ralph-loop` 模式（红-绿-重构循环）；Quick 路径单次执行 → [√] 模式: {ralph-loop|单次}
- [√] STEP 3.4: 聚合结果 → 下一层依赖
- [√] STEP 3.5: 子任务重试 → 连续失败时加载 `ralph` 做计划→执行→检查→重试循环（最多 3 种不同策略后标记阻塞）→ [√]
- [√] STEP 3.6: 更新 `state.json` 记录当前 phase/step → `write_file state.json {\"phase\":3,\"step\":3.6,\"startedAt\":\"{ISO时间}\"}`
- [√] **STEP 3.6a: 🔴 修复闭环 — 强制记录新错误模式** — 本次执行中发现的任何新 Bug/错误，追加到 `error_patterns.json`（含 `skill_id`/`phase`/`confidence`/`fix`/`prevention`），然后更新 `routing_weights.json`（按 confidence 设 penalty）→ 追加前检查是否已有同类模式 → 有则合并（提升 confidence），无则新增 → [√] {新增 N 条/合并 N 条/无新错误}
- [√] STEP 3.7: 加载 `error_patterns.json` 检查是否有当前场景的已知错误模式 → 有则应用 `fix` 策略 → 输出 `[ErrorPattern] {已知模式}: {apply fix}`
- [√] STEP 3.8: 自检 rules/04-self-check.md
- [√] **合规出口** — 调用 `compliance-check` 验证 Phase 3 合规性 → [√]
**格式自检**: 检查最近 3 步是否均含 [√] → ✅
- 更新 state.json：`write_file state.json {"phase":3,"step":"PASS","startedAt":"{ISO时间}"}` → [√]
=== Phase 3 PASSED ===

## Phase 4: 验证 — 每步独立 [√]
- [√] **STEP 4.0: 错误模式预检 + 平台检测** — 加载 `error_patterns.json` 匹配当前测试场景 + 检测 OS 平台（Windows/Linux/macOS）→ Windows 时自动防御：① subprocess 不用 text=True ② Flask 验证用 test_client ③ 文件路径用 os.path.join ④ 编码用 utf-8 errors=replace → [√] 平台: {Windows|Linux|macOS} 防御: {N 条}
- [√] **STEP 4.0.5: 测试 import 路径自检** — Python 项目若有 `tests/` 子目录且执行 pytest 时报 import 错误 → 检查 conftest.py 是否有 sys.path.insert；若测试文件 import 项目模块失败，自动生成 conftest.py 补 sys.path → [√] {正常/已修复}
- [√] STEP 4.1: 运行测试 → N/M（或分析类任务的质量自检）
- [√] STEP 4.2: 失败 → diagnose → 修复 → 重跑
- [√] **STEP 4.2.5: 🔴 修复后强制记录到 error_patterns.json** — 任何测试/运行中发现的 Bug，修复完毕后立即追加到 `error_patterns.json`（含 `skill_id`/`phase`/`confidence`/`fix`/`prevention`）+ 更新 `routing_weights.json`（按 confidence 设 penalty）→ 追加前检查是否已有同类 → 有则合并提升 confidence → [√] {新增 N 条/合并 N 条}
- [√] STEP 4.3: Full 路径 → security-best-practices 最终审查
- [√/⏭️] STEP 4.4: **应用内测** — 调用路由表 `testing` 行匹配技能（如 dogfood/webapp-testing/midscene-test）→ [√] {已测试/N 技能/不适用}
- [√] **合规出口** — 调用 `compliance-check` 验证 Phase 4 合规性 → [√]
**格式自检**: 检查最近 3 步是否均含 [√] → ✅
- 更新 state.json：`write_file state.json {"phase":4,"step":"PASS","startedAt":"{ISO时间}"}` → [√]
=== Phase 4 PASSED ===

## Phase 4.5: 分支收尾检查 — 每步独立 [√/⏭️]
<Quick> 跳过 → [√]
- [√/⏭️] Standard 路径 → 询问合并/PR/保留/丢弃
- [√/⏭️] Full 路径 → 强制调用 `finishing-a-development-branch`
**格式自检** → ✅
=== Phase 4.5 PASSED ===

## Phase 5: 交付 + 自我回顾与进化 — 所有路径通用（Quick 精简版，Standard/Full 完整版）

> 🧠 **核心理念**: 每次执行结束后，系统自动回顾全过程、发现可改进点、更新知识库，确保下一次比这一次更好。
> **Quick 路径**: 跳过阶段 A/B/E，必须执行阶段 C/D（保底学习）
> **Standard/Full 路径**: 必须执行全部 A→E

### 阶段 A: 执行过程回顾（Standard/Full）
- [√] **STEP 5A.1: 扫描执行记录** — 回顾本次任务：完成了什么、卡在哪儿、跳过了哪些步骤 → 输出回顾摘要 → [√] {N 个步骤完成 / M 个问题}
- [√] **STEP 5A.2: 检查违例** — 回顾是否有无理由跳过的步骤 → 若有则追加到 error_patterns.json（违例格式：`{"error":"无理由跳过 {步骤}","confidence":0.7,"skill_id":"full-autonomous","phase":{N},"fix":"输出 [√] ⏭️ 理由:{一句话}"}`）→ [√] {N 次违例}
- [√] **STEP 5A.3: 对比预期 vs 实际** — 计划复杂度 vs 实际耗时/步骤数 → 若偏差大则记录到经验（下次评估更准）

### 阶段 B: 错误模式分析（Standard/Full）
- [√] **STEP 5B.1: 扫描本次遇到的所有问题** — 逐个回溯：bug/报错/crash/异常/不符合预期的行为 → 列出问题清单 → [√] {N 个问题}
- [√] **STEP 5B.2: 交叉对比 error_patterns.json** — 每个问题查 error_patterns.json：有匹配 → 提升 confidence（取 max）；无匹配 → 追加新记录（含 skill_id/phase/confidence(0.7起)/fix/prevention）→ [√] {命中 N 条 / 新增 N 条}
- [√] **STEP 5B.3: 更新 routing_weights.json** — 按新错误模式的 confidence 更新对应技能的 weight_penalty（规则同前：0.7→0.1, 0.8→0.2, 0.9→0.3；full-autonomous 自身豁免；同一 skill 取最高）→ [√] {更新 N 条}

### 阶段 C: 经验写入 + 验证（所有路径 🔴 必须）
- [√] **STEP 5C.1: 追加 skill_performance.json** — `write_file` 写入，格式：
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
    "errors_found": {N},
    "errors_recorded": {N},
    "skills_used": ["{skill1}"],
    "skills_skipped": ["{skill3}"]
  }
  ```
- [√] **STEP 5C.2: 写入经验到 memory/experiences/** — `write_file` 创建 `{ISO日期}-{任务摘要}.md`，内容包含：做了什么、遇到什么问题、如何修复的、下次如何预防、本次学到了什么可泛化的规则
- [√] **STEP 5C.3: 🔴 验证写入** — `read_file skill_performance.json` 确认最后一条为刚写记录 → 失败则重写 + 记违例 → [√] {已验证/N 条}
- [√] **STEP 5C.4: learnings/ 轮转** — 超过 20 条时删除最旧文件

### 阶段 D: 进化建议（Standard/Full）
- [√] **STEP 5D.1: 输出 1-3 条进化建议** — 格式：`下次{场景}→{新做法}` → [√] {N 条建议}
- [√] **STEP 5D.2: 若发现问题可泛化为全局规则** → 追加到 AGENTS.md 或通过 `remember` 写全局记忆 → [√] {已更新/无需}
- [√] **STEP 5D.3: 更新 state.json** — `write_file state.json {"phase":5,"step":"REVIEW_DONE","startedAt":"{ISO时间}"}`
**格式自检**: 检查最近 3 步是否均含 [√] → ✅

### 阶段 E: 系统清理（所有路径）
- [√] STEP 5E.1: **通知用户** — 交付报告 + 进化建议
- [√/⏭️] STEP 5E.2: **日志轮转** — 检查 usage.jsonl >512KB → 归档 → [√] {正常/已轮转}
- [√/⏭️] STEP 5E.3: **memory 清理** — 调用 memory-manager 结束清理 → [√]
- [√] STEP 5E.4: **停看门狗** — `stop_job(watchdog_job_id)` → [√]
- [√/⏭️] STEP 5E.5: **主动归档** — 未完成任务 → 调用 handoff 交接文档 → [√] {已生成/无需}
- [√/⏭️] STEP 5E.6: **git-commit**（如适用）→ [√]
[State] 删除 state.json
=== Phase 5 PASSED ===
</MANDATORY_EXECUTION_SCRIPT>

## 引用文件
| 路径 | 内容 | 何时看 |
|------|------|--------|
| rules/01a-routing-quick-index.md | 路由精简索引（快速查找） | Phase 1 |
| rules/01-skill-routing-table.md | 完整路由表（含Enhanced/Extended/Testing） | 需要扩展技能时 |
| rules/02-gate-checklists.md | Phase 出口检查清单 | 每 Phase 结束时 |
| rules/03-output-format.md | 输出模板（[Auto]/自检/危险操作） | 首次使用时 |
| rules/04-self-check.md | 周期性自检流程 | Phase 3 |
| docs/execution-flow.md | 执行流程详解 | 需要时 |
| docs/extension-mechanisms.md | 扩展机制（**DRAFT** — 尚未实现） | 不应引用 |
| scripts/watchdog.py | 外部看门狗进程 | STEP 1 自动启动（AGENTS.md 管理）|
