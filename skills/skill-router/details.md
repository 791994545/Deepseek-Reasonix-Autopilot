# Skill Router v2 — 动态技能路由器

> 不写死技能列表。动态扫描，语义匹配，自动编排。

---

## 第一步：动态发现技能

**不要依赖写死的技能列表。** 每次路由时，动态扫描技能目录：

```
扫描路径: ~/.reasonix/skills/
对每个子目录:
  读取 SKILL.md 的 frontmatter
  提取: name, description
  构建当前可用技能清单
```

### 扫描方法

1. 列出 `skills/` 下所有子目录
2. 对每个子目录，读取 `SKILL.md` 的前 10 行（frontmatter 部分）
3. 提取 `name` 和 `description` 字段
4. 构建可用技能清单：`{name: string, description: string}[]`

### 为什么动态

- 新技能随时可能安装
- 旧技能可能被删除
- 不同项目可能有项目级技能
- 写死列表 = 维护负担 = 必然过时

---

## 第二步：任务分类

根据用户输入的语义，将任务归入以下类别之一：

| 类别 | 识别信号 |
|------|---------|
| **新功能开发** | 添加、实现、开发、新建、create、add、build |
| **Bug 修复** | 修复、bug、报错、异常、fix、debug、500、error |
| **代码审查** | 审查、review、检查、看看有没有问题 |
| **重构** | 重构、refactor、优化结构、拆分、合并 |
| **调试追踪** | 为什么、怎么回事、trace、排查、定位 |
| **架构改进** | 架构、设计、改进、improve、技术债、shallow |
| **需求分析** | 需求、PRD、规划、plan、想做一个、idea |
| **长任务全自动** | 全自动、通宵跑、批量、overnight、别停、ralph |
| **文档/交接** | 文档、交接、handoff、说明、onboarding |
| **代码理解** | 怎么工作、理解、explain、怎么跑的、架构是啥 |
| **Issue 管理** | issue、任务拆分、排优先级、triage |
| **测试** | 测试、test、覆盖率、TDD、spec |
| **前端/UI** | 页面、组件、样式、CSS、HTML、React、shadcn |
| **后端/API** | API、数据库、查询、存储、Redis、Neo4j |
| **设计/原型** | 设计、原型、UI设计、PRD、prototype |
| **文档生成** | docx、pdf、pptx、xlsx、markdown、报告、PPT |
| **自动化/Agent** | 自动、循环、无人值守、browser、批处理 |
| **技能管理** | 技能、安装、查找、创建技能、skill |
| **安全审查** | 安全、权限、认证、审计、vulnerability |
| **移动开发** | React Native、Expo、Android、iOS |
| **其他** | 不属于以上任何类别 |

---

## 第三步：语义匹配

对当前可用技能清单中的每个技能，用其 `description` 与任务类别做语义匹配：

### 匹配规则

```
对于每个可用技能:
  读取 description + name
  判断: 这个技能的 description 是否与当前任务类别相关？
  相关度: 高 / 中 / 低 / 无关  (标准见 R-5 匹配度量化)
  只保留 相关度 >= 中 的技能
```

### R-5 匹配度量化标准

| 级别 | 判定条件 | 示例 |
|------|----------|------|
| **高** | description 直接包含任务类别中的核心动词/技术名词（≥2 个匹配），或 trigger phrases 完全命中 | "调试"→diagnose(含debug/fix/trace)；"写前端"→frontend-design(含React/component/UI) |
| **中** | description 包含 1 个核心动词或技术名词，语义明显相关 | "加缓存"→redis-development(含Redis) |
| **低** | 仅有边缘关联，或无直接匹配但可间接使用 | "写文档"→knowledge-capture(含documentation) |
| **无关** | description 与任务无任何语义关联 | "写数据库"→frontend-design |

**特异性加权**：当多个技能匹配度相同时，description 长度越长、含可操作动词越多、含具体技术名词越多，排名越前（R-2）。

### 通用匹配模式（不依赖具体技能名）

