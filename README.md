# Reasonix Autopilot — 全自动自进化开发系统

> **83 skills · AI-driven watchdog · Adaptive pipeline · Self-evolving feedback loop**
>
> 不只是配置集，而是一个**会自我进化的 AI 开发助理系统**。

---

## 📋 Overview · 概览

**Reasonix Autopilot** is a full-lifecycle autonomous development system built on top of the Reasonix platform. It transforms how AI assistants work — from single-shot question answering to **multi-phase, self-correcting, self-improving development pipelines**.

本系统不是简单的配置集合，而是一套完整的** AI 开发方法论**：从任务评估、技能路由、执行编排、多策略重试、合规审计，到复盘学习、权重回调，构成了一个完整的**自进化闭环**。

---

## 🌐 Cross-Platform · 跨平台

| Platform · 平台 | Status · 状态 | Notes · 说明 |
|----------------|--------------|-------------|
| **Windows** | ✅ 完整支持 | watchdog.py 纯 Python，含 win32 分支；Powershell 脚本兼容 |
| **Linux** | ✅ 完整支持 | 核心系统全兼容；额外支持 .sh 脚本 |
| **macOS** | ✅ 完整支持 | 同 Linux；额外支持 macOS 原生截图脚本 |

核心系统（watchdog + full-autonomous + skill-router）为纯 Python，**三平台通用**。个别技能含平台专用脚本（.sh / .ps1 / .swift），按需使用。

## 🔧 Dependencies · 依赖

```bash
# 查看完整依赖清单
cat requirements.txt

# 核心必需
# - Python 3.10+（watchdog 及技能脚本）
# - Git 2.30+（版本控制）

# 可选推荐
# - gitnexus CLI（改代码前影响分析）
# - gh CLI（GitHub 操作）
# - Node.js 18+（部分技能）

# 安装方式见 requirements.txt
```

## 📋 Overview · 概览

**Reasonix Autopilot** is a full-lifecycle autonomous development system built on top of the Reasonix platform. It transforms how AI assistants work — from single-shot question answering to **multi-phase, self-correcting, self-improving development pipelines**.

本系统不是简单的配置集合，而是一套完整的** AI 开发方法论**：从任务评估、技能路由、执行编排、多策略重试、合规审计，到复盘学习、权重回调，构成了一个完整的**自进化闭环**。

> **技能发现**：不维护硬编码技能列表。所有 83 个技能由 skill-router 在 Phase 0 动态扫描 `~/.reasonix/skills/` 自动发现加载。新增技能只需放入目录即可，无需修改任何配置文件。

## 🗂 Architecture · 架构

```
Reasonix Autopilot
│
├── AGENTS.md              ← 全局行为准则 + 启动脚本（中枢神经）
├── config.json            ← 平台配置（API Key 由环境变量注入）
│
├── 🔩 Watchdog Engine · 看门狗引擎
│   └── scripts/watchdog.py     ← 182 行守护进程
│        优雅终止 │ sessions 轮转 │ 复盘验证 │ 违例追踪
│
├── 🧠 Memory System · 记忆系统
│   ├── memory/global/          ← 9 条全局行为记忆（自动注入）
│   └── memory/experiences/     ← 跨会话经验积累
│
├── 📊 Feedback Loop · 反馈闭环
│   ├── error_patterns.json     ← 跨会话错误模式库
│   ├── skill_performance.json  ← 每次执行复盘记录
│   ├── routing_weights.json    ← error → 路由权重自动回调
│   └── project-rules.md        ← 项目规则模板（自动生成）
│
└── 📦 Skill Library · 技能库（83 技能）
    ├── 🔷 Core (19) · 内置核心
    │   └── full-autonomous · skill-router · compliance-guard · ralph-loop · etc.
    ├── 📐 Development · 开发类（20+）
    │   └── web-dev · mcp-builder · shadcn · react-best-practices · etc.
    ├── 🔒 Security · 安全类
    │   └── security-best-practices · compliance-check · compliance-guard
    ├── 🧪 Testing · 测试类
    │   └── tdd · dogfood · midscene-test · webapp-testing
    ├── 📄 Document · 文档类
    │   └── docx · pdf · pptx · obsidian · knowledge-capture · etc.
    └── 🔧 Utility · 工具类
        └── git-commit · github · debug · diagnose · handoff · etc.
```

