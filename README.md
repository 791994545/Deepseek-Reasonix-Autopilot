# Reasonix — 全自动开发系统

> 五阶段全自动开发剧本 — Phase 0→5，自适应路径 + GitNexus 影响分析 + 看门狗进程监控 + 自学习闭环

## 快速安装

```bash
# 1. 克隆到用户目录
git clone https://github.com/YOUR_USER/reasonix-config.git ~/.reasonix

# 2. 设置 API Key（从 https://platform.deepseek.com/api_keys 获取）
setx DEEPSEEK_API_KEY sk-your-key-here
# 或：系统设置 → 环境变量 → 新建 DEEPSEEK_API_KEY

# 3. 启动 Reasonix
reasonix code
```

## 系统架构

```
~/.reasonix/
├── AGENTS.md                     # 全局行为准则 + 启动脚本
├── config.json                   # 平台配置（API Key 由环境变量注入）
├── error_patterns.json           # 跨会话错误模式库
├── routing_weights.json          # error→confidence→路由权重自动回调
├── skill_performance.json        # 每次执行的复盘记录
├── project-rules.md              # 项目规则模板（自动生成）
├── .env.example                  # 环境变量示例
├── memory/
│   ├── global/                   # 9 条全局记忆（自动注入无需手动加载）
│   └── experiences/              # 跨会话学习经验
├── scripts/
│   └── watchdog.py               # 外部看门狗（PID 清理/日志轮转/复盘验证）
├── sessions/                     # 会话日志（.gitignore 排除）
└── skills/                       # 83 个技能
    ├── full-autonomous/          # 核心全自动编排引擎
    ├── skill-router/             # 技能路由器
    ├── compliance-check/         # 合规检查（Gate 门禁）
    ├── compliance-guard/         # 写操作实时审计
    ├── gitnexus-auto/            # 代码修改前影响分析
    ├── ralph-loop/               # 红-绿-重构循环
    ├── ralph-planner/            # 细粒度任务拆分
    ├── ralph/                    # 多策略重试
    └── ... (75+ 更多)
```

## 全自动模式

**默认开启**，无需触发词。每次会话自动执行复杂度评估：

| 路径 | 复杂度 | 流程 |
|------|--------|------|
| Quick | ≤3 | 直接执行（~500 token 开销）|
| Standard | 4-7 | Phase 2a→2.3→2.5→3→4→4.5→5 |
| Full | ≥8 | Phase 2b→2.3→2.5→3→4→4.5→5 |

**覆盖规则**:
- `直接回答` / `快速回答` → 强制 Quick
- `全自动` / `深度分析` → 强制 Full

## 核心特性

| 特性 | 说明 |
|------|------|
| 🏗️ 自适应路径 | Quick/Standard/Full 三级，按复杂度自动分流 |
| 🔒 安全体系 | API Key 环境变量注入，看门狗优雅终止 |
| 🛡️ 双重合规 | compliance-check（门禁）+ compliance-guard（实时审计）|
| 🔄 自学习闭环 | skill_performance 强制写 + 看门狗自动验证 |
| 📊 权重回调 | error.confidence → routing_weights.json → 技能自动降级 |
| 🧵 并行执行 | 读文件并发、multi_edit 批量写入、独立命令并发 |
| 🐙 Git 集成 | git-commit 技能、worktree 隔离、分支收尾 |
| 🔍 代码安全 | gitnexus-auto 影响分析（改前知后果）|

## 技能清单（19 个内置）

`brainstorming`, `grill-me`, `grill-with-docs`, `zoom-out`, `writing-plans`, `improve-codebase-architecture`, `security-best-practices`, `diagnose`, `self-improving`, `ralph-planner`, `ralph-loop`, `ralph`, `no-confirm-silent`, `proactive-agent`, `handoff`, `memory-manager`, `gitnexus-auto`, `using-git-worktrees`, `finishing-a-development-branch`

## 许可证

MIT
