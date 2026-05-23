---
name: memory-manager
description: Reasonix 记忆管理 — 用 remember/forget 工具管理全局和项目级记忆
---

> **Reasonix 适配版** — OpenCode 的原 `~/.opencode/memory/` 文件系统方案已替换为 Reasonix 的 `remember`/`forget` 工具调用

# Memory Manager — Reasonix 版

## 记忆系统架构

Reasonix 使用 `remember` 工具存储结构化记忆，分为两层：

| 层级 | 范围 | 注入时机 |
|------|------|----------|
| **Global** | 跨项目共享 | 每次 `/new` 或启动注入到 system prompt |
| **Project** | 当前项目 | 每次会话启动加载 |

## 记忆类型

| 类型 | 用途 | 示例 |
|------|------|------|
| `user` | 用户角色/偏好/技能 | 偏好简洁回答、擅长 Python |
| `feedback` | 纠正或确认的方法 | 某 API 的正确用法 |
| `project` | 项目事实/决策 | 技术栈、架构决策、约定 |
| `reference` | 外部系统参考 | 第三方文档速查 |

## 操作方式

### 保存记忆
```
remember(type="reference", scope="global", name="...",
        description="≤150 字摘要",
        content="Markdown 正文",
        priority="medium")
```

### 读取记忆
```
recall_memory(name="...", scope="global")
```

### 删除记忆
```
forget(name="...", scope="global")
```

## 最佳实践

1. **高频规则用 priority:high** — 每次启动注入 prompt
2. **描述 ≤150 字** — 在 MEMORY.md 中一目了然
3. **内容用 Markdown** — 支持结构化格式
4. **自动过期** — 设置 `expires:"project_end"` 项目结束时自动清理