---

## ✨ What Makes It Special · 核心特点

### 🏗️ Adaptive Pipeline · 自适应执行路径

No more "one size fits all". The system evaluates complexity at session start and auto-selects the optimal path.

不再一刀切。每次会话自动评估复杂度，选择最优执行路径：

| Path · 路径 | Complexity · 复杂度 | Flow · 流程 | Token Overhead |
|-------------|-------------------|-------------|----------------|
| **Quick** | ≤ 3 | Direct execution · 直接执行 | ~500 tokens |
| **Standard** | 4-7 | Phase 2a → 2.3 → 2.5 → 3 → 4 → 4.5 → 5 | ~3000 tokens |
| **Full** | ≥ 8 | Phase 2b → 2.3 → 2.5 → 3 → 4 → 4.5 → 5 | ~5000 tokens |

### 🔒 Defense-in-Depth · 纵深安全防御

```
API Key 环境变量注入 → compliance-guard 写操作审计 → watchdog 进程监控
```

Three layers of safety. Not a single line of secret is ever written to disk.

三层安全防护：API Key 不落盘、写操作有审计、进程级监控保底。

### 🔄 Self-Evolving Loop · 自进化闭环

```
Task → Execute → Review → skill_performance.json → error_patterns.json
  → routing_weights.json → skill priority adjusted → Next Task
```

Every mistake makes the system smarter. Every review feeds back into routing weights.

每次错误都在让系统变聪明，每次复盘都在优化下次路由。

### 🐙 Git-Native · 原生 Git 集成

- `gitnexus-auto`: Impact analysis before ANY code modification — know the consequences before you act
- `using-git-worktrees`: Isolate work in separate directories
- `finishing-a-development-branch`: Guide merge/PR/keep/discard decisions

改代码前先做影响分析、独立 worktree 隔离、分支收尾引导。

---

## ✅ System Test · 系统测试

| Test · 测试项 | Result · 结果 | Detail · 详情 |
|---------------|--------------|---------------|
| Skill discovery · 技能发现 | ✅ 10/10 | 83/83 skills, all with SKILL.md |
| API Key env var · 安全 | ✅ | `\${DEEPSEEK_API_KEY}` only, no plaintext |
| Watchdog · 看门狗 | ✅ 7/7 | graceful stop, state init, PID cleanup, log rotation, perf verification |
| Error pattern linkage · 错误关联 | ✅ | All entries have `skill_id` |
| Routing weights · 权重回调 | ✅ | Auto-generated from error patterns |
| skill_performance · 复盘 | ✅ | 2 records, full format |
| Experiences · 经验积累 | ✅ | 2 cross-session entries |
| Routing table · 路由表 | ✅ | 17 types + catch-all + weight reference |
| Execution rules · 执行规则 | ✅ | multi_edit + concurrent commands in HARD-GATE-TOOL |
| AGENTS.md config · 全局配置 | ✅ | Default-on mode + override rules + dynamic scanning |

## 🚀 Quick Start · 快速开始

### Prerequisites · 前置条件

