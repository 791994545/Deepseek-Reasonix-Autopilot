---
name: opencode-self-evolution
description: 自我改进/持久化记忆/自动复盘/错误模式库
type: reference
scope: global
created: 2026-05-23
priority: medium
---
# 自我改进、持久化记忆、复盘

> **Reasonix 适配**: 此规则源自 OpenCode，已在 Reasonix 平台生效。

## 会话启动（每次）
1. 工具清单 → 扫描 `<available_tools>` 构建运行时映射
2. 加载错误模式库 (`opencode-error-patterns`)
3. 加载当前项目 `.reasonix/project-rules.md`
4. 检查 skill 版本快照与当前 `<available_skills>` 对比
5. 扫描 `<available_skills>` 匹配当前任务 → 自动加载匹配 skill
6. 记录：`[SessionStart] loaded {n} skills, {m} agents, {t} tools`

## 持久化
- 错误模式 → 追加到错误模式库
- 用户纠正 → 永久学习
- 命令/工具失败 → 记录错误模式

## 自动复盘（重要任务后）
1. 记录：做得好的、出错的、下次怎么做
2. 被用户纠正 → 写入 `opencode-error-patterns` 记忆
3. 命令失败 → 记录错误模式

## 技能缺口检测
启动任务时扫描 `<available_skills>` — 如果无匹配（<50%），检查是否可用工具完成，如果任务复杂且无匹配 → 触发 write-a-skill 创建新 skill

## 错误模式库
每条模式有 confidence 字段（0.0~1.0）：
- 初始：0.5 | 成功应用 → +0.1 | 用户纠正同模式 2 次 → -0.3
- 低于 0.2 自动归档为废弃
- 命令失败 → `[ErrorPattern] {command} → {error} → {fix} (conf:0.5)`
- 用户纠正 → `[Correction] {context} → {what user said} → {what to do next time}`