| 任务类别 | 匹配 description 中的语义信号 |
|----------|---------------------------|
| 新功能开发 | implement, create, build, develop, prototype, TDD, test |
| Bug 修复 | debug, diagnose, fix, trace, error, bug, reproduce |
| 代码审查 | review, architecture, improve, quality, audit |
| 重构 | refactor, rename, extract, split, restructure, impact |
| 调试追踪 | debug, trace, diagnose, why, reproduce, minimize |
| 架构改进 | architecture, design, improve, shallow, deepen |
| 需求分析 | plan, PRD, requirement, grill, question, interview |
| 长任务全自动 | autonomous, loop, retry, unstoppable, executor, silent |
| 文档/交接 | document, handoff, context, onboarding, docx, pdf, pptx, xlsx |
| 代码理解 | explore, understand, zoom, context, architecture |
| Issue 管理 | triage, issue, prioritize, breakdown |
| 测试 | test, TDD, spec, verify, red-green, webapp-testing |
| 前端/UI | frontend, UI, component, style, React, shadcn, design |
| 后端/API | backend, API, database, Redis, security, server |
| 设计/原型 | prototype, design, PRD, plan, figma, theme |
| 文档生成 | document, generate, create, docx, pdf, pptx, xlsx, slides |
| 自动化/Agent | autonomous, loop, unstoppable, browser, agent, automation |
| 技能管理 | skill, install, find, create, write-a-skill |
| 安全审查 | security, audit, vulnerability, best-practices |
| 移动开发 | mobile, react-native, expo, iOS, Android |

### 附加规则：元技能自动匹配

以下类型的技能**始终纳入候选**（无论任务类别）：

- **影响分析类** — description 中包含 impact, blast-radius, affect — 改代码前必用
- **上下文理解类** — description 中包含 zoom-out, explore, understand — 理解先于行动
- **路由器自身** — 不递归

---

## 第四步：冲突检测

匹配出的技能之间可能冲突，需要检测并处理：

### 冲突检测规则（通用，不依赖具体技能名）

| 冲突模式 | 检测方法 | 处理方式 |
|----------|---------|---------|
| **静默 vs 追问** | description 含 silent/quiet/no-confirm，另一个含 grill/question/interview | 追问阶段自动暂停静默模式 |
| **极简 vs 交互** | description 含 caveman/compressed/terse，另一个含 interview/question/grill | 交互阶段暂停极简模式 |
| **自动执行 vs 需确认** | description 含 autonomous/executor/no-stop，另一个含 confirm/approve/triage | 确认步骤优先，确认后再自动执行 |
| **重叠功能** | 两个技能 description 语义高度相似 | 选更具体的那个，或按用户偏好选 |

### 检测方法

```
对于候选技能列表中的每对 (A, B):
  如果 A.description 包含 "silent/quiet/no-confirm"
  且 B.description 包含 "grill/question/interview"
  → 标记为冲突，按上表处理
```

---

## 第五步：排序编排 + 动态工作流装配

### 排序原则（含设计/验证类的动态识别）

| 优先级 | 原则 | 匹配方式 | 含义 |
|--------|------|---------|------|
| 1 | **理解先于行动** | 语义匹配 | explore/understand/zoom/context |
| 2 | **评估先于修改** | 语义匹配 | impact/analyze/diagnose/assess |
| 3 | **追问先于实现** | 语义匹配 | grill/question/interview/plan/PRD |
| 3.5 | **设计先于编码** | 语义匹配（动态识别） | 见下方案例 |
| 4 | **验证先于交付** | 语义匹配 | test/TDD/verify |
| 5 | **执行完成功能** | 语义匹配 | execute/implement/build/create |
| 6 | **循环/续航** | 语义匹配 | loop/retry/autonomous/unstoppable |

### 排序算法（动态增强版）

