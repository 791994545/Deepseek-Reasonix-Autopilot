# Deepseek-Reasonix Autopilot v2.0

> **113 技能 · 执行引擎驱动 · 全自动闭环 · 零弹窗**
>
> 你只管说「帮我做 X」，剩下的事系统自动跑完。

---

## 这是什么

一套会自己跑的全自动开发系统。放在 `~/.reasonix/` 下，Reasonix 启动时自动加载。

**不需要触发词。** 你说「帮我做 X」→ 全自动走流程 → 给你看成果。你说「怎么用 React」→ 直接回答，不跑流程。

## 三步开始

```bash
git clone git@github.com:791994545/reasonix-config.git ~/.reasonix
setx DEEPSEEK_API_KEY sk-your-key-here
reasonix code
```

完了。看门狗自动启动、错误库自动加载、复杂度自动评估。

## 自动流程

```
你说「帮我做XXX」
      ↓
  复杂度评估 (1-10) → Quick / Standard / Full
      ↓
  技能装配 → 查路由表，加载对应技能
      ↓
  策略选择 → 按任务类型选策略:
              构建 → 设计驱动
              审计 → 并行探索
              修Bug → 诊断驱动
              脚本 → 精简设计
      ↓
  编码 → 测试 → 修复
      ↓
  成果展示 → 写记录 → 压缩记忆 → 闭环
```

每次任务结束你会看到：

```
📦 完成
──────────────────────────────
任务: 创建文件统计工具
路径: Quick  耗时: 0分32秒
产出: 📄 filecounter.py — 递归统计目录文件类型
结果: ✅ 测试通过
```

## 引擎架构

```
run_pipeline.py      执行引擎（自动调用，无需手动）
watchdog.py          看门狗 + 自动进化引擎（后台静默）
compact_memories.py  记忆压缩（自动裁剪四文件到上限）
```

## 文件结构

```
~/.reasonix/
├── AGENTS.md                    全局行为规则
├── SKILL.md                     全自动流程定义
├── error_patterns.json          错误模式库（自动积累）
├── routing_weights.json         路由权重（自动回调）
├── skill_performance.json       执行记录（每次复盘）
│
├── skills/                      113 个技能
│   ├── full-autonomous/         核心编排引擎
│   │   ├── scripts/
│   │   │   ├── run_pipeline.py      执行引擎
│   │   │   ├── watchdog.py         看门狗 + 自动进化
│   │   │   └── compact_memories.py 记忆压缩
│   │   ├── rules/                   路由表/门禁/自检
│   │   └── docs/                    执行流程/扩展机制
│   └── ...
│
├── memory/
│   ├── global/                   全局记忆（自动注入）
│   └── experiences/              经验积累（每次任务后写）
│
└── config.json                   平台配置
```

## 安全

- API Key 用环境变量 `${DEEPSEEK_API_KEY}`，不写盘
- 看门狗 60 秒巡检，违例自动记录
- 记忆文件自动压缩，不膨胀
- 会话日志自动轮转

## License

MIT
