---

name: skill-router
description: 技能路由器。当 AI 不确定该调用哪些技能时自动激活，动态扫描已安装技能，语义匹配最佳组合，编排执行顺序，处理冲突。触发词：该用什么技能、怎么组合、帮我选技能、skill route，或任何涉及多技能协作的复杂任务。
version: 2.1.0
---

> **Reasonix 注意**: 路由表位于 `full-autonomous/rules/01-skill-routing-table.md`。`the-ralph-loop` 已替换为 `full-autonomous`，`ralph-task-executor` 已替换为 `task-executor`。

<MANDATORY_EXECUTION_SCRIPT>
你必须严格按照以下步骤执行，每完成一步输出 [√] 并附简要结果。
禁止跳过、合并、改变顺序。未输出 [√] 的步骤视为未执行。

## 🔴 快速路径（任务类型已明确时使用）
若任务类型在调用时已明确（如 full-autonomous Phase 0 传入），跳过 Gate 1-3 全流程：
- 直接输出 `[Router] ⚡ 快速路径: 类型已明确 ({类型})` 
- 查 rules/01-skill-routing-table.md 返回技能组合包 → [√]
- 不执行全扫描/匹配/冲突检测/工作流装配
=== Gate 0 快速路径 PASSED ===

## Gate 1: 动态发现 + 任务分类
STEP 1.1: 输出 `[Router] === skill-router v3.0 启动 ===` → [√]
STEP 1.2: 动态扫描 ~/.reasonix/skills/ 下所有子目录，读取每个 SKILL.md 的 name+description → [√] 发现 N 个技能
STEP 1.3: 解析用户输入，归入 21 类任务类型之一（见 details.md Step 2）→ [√] 类型: {类别名}
STEP 1.4: 若任务类型不明确 → 触发 zoom-out + grill-me 追问 → [√] 已澄清
=== Gate 1 PASSED（发现+分类完成）===

## Gate 2: 语义匹配 + 冲突检测 + 工作流装配
STEP 2.1: 对每个可用技能按 R-5 标准匹配任务类型，保留相关度 ≥ 中 → [√] 候选 N 个
STEP 2.2: 对候选技能列表做冲突检测（静默×追问、极简×交互、自动×确认、重叠功能）→ [√] 冲突 N 个，已按规则处理
STEP 2.3: 按动态排序原则编排（理解1→评估2→追问3→**设计3.5**→验证4→执行5→循环6）→ [√] 排序完成
STEP 2.4: 动态工作流装配（见 details.md 第五步）— 根据任务类型注入设计/验证类技能
         → 若 web-frontend/web-fullstack → 注入 frontend-design/web-design-guidelines/webapp-testing
         → 若 backend-api → 注入 zoom-out/security-best-practices/tdd
         → 若 mobile-app → 注入 react-native-skills/midscene-test → [√] 装配完成
         `[Router] 📐 工作流: {skillA} → {skillB} → {skillC} | 类型: {web-fullstack/backend/mobile/文档/...}`
=== Gate 2 PASSED（匹配+装配完成）===

## Gate 3: 声明链 + 执行
STEP 3.1: 声明技能链: `[Router] 技能链: {skill1} → {skill2} → {skill3}` → [√]
STEP 3.2: 逐一激活技能，每完成一个输出进度 → [√] {N/M} 完成
STEP 3.3: 每步验证 Gate → 若卡住 → 触发 diagnose → 重新路由或重试 → [√]
STEP 3.4: 动态调整——新需求则重新匹配, 技能不适用则跳过 → [√]
=== Gate 3 PASSED（执行完成）===

## Gate 4: 自检 + 记录
STEP 4.1: 执行自检——检查最近 3 步是否全部含 [√]，技能链是否全部执行 → [√]
STEP 4.2: 回传进度——记录所选技能、耗时、匹配质量到 skill_performance.json → [√]
STEP 4.3: 若有匹配失败或路由错误 → 记录到 error_patterns.json → [√]
=== Gate 4 PASSED（路由完成）===
</MANDATORY_EXECUTION_SCRIPT>

---

## 四层强制保障

| 层 | 机制 | 位置 |
|----|------|------|
| 1 | 剧本化指令 — MANDATORY 脚本，不可跳过 | 本文件顶部 |
| 3 | 周期性自检 — Gate 4 强制自检 + 心跳 | 本文件 Gate 4 |
| 4 | 最小化上下文 — 本文件仅保留执行必须信息 | 详细设计移至 `details.md` |
| 5 | 违例自学习 — 路由失败自动记录 | `opencode-error-patterns` + `skill_performance.json` |

> Layer 2（合规看门狗）由 `compliance-guard` skill + `opencode-core-rules` 全局记忆统一覆盖。

---

## 硬门禁清单（Gate 出口必须逐项输出）