```
对候选技能按以下规则排序:

优先级 1 — 理解类:
  description 含 explore/understand/zoom/context/map/trace

优先级 2 — 评估类:
  description 含 impact/analyze/diagnose/assess/audit/blast-radius
  
优先级 3 — 追问/规划类:
  description 含 grill/question/interview/plan/PRD/breakdown/requirement

优先级 3.5 — 设计/创建类（动态识别）:
  description 含 design/create/component/UI/style/theme/mockup/
    prototype/shader/visual/layout/composition/shadcn/figma/
    React/TSX/landing/brand/palette/typography/art

优先级 4 — 验证/测试类:
  description 含 test/TDD/verify/QA/spec/coverage/regression/
    webapp-testing/midscene/dogfood/web-design-guidelines

优先级 5 — 执行/构建/实现类:
  description 含 execute/implement/build/create/develop/code/
    scaffold/generate/construct/assemble/integrate/deploy

优先级 6 — 循环/续航/交接:
  description 含 loop/retry/autonomous/unstoppable/executor/
    handoff/checkpoint/recovery/persist/ralph

优先级 0（强制最前，不影响主流程）:
  description 含 meta/skill-router/find-skills/write-a-skill
```

#### 为什么设计类在 3.5（追问之后，编码之前）

自然的项目流程是：
```
理解需求 → 评估影响 → 追问澄清 → 设计原型 → 测试验证 → 编码实现 → 循环迭代
```

设计类技能（frontend-design, shadcn, figma, theme-factory 等）应该在**需求明确之后、动手编码之前**执行。优先级 3.5 正好插在追问（3）和测试（4）之间。

#### 验证类的动态双位置

验证类技能（test/TDD/verify）实际上有两类用途：
- **设计验证**（优先级 3.5 后）— web-design-guidelines, accessibility 等在交付前审查
- **测试驱动**（优先级 4）— tdd 在编码前先写测试

排序算法根据上下文处理：若技能名/description 含 design/audit/review/guideline → 更靠近 3.5；含 tdd/spec/coverage → 更靠近 4。

### 动态工作流装配

排序完成后，根据任务类型（Gate 1 已分类）自动装配完整工作流：

```
装配规则: 从排序后的技能链中，按任务类型在关键节点插入辅助技能
  
  任务类型: web-frontend | web-fullstack
  装配模式:
    (排序) → 注入 frontend-design/frontend-skill/theme-factory 
              (若不在候选但描述匹配) → 继续执行
    验证阶段: 注入 web-design-guidelines / webapp-testing / midscene-test

  任务类型: backend-api | 后端
  装配模式:
    设计阶段: 注入 security-best-practices / zoom-out
    验证阶段: 注入 tdd / diagnose

  任务类型: 全栈 | web-fullstack
  装配模式:
    设计阶段: frontend-design + zoom-out + security-best-practices
    验证阶段: tdd + webapp-testing + web-design-guidelines

  任务类型: 移动开发
  装配模式:
    设计阶段: react-native-skills + frontend-design
    验证阶段: tdd + webapp-testing + midscene-test

  任务类型: 文档生成
  装配模式:
    设计阶段: theme-factory + brand-guidelines
    验证阶段: 无（文档完成即交付）

  任务类型: 自动化/Agent
  装配模式:
    设计阶段: 无
    验证阶段: 无（依赖运行时验证）
    增强: 注入 autonomous-unstoppable/ralph 循环重试

  任务类型: CLI/数据处理/配置
  装配模式:
    设计阶段: 无（或 minimal）
    验证阶段: tdd
```

> ⚠️ 以上装配规则是**参考模式**，不是硬编码。路由器先按语义匹配合格技能，再用这些规则补充缺失的链路。如果某类技能不存在（比如 mobile-app 但 react-native-skills 没安装），不报错，直接用现有的。

#### 装配后的工作流示例

