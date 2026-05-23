# 2026-05-23: OpenCode 交叉验证方法论

## 场景
全自动分析 OpenCode 优化版 vs Reasonix 版，找出剩余差距。

## 有效方法
1. 启动 OpenCode CLI 让其自己跑 full-autonomous 分析 Reasonix
2. 将 OpenCode 的分析结果与磁盘实际状态逐条核对
3. 发现 OpenCode 指出的 "缺失" 有些其实是它用了旧快照

## 下次遇到同类问题
先用 `run_command` 核对磁盘实际状态，再判断 OpenCode 的报告是否过时。
