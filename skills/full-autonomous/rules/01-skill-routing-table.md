# 技能路由表（冻结版）

> 🧊 **此表已冻结**。2026-05-23 最终稳定版本。
> 以后新增技能**不需要**修改此表。新技能会被 skill-router 通过 SKILL.md 的 description 关键词自动发现匹配。
> 如有匹配不准，调整新技能的 description 字段即可，不动此文件。

## 路由规则

| 任务类型 | 触发关键词 | Core（所有路径） | Enhanced（Standard+） | Extended（Full 仅） | Testing（Standard+） |
|----------|-----------|-----------------|----------------------|--------------------|---------------------|
| **web-frontend** | 页面/前端/UI/landing/网站/界面 | frontend-design, web-dev | shadcn, composition-patterns, theme-factory, brand-guidelines | figma, web-artifacts-builder, frontend-skill | webapp-testing, web-design-guidelines, midscene-test |
| **web-fullstack** | 全栈/web应用/前后端 | frontend-design, web-dev, mcp-builder, security-best-practices, using-git-worktrees, finishing-a-development-branch | shadcn, improve-codebase-architecture, react-best-practices, ralph-planner, ralph-loop, ralph, gitnexus-auto | figma, composition-patterns, redis-development | webapp-testing, tdd, midscene-test, dogfood |
| **backend-api** | 后端/API/服务/接口/MCP | mcp-builder, security-best-practices, improve-codebase-architecture, using-git-worktrees, finishing-a-development-branch | redis-development, tdd, ralph-planner, ralph-loop, ralph, gitnexus-auto | gitnexus-impact-analysis, gitnexus-refactoring | webapp-testing, diagnose |
| **cli-tool** | 命令行/CLI/脚本/tool | tdd, writing-plans, using-git-worktrees, finishing-a-development-branch | improve-codebase-architecture, gitnexus-exploring, ralph-planner, ralph-loop, ralph, gitnexus-auto | diagnose, full-autonomous | tdd, diagnose |
| **data-processing** | 数据/Excel/CSV/报表 | xlsx, pdf, markdown-convert | docx, internal-comms | doc-coauthoring, research-documentation | diagnose |
| **mobile-app** | 移动端/React Native/手机 | react-native-skills, tdd | frontend-design, web-design-guidelines | composition-patterns, improve-codebase-architecture | webapp-testing, midscene-test |
| **browser-auto** | 浏览器/爬虫/自动化/抓取 | agent-tars, screenshot | electron, midscene-test | diagnose, memory-manager | midscene-test |
| **desktop-app** | 桌面/Electron/原生 | electron, agent-tars, screenshot | tdd, diagnose | memory-manager, self-improving | webapp-testing |
| **git-operation** | Git/提交/PR/Issue/推送 | git-commit, github, github-ops | gitnexus-auto, finishing-a-development-branch, github-contributor | using-git-worktrees | — |
| **code-packaging** | 打包代码/安全扫描/分发包 | repomix-safe-mixer | repomix-unmixer | — | — |
| **code-quality** | QA/测试/代码质量 | qa-expert | tdd, dogfood | webapp-testing | midscene-test |
| **deep-research** | 深度研究/竞品分析/市场调研 | deep-research, fact-checker | competitors-analysis, product-analysis | financial-data-collector | — |
| **skill-creation** | 技能创建/验证/打包 | skill-creator, skills-search | write-a-skill | — | skill-reviewer |
| **prompt** | Prompt 优化/评估 | prompt-optimizer | promptfoo-evaluation | — | — |
| **media** | 视频/音频/截图/图标 | youtube-downloader, video-comparer, twitter-reader | cli-demo-generator, llm-icon-finder, capture-screen | — | — |
| **i18n** | 国际化/本地化 | i18n-expert | — | — | — |
| **transcript** | 语音转录/字幕修正 | transcript-fixer | — | — | — |
| **network-debug** | 网络诊断/Cloudflare/SSH | debugging-network-issues, cloudflare-troubleshooting, tunnel-doctor | — | — | — |
| **data-collection** | 数据采集/爬虫/金融 | scrapling-skill, financial-data-collector, douban-skill | feishu-doc-scraper | — | — |
| **product-analysis** | 竞品分析/产品调研 | competitors-analysis, product-analysis | — | — | — |
| **excel** | Excel 操作/自动化 | excel-automation | — | — | — |
| **macos** | macOS 系统工具 | macos-cleaner | — | capture-screen | — |
| **china-tools** | 中国区特有工具 | gangtise-copilot, ima-copilot | daymade-docs | — | — |
| **github-contrib** | GitHub 贡献策略 | github-contributor | — | — | — |
| **repomix** | Repomix 解包/分析 | repomix-unmixer | repomix-safe-mixer | — | — |
| **documentation** | 文档/知识库/Wiki/说明/API文档生成 | doc-coauthoring, api-docs-generator, obsidian-markdown, internal-comms | json-canvas, obsidian-bases, knowledge-capture | research-documentation, meeting-intelligence | — |
| **design-system** | 设计系统/组件库/shadcn | shadcn, composition-patterns, brand-guidelines | theme-factory, figma, web-artifacts-builder | react-best-practices, web-design-guidelines | webapp-testing |
| **algorithmic-art** | 算法艺术/生成艺术/p5.js | algorithmic-art, prototype | frontend-design, theme-factory | — | — |
| **config-tool** | 配置/技能/插件/MCP | write-a-skill, find-skills, customize-reasonix | skill-router, self-improving | memory-manager, handoff | — |
| **testing** | 测试/QA/E2E/单元测试 | tdd, midscene-test, webapp-testing | dogfood, diagnose, full-autonomous | self-improving, memory-hygiene | — |
| **presentation** | 演示/PPT/幻灯片 | slides, pptx, theme-factory | brand-guidelines, internal-comms | doc-coauthoring | — |
| **analysis** | 分析/评估/审查/对比/diff/状态 | self-improving, zoom-out | diagnose, brainstorming | grill-me, writing-plans | diagnose |
| **other** | 其他/未分类 | self-improving, zoom-out, using-git-worktrees, finishing-a-development-branch, ralph-planner, ralph-loop, ralph, gitnexus-auto | diagnose, brainstorming | grill-me, writing-plans | diagnose |