### Gate 1 出口
- [ ] 技能目录已扫描: {N} 个
- [ ] 任务类型已分类: {实际类型}
- [ ] 若类型不明确 → zoom-out+grill-me 已执行
- [✓] 本门禁所有项已勾选

全部满足后输出：`=== Gate 1 PASSED ===`

### Gate 2 出口
- [ ] 候选技能: {N} 个（相关度 ≥ 中）
- [ ] 冲突检测: {N} 个冲突已处理
- [ ] 动态排序完成（含设计类 3.5 优先级）
- [ ] 工作流装配完成: {N} 个技能 | 类型: {类别}
- [✓] 本门禁所有项已勾选

全部满足后输出：`=== Gate 2 PASSED ===`

### Gate 3 出口
- [ ] 技能链已声明
- [ ] 所有技能已按序激活执行
- [ ] 动态调整已处理
- [✓] 本门禁所有项已勾选

全部满足后输出：`=== Gate 3 PASSED ===`

### Gate 4 出口
- [ ] 自检通过
- [ ] 进度已回传
- [ ] 错误已记录（如有）
- [✓] 本门禁所有项已勾选

全部满足后输出：`=== Gate 4 PASSED ===`

---

## 输出格式模板

所有外部输出必须使用以下模板，禁止自由发挥。

### 启动
```
[Router] === skill-router v3.0 启动 ===
[Router] 发现技能: N 个 | 任务类型: {类型}
```

### 匹配结果
```
[Router] 候选: {skill1}(高), {skill2}(中), ... | 冲突: {N} 已处理
[Router] 排序: {skillA}(1) → {skillB}(2) → {skillC}(3.5) → {skillD}(4) → {skillE}(5)
[Router] 📐 工作流: {skillA} → {skillB} → {skillC} | 类型: {web-fullstack/backend/mobile/文档/...}
```

### 声明链
```
[Router] 技能链: {skill1} → {skill2} → {skill3}
```

### 进度
```
[Router] ✅ (1/3) {skill1} 完成
[Router] 🔄 (2/3) {skill2} 失败→重试方法B
[Router] ⏸ (3/3) 阻塞: 原因
```

### 自检
```
[Router 自检] Gate 1 ✅ | Gate 2 ✅ | Gate 3 ✅ | Gate 4 进行中
[Router 自检] 最近 3 步均含 [√]? [是/否]
```

### 汇总
```
[Router] 🏁 路由完成: {N} 技能已编排 | 匹配质量: {高/中/低} | 耗时: {X}s
```

---

## 关键规则

### 触发条件
- 用户消息包含触发词：该用什么技能、怎么组合、帮我选技能、skill route
- full-autonomous 在 Phase 0 STEP 0.2 调用
- 当前任务不属于任何明确 skill 范畴

### 元技能自动纳入
以下技能**始终加入候选**（无论任务类型）：
- **影响分析类** — description 含 impact/blast-radius/affect
- **上下文理解类** — description 含 zoom-out/explore/understand
- **路由器自身** — 不递归

### 动态工作流装配规则
根据 Gate 1 分类的任务类型，排序后自动注入缺失的关键环节技能：
- **设计类项目**（web-frontend/web-fullstack/mobile/design-system）→ 自动补充 frontend-design / shadcn / web-design-guidelines / webapp-testing
- **后端类项目**（backend-api/数据处理）→ 自动补充 zoom-out / security-best-practices / tdd
- **文档/内容类**（文档生成/演示）→ 自动补充 theme-factory / brand-guidelines
- **自动化类**（长任务/Agent）→ 自动补充 autonomous / ralph 循环重试
- 不强制——只补充已安装的技能，缺了不报错，照常执行

### 不确定任务类型
```
1. 激活 zoom-out / explore 获取上下文
2. 激活 grill-me 追问用户意图
3. 根据回答重新分类匹配
```

### 混合任务
```
1. 按依赖关系拆分子任务
2. 每个子任务独立匹配技能
3. 例: "修 Bug + 加缓存" →
   子任务A: Bug 修复 → diagnose
   子任务B: 加缓存 → redis-development
   依赖: A 完成后 → B
```

### 路由失败处理
| 失败场景 | 处理 |
|----------|------|
| 选错技能 | 触发 diagnose → 重新路由 |
| 技能执行失败 | 激活重试类 skill → 3 次后报告 |
| 无匹配技能 | 用 find-skills 搜索生态 → 仍无则通用能力兜底 |
| 3 次重试仍失败 | 暂停，向用户报告 |

---

## 冲突裁决

| 冲突 | 处理 |
|------|------|
| 项目规则 > 本路由 | 项目级 CLAUDE.md 强制要求优先 |
| 重叠功能技能 | 选 description 更具体的 |
| 与 AGENTS.md 冲突 | 以 AGENTS.md 为准 |

---

See `details.md` for full reference: 21 任务分类表、R-5 匹配度标准、冲突检测算法、排序算法、特殊场景详解。
