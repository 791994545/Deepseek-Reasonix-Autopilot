---
name: find-skills
description: 查找和发现已安装的 Reasonix 技能 — 按关键词/分类搜索技能，查询技能能做什幺
---

> **Reasonix 适配版** — 原 OpenCode 版基于 `npx skills` CLI，Reasonix 版使用内置技能清单 + `run_skill`

# Find Skills — Reasonix 版

## 如何查找技能

### 方法 1: 查技能目录清单

当前已安装的所有技能：

```
~/.reasonix/skills/
├── full-autonomous/    五阶段全自动开发
├── brainstorming/      创意/设计前必用
├── diagnose/           严格调试循环
├── skill-router/       技能路由器
├── writing-plans/      实施计划
├── executing-plans/    执行计划
├── grill-me/           方案压力测试
├── caveman/            极简模式
├── task-executor/      隔离子代理编码执行
├── compliance-guard/   合规看门狗审计
├── zoom-out/           全局代码视角
├── git-commit/         规范提交
├── ...                 共 80 个技能
```

完整清单见全局记忆 `opencode-skill-catalog`。

### 方法 2: 按关键词搜索

根据用户需求匹配技能：

| 需求 | 相关技能 |
|------|---------|
| 写代码/建项目 | full-autonomous, web-dev, prototype, tdd |
| 修 bug | diagnose, zoom-out, grill-me |
| 设计/创意 | brainstorming, frontend-design, figma |
| 文档/PPT | docx, pdf, pptx, slides, doc-coauthoring |
| Git/GitHub | git-commit, github, gitnexus-* |
| 测试 | tdd, webapp-testing, midscene-test, dogfood |
| 安全 | security-best-practices, compliance-check |
| 知识管理 | knowledge-capture, meeting-intelligence, obsidian-* |
| 前端 | shadcn, react-best-practices, composition-patterns |
| 数据库 | redis-development, xlsx |
| 自动化 | agent-tars, electron, screenshot |

### 方法 3: 直接试

不确定直接 `run_skill({name:"<skill-name>", arguments:"<task>"})`。

## 安装新技能

Reasonix 没有外部技能市场。创建新技能用：

```
install_skill(name="my-skill", description="...", body="...")
```

或直接写入 `~/.reasonix/skills/<name>/SKILL.md`。