## 子代理类型选择

| 任务特征 | 子代理类型 |
|----------|-----------|
| 只读探索（搜索/理解代码） | `explore` |
| 含写操作（生成代码/修改文件） | `task-executor`（隔离 subagent，读写全权限） |
| 复杂多步骤（需要独立编排） | `full-autonomous` 编排 + `task-executor` 执行 |
| 先探索后修改（需要上下文传递） | `explore`（单向分析）→ `task-executor`（串行执行）|

## 通用流程技能

以下技能适用于**所有涉及代码开发的 task 类型**，由 full-autonomous 的 Phase 0→5 自动编排：

| 阶段 | 技能 | 说明 |
|------|------|------|
| Phase 0 | `memory-manager`（启动压缩检测）| 启动时检查记忆文件是否需压缩 |
| Phase 0 | `no-confirm-silent` / `proactive-agent` | 根据用户意图自动加载（silent=少确认 / proactive=主动建议）|
| Phase 2.3 | `ralph-planner` | 粗粒度计划后拆分为细粒度子任务 + 依赖编排 |
| Phase 2.5 | `using-git-worktrees` | 开始实现前创建隔离 worktree |
| Phase 3 | `gitnexus-auto` | 代码修改前全流程影响分析（索引→上下文→影响→改→检测）|
| Phase 3 | `ralph-loop` + `ralph` | Standard/Full 路径的红-绿-重构循环 + 多策略重试 |
| Phase 4→5 | `finishing-a-development-branch` | 完成合并/PR/保留/丢弃决策 |
| Phase 5 | `handoff` | 任务未完成时生成交接文档 |
| Phase 5 | `memory-manager`（结束清理）| session 结束时清理记忆 |
| Phase 5 | `self-improving` | 反思整理→记录错误/学习/→关联→简化→提升→技能提取→回顾 |
| Phase 5 | `memory-hygiene` | 向量记忆审计清理（LanceDB 臃肿时）|
| Phase 3 | `tdd` | RED-GREEN-REFACTOR 测试驱动开发（与 ralph-loop 配合）|
| Phase 4 | `dogfood` | 系统性探索测试 web 应用（UX bug/功能问题）|
| 全 Phase | `compliance-check` | 每次 Phase 出口前验证合规性 |

加载 full-autonomous 时，根据复杂度路径自动决定是否调用：
- **Quick** — 仅调用 memory-manager、no-confirm-silent/proactive-agent
- **Standard** — 按需询问（worktree、finish-branch、handoff）
- **Full** — 强制调用所有（ralph-planner → worktree → gitnexus-auto → ralph-loop → finish-branch）

## 优先级规则

1. 技能路由器返回的技能按 Core → Enhanced → Extended → Testing 顺序加载
2. 同一技能不重复加载
3. 如果某个技能在 `<available_skills>` 中不存在 → 标记技能缺口 → Phase 0 触发 `write-a-skill`
4. 相同任务类型的多次执行 → `self-improving` 学习后优化技能组合权重
5. **权重惩罚**：加载前查 `routing_weights.json`，weight_penalty > 0 的技能自动降级（优先用备选列表中权重低的技能）

### 权重参考
| weight_penalty | 含义 | 路由行为 |
|---------------|------|---------|
| 0.0 | 正常 | 按原优先级加载 |
| 0.1 | 轻度违规 | 降级到备选列表末尾 |
| 0.2 | 中度违规 | 除非别无选择，否则不加载 |
| 0.3 | 严重违规 | 完全排除（直到人工确认修复）|