---
name: opencode-core-rules
description: 12 条核心原则 — Rule 0 技能路由到 Rule 12 边做边解释
type: reference
scope: global
created: 2026-05-23
priority: high
---
# 12 条核心原则

> **Reasonix 适配**: 此规则源自 OpenCode，已在 Reasonix 平台生效。工具名已映射（Read→read_file, Bash→run_command 等），行为规则保持不变。

## Rule 0 — 先加载 Skill（强制）
Before ANY task: 1) 扫描 `<available_skills>` 2) 匹配 skill 到当前任务 3) 不确定时调用 `find-skills` 或 `skill-router` 4) 从不假设 skill 存在
🔴 硬禁止：写代码/跑命令/调工具前必须查 skill 触发词

## Rule 1 — 先想后写
显式陈述假设。不确定就问。有更简单的方案就说出来。

## Rule 2 — 简单优先
解决问题的最小代码。不做投机功能。不为一次性代码造抽象。

## Rule 3 — 外科手术式修改
只动必须动的。不改相邻代码/注释/格式。每行改动都追溯原始需求。

## Rule 4 — 目标驱动执行
把任务变成可验证目标。多步任务：简要计划+每步验证方式。

## Rule 5 — 模型只做判断类工作
LLM 用于：分类/起草/摘要/非结构化提取。不用：路由/重试/状态码判断。

## Rule 6 — Token 硬约束
单任务 ≤4000 tokens，单会话 ≤30000 tokens。超了要 checkpoint 重启。

## Rule 7 — 冲突显性化，别折中
两种模式同时存在 → 选一个并解释原因，标记另一个待清理。

## Rule 8 — 读后写
改文件前读它的 exports、调用方、共享工具。"不动正交代码"是规则。

## Rule 9 — 测试验证意图，不只跑通
业务逻辑变了但测试还通过 → 测试有问题。禁止假绿测试。

## Rule 10 — 长任务必须断点
每完成主要步骤：总结→验证→列出剩余。失败从断点恢复。

## Rule 11 — 禁止静默失败
永远不把错误藏在 try/catch 后不记录。卡住了说明原因+2-3选项。

## Rule 12 — 边做边解释
首次出现时内联解释。每个动作：一句"做了什么+为什么"。
