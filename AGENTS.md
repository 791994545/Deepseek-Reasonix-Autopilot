# Reasonix — 全局行为规则

## 启动

全自动模式默认开启。触发机制见 `memory/global/auto-trigger.md`。
工作流定义见 `skills/full-autonomous/SKILL.md`。

## 文件工具优先

- 读文件用 `read_file`、`search_content`、`glob`
- 写文件用 `write_file`、`edit_file`、`multi_edit`
- 不要用 `run_command` 替代文件工具（echo/cat/sed/dir 等）
- 不要用 `cd` — 用 `--prefix`、`-C`、`cwd` 等参数

## 运行命令

- 开发服务器/watch 命令用 `run_background`
- 单次命令（测试/构建/lint/typecheck）用 `run_command`
- 独立命令同轮次并发（互不依赖的同时发）

## 编辑

- 多文件跨文件修改用 `multi_edit`（批量验证，失败全回滚）
- 单文件修改用 `edit_file`（SEARCH/REPLACE）
- 编辑前先 `read_file` 确认内容

## 关键文件

| 文件 | 用途 |
|------|------|
| `memory/global/auto-trigger.md` | 全自动触发规则（HIGH PRIORITY） |
| `skills/full-autonomous/SKILL.md` | 工作流引擎 |
| `config.json` | 平台配置 |
| `error_patterns.json` | 错误模式库 |
| `skill_performance.json` | 执行记录 |
