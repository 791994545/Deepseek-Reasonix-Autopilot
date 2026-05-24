# 2026-05-24-full-autonomous-demo.md

## 做了什么
在 D:\demo 下创建了 treemd.py — Markdown 目录树生成器 CLI 工具

## 执行流程
full-autonomous Standard 路径 Phase 0→5，共 25 步

## 遇到什么问题
1. watchdog.py GBK 编码问题 → 已修复（加 utf-8 stdout 重定向）
2. 无其他阻塞

## 如何修复的
watchdog.py 添加 sys.stdout = TextIOWrapper 解决 Windows 终端编码

## 下次如何预防
- Windows 环境下创建新脚本时预置 utf-8 编码处理
- 单文件 CLI 工具可直接走 Quick 路径

## 学到了什么（可泛化规则）
- Python 脚本在 Windows GBK 终端输出 Unicode 字符必须重定向 stdout
- write_file 写入 D: 盘路径需要 Python 而非 cmd 重定向