- [Reasonix](https://reasonix.dev) platform installed
- A DeepSeek API key from [platform.deepseek.com](https://platform.deepseek.com/api_keys)

### Installation · 安装

```bash
# 1. Clone to your user directory
git clone https://github.com/791994545/reasonix-config.git ~/.reasonix

# 2. Set your API Key as environment variable
# Windows
setx DEEPSEEK_API_KEY sk-your-key-here

# Linux / Mac
# export DEEPSEEK_API_KEY="sk-your-key-here"

# 3. Launch Reasonix
reasonix code
```

That's it. The watchdog auto-starts. The complexity assessment auto-runs. Zero configuration needed.

零配置。克隆 → 设环境变量 → 启动，三步完成。

### First Run · 首次运行

The first time you start Reasonix with this config, the system will:

1. Start the watchdog process (background, checks every 60s)
2. Load error patterns and past experiences
3. Wait for your first message → evaluate complexity → auto-route

第一次启动时，看门狗自动启动、error_patterns/experiences 自动加载、复杂度自动评估。

---

## 📚 Skill Library · 技能库（83 Skills）

> 技能由 skill-router 动态扫描发现，无需硬编码列表。以下仅为常用技能示例。

### 🔷 Core Skills · 核心技能

自动编排在 Phase 0→5 流程中，无需手动加载。

| Skill · 技能 | Phase | Purpose · 用途 |
|-------------|-------|----------------|
| `brainstorming` | 2a/b | Requirements exploration · 需求探索 |
| `grill-me` / `grill-with-docs` | 2a/b | Stress-test the plan · 压力测试 |
| `zoom-out` | 2a/b | Architecture assessment · 架构评估 |
| `writing-plans` | 2a/b | Implementation planning · 实施计划 |
| `improve-codebase-architecture` | 2b | Architecture improvement · 架构优化 |
| `security-best-practices` | 2b/4 | Security review · 安全审查 |
| `ralph-planner` | 2.3 | Fine-grained task splitting · 细粒度任务拆分 |
| `ralph-loop` | 3 | Red-green-refactor cycle · 红-绿-重构循环 |
| `ralph` | 3.5 | Multi-strategy retry · 多策略重试 |
| `gitnexus-auto` | 3.2 | Impact analysis before coding · 改前影响分析 |
| `using-git-worktrees` | 2.5 | Worktree isolation · 工作区隔离 |
| `memory-manager` | 0/5 | Memory compression · 记忆压缩 |
| `no-confirm-silent` | 0.2 | Silent mode · 静默模式 |
| `proactive-agent` | 0.2 | Proactive suggestions · 主动建议 |
| `handoff` | 5.3 | Handoff documentation · 交接文档 |
| `finishing-a-development-branch` | 4.5 | Branch completion · 分支收尾 |
| `diagnose` | 4 | Debugging loop · 调试循环 |
| `self-improving` | 5.6 | Retrospective review · 复盘回顾 |

### Specialized Skills · 专项技能（64+）

| Category · 分类 | Skills · 技能 |
|----------------|---------------|
| **Web Fullstack** | `web-dev`, `frontend-design`, `shadcn`, `theme-factory`, `web-artifacts-builder`, `composition-patterns`, `react-best-practices` |
| **Backend / API** | `mcp-builder`, `redis-development`, `improve-codebase-architecture` |
| **CLI / Scripts** | `free-ride` |
| **Testing** | `tdd`, `dogfood`, `midscene-test`, `webapp-testing` |
| **Security** | `security-best-practices`, `compliance-check`, `compliance-guard` |
| **Document** | `docx`, `pdf`, `pptx`, `slides`, `xlsx`, `obsidian-markdown`, `obsidian-cli`, `notion-cli` |
| **Knowledge** | `knowledge-capture`, `meeting-intelligence`, `research-documentation`, `doc-coauthoring` |
| **Design** | `frontend-design`, `algorithmic-art`, `brand-guidelines`, `figma` |
| **Mobile** | `react-native-skills` |
| **Git** | `git-commit`, `github`, `gitnexus-auto/cli/guide/debugging/exploring/impact-analysis/refactoring` |
| **Configuration** | `write-a-skill`, `find-skills`, `customize-reasonix`, `skill-router` |
| **Utility** | `brainstorming`, `diagnose`, `executing-plans`, `spec-to-implementation`, `memory-hygiene`, `proactive-agent`, `triage`, `to-issues`, `to-prd`, `electron`, `screenshot`, `browser-auto` |

---

## 📁 File Structure · 文件结构

```
~/.reasonix/
├── AGENTS.md                         # Global behavior rules + boot script
├── config.json                       # Platform config (API key via env var)
├── error_patterns.json               # Cross-session error pattern library
├── routing_weights.json              # Error → routing weight callback
├── skill_performance.json            # Execution review records
├── project-rules.md                  # Auto-generated project rules template
├── .env.example                      # Environment variable template
├── .gitignore                        # Git exclusion rules
│
├── memory/
│   ├── global/                       # 9 global memory files (auto-injected)
│   └── experiences/                  # Cross-session learning experiences
│
├── scripts/
│   └── watchdog.py                   # Background watchdog daemon (182 lines)
│
├── sessions/                         # Session logs (excluded from Git)
│
└── skills/                           # 83 skill directories
    ├── full-autonomous/              # Core orchestration engine
    ├── skill-router/                 # Skill router
    ├── compliance-check/             # Gate compliance
    ├── compliance-guard/             # Real-time write audit
    ├── ralph-loop/                   # Red-green-refactor loop
    └── ... (79 more)
```

---

## 🔁 How the Loop Works · 闭环工作原理

```
                            ┌─────────────────────────────┐
                            │      User Message           │
                            │       用户消息                │
                            └──────────┬──────────────────┘
                                       │
                            ┌──────────▼──────────────────┐
                            │  STEP 3: Complexity Eval    │
                            │  复杂度评估 (1-10)            │
                            └──────┬───────┬───────┬──────┘
                                   │       │       │
                            Quick  │Standard│  Full │
                                   │       │       │
                            ┌──────▼───┐ ┌─▼───────▼──┐
                            │Direct Run │ │Phase 2→3→4 │
                            │直接执行    │ │标准/完整流程│
                            └──────┬───┘ └──────┬──────┘
                                   │            │
                            ┌──────▼────────────▼──────┐
                            │  Phase 3: Execute        │
                            │  gitnexus-auto (safety)  │
                            │  ralph-loop (retry)      │
                            └──────────┬───────────────┘
                                       │
                            ┌──────────▼───────────────┐
                            │  Phase 5: Review         │
                            │  skill_performance.json  │ ← Mandatory!
                            │  memory/experiences/     │ ← Mandatory!
                            │  error_patterns.json     │ ← +skill_id
                            └──────────┬───────────────┘
                                       │
                            ┌──────────▼───────────────┐
                            │  Watchdog verifies       │
                            │  skill_performance       │
                            │  written within 5 min    │
                            │  If not → violation      │
                            └──────────┬───────────────┘
                                       │
                            ┌──────────▼───────────────┐
                            │  Next session loads      │
                            │  updated error patterns  │
                            │  + experiences + weights │
                            └─────────────────────────┘
```

---

## 🔐 Security · 安全

| Measure · 措施 | Detail · 详情 |
|----------------|---------------|
| **API Key** | Environment variable `${DEEPSEEK_API_KEY}`, never written to disk |
| **Watchdog** | SIGTERM → 3s grace → SIGKILL, prevents zombie processes |
| **Session logs** | Auto-rotated >512KB, subagent logs >3 days deleted |
| **Compliance guard** | Every write operation is audited in real-time |
| **Error patterns** | Now include `skill_id` for traceability |
| **Git** | `.gitignore` excludes sessions/, usage.jsonl, state.json, .bak |

---

## 🗺 Roadmap · 未来规划

- [ ] Auto-adjust routing weights from error pattern confidence (hard threshold already in place)
- [ ] Multi-strategy retry on phase failure (ralph skill ready)
- [ ] Project-specific rule auto-detection (template already exists)

---

## 📝 License · 许可证

MIT

---

## 🙏 Credits · 致谢

- Built on the [Reasonix](https://reasonix.dev) platform
- Skill catalog inspired by OpenCode ecosystem
- Ralph-loop methodology from the ralph development framework