**示例 1: "帮我做个博客前端"** → 类型: web-frontend
```
匹配: frontend-design(高) + shadcn(中) + theme-factory(中)
排序: frontend-design(3.5) → theme-factory(3.5) → shadcn(3.5)
装配: ↑ + web-design-guidelines(4) + webapp-testing(4)
最终链: brainstorming → frontend-design → theme-factory → shadcn → 
        writing-plans → web-design-guidelines → executing-plans → webapp-testing
```

**示例 2: "写个 REST API"** → 类型: backend-api
```
匹配: mcp-builder(高) + security-best-practices(中)
排序: security-best-practices(2) → mcp-builder(5)
装配: ↑ + zoom-out(1) + tdd(4)
最终链: brainstorming → zoom-out → security-best-practices → 
        writing-plans → tdd → mcp-builder → executing-plans
```

**示例 3: "全栈电商网站"** → 类型: web-fullstack
```
匹配: frontend-design(高) + shadcn(中) + mcp-builder(中) + redis-development(中)
排序: frontend-design(3.5) → shadcn(3.5) → mcp-builder(5) → redis-development(5)
装配: ↑ + zoom-out(1) + security-best-practices(2) + tdd(4) + webapp-testing(4) + web-design-guidelines(4)
最终链: brainstorming → zoom-out → security-best-practices → 
        frontend-design → shadcn → writing-plans → tdd → 
        web-design-guidelines → webapp-testing → mcp-builder → 
        redis-development → executing-plans
```

**示例 4: "做个 PPT 汇报"** → 类型: 文档生成
```
匹配: slides(高)
排序: slides(5)
装配: ↑ + theme-factory(3.5) + brand-guidelines(3.5)
最终链: slides → theme-factory → brand-guidelines
```

---

## 第六步：执行协议

```
1. 声明: "本次任务将使用: [skill1] → [skill2] → [skill3]"
2. 逐步激活，完成一个再进下一个
3. 每步验证:
    - 是否达到该技能的完成标准？
    - 下一步前置条件是否满足？
    - 是否发现需要额外技能？→ 动态加入
4. 动态调整:
    - 新需求 → 重新走匹配流程
    - 技能不适用 → 跳过
    - 出现冲突 → 按冲突规则处理
5. 进度回传（R-4）:
    每次技能执行后回传:
    - task_id, skill_name, status(success/fail/downgraded)
    - duration_seconds, tokens_used (如可获取)
    - error_type (如果失败): timeout/api/逻辑/技能不匹配
    编排器利用回传数据更新任务状态、触发降级或回溯
```

---

## 特殊场景

### 不确定任务类型

```
1. 激活理解类技能（zoom-out / explore）获取上下文
2. 激活追问类技能（grill-me）追问用户意图
3. 根据回答重新分类和匹配
```

### 混合任务 (R-6 多类别并行匹配)

```
1. 将任务拆分为主任务 + 可独立执行的子任务
2. 每个子任务独立匹配技能
3. 匹配结果打平为并行队列，按依赖关系排序
4. 例: "修复搜索bug并加缓存" →
   子任务A: 修复搜索bug → diagnose
   子任务B: 添加缓存 → redis-development
   依赖: 子任务A 完成后 → 子任务B (避免缓存掩盖bug)
```

### 技能执行失败

```
1. 激活调试类技能（diagnose）分析原因
2. 如果是选错技能 → 重新路由
3. 如果是执行问题 → 激活重试类技能（loop/retry）
4. 3 次重试仍失败 → 暂停，向用户报告
```

### 全自动模式

```
1. 规划类技能拆分任务
2. 对每个子任务:
   a. 评估类技能评估影响
   b. 测试类技能写测试
   c. 执行类技能执行
   d. 重试类技能验证
3. 续航类技能管理上下文
4. 交接类技能生成报告
```

---

## 与项目级规则的关系

本技能是全局的，但项目级规则（如 CLAUDE.md 中的 GitNexus 强制规则）**优先级更高**：

- 如果项目规则要求"改代码前必须做 X"，则 X 不可跳过
- 本路由器的排序原则与项目规则冲突时，以项目规则为准
- 项目可以有自己的规则覆盖全局路由行为
