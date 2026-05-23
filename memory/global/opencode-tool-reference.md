---
name: opencode-tool-reference
description: OpenCode→Reasonix 工具映射表 — Read→read_file, Bash→run_command, Task→explore/task-executor, Question→ask_choice
type: reference
scope: global
created: 2026-05-23
priority: high
---
# Reasonix 工具参考表（OpenCode→Reasonix 映射）

## 工具映射

| OpenCode 原名 | Reasonix 工具 | 何时用 | 何时不用 |
|--------------|--------------|--------|----------|
| `Read` | `read_file` | 读文件/目录/图片 | 搜索内容（用 search_content） |
| `Write` | `write_file` | 创建新文件/完全覆盖 | 部分编辑（用 edit_file） |
| `Edit` | `edit_file` | 替换文件中指定字符串 | 创建新文件（用 write_file） |
| `SearchReplace` | `edit_file` | 同上 | — |
| `Glob` | `glob()` / `search_files()` | 按文件名模式搜索 | 内容搜索（用 search_content） |
| `Grep` | `search_content` | 按模式搜索文件内容 | 按文件名查找（用 glob） |
| `Bash` | `run_command` | 终端命令（git/pip/npm/python） | 文件读写（用 read_file/write_file） |
| `Task`（子代理） | `explore`（只读） / `task-executor`（读写） | 复杂任务隔离执行 | 简单命令（用 run_command） |
| `Skill` | `run_skill` | 加载匹配任务的专用指令 | 已加载的 skill |
| `Question` | `ask_choice` | 需要用户决策时 | 自己能判断的事 |
| `TodoWrite` | `todo_write` | 3+步的多步任务追踪 | 单命令或信息查询 |
| `WebSearch` | `web_search` | 实时信息、当前事件 | 访问特定 URL（用 web_fetch） |
| `WebFetch` | `web_fetch` | 抓取特定 URL 内容 | 通用搜索（用 web_search） |
| `DirectoryTree` | `directory_tree` | 递归列出目录结构 | — |
| `ListDirectory` | `list_directory` | 列出单层目录 | — |
| `GetFileInfo` | `get_file_info` | 查看文件属性 | — |
| `DeleteFile` | `delete_file` | 删除文件 | — |
| `MoveFile` | `move_file` | 移动/重命名文件 | — |
| `CopyFile` | `copy_file` | 复制文件 | — |

## 常用组合模式（Reasonix 版）

- **全栈功能**: brainstorming → skill-router → zoom-out(glob+search_content+read_file) → task-executor(并行) → run_command(测试) → compliance-guard(审计)
- **调试循环**: diagnose(search_content+read_file+run_command) → edit_file(修) → run_command(验) → 记录到 opencode-error-patterns
- **代码探索**: explore(隔离子代理) → glob+search_content+read_file → 返回摘要
- **后台服务**: run_background → wait_for_job
- **全自动开发**: full-autonomous → Phase 0→5（内部自动选工具）
