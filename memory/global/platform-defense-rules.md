---
name: platform-defense-rules
description: Windows/Python/Flask 平台防御规则 — 从 PK 构建 5 个 Bug 中提取
type: reference
scope: global
created: 2026-05-24
priority: medium
---
# 平台防御规则（从 PK 构建实战提取）

## 规则一览
| 场景 | 规则 | 来源 Bug |
|------|------|---------|
| Windows subprocess | 不用 text=True，手动 decode("utf-8", errors="replace") | GBK 编码 stdout=None |
| Flask 验证 | 用 test_client 而非 curl，debug=False 避免重载 404 | Flask reloader 路由丢失 |
| Python 测试路径 | tests/ 子目录 → conftest.py 加 sys.path.insert | ModuleNotFoundError |
| Python bytes 中文 | 用 .decode() 替代 b"中文" 字面量 | SyntaxError |
| YAML frontmatter | 状态机解析（跳过首 --- → 读内容 → 遇二 --- 退出） | description 全空 |

## 完整修复闭环
任何测试/运行中发现的 Bug → 修复后立即：
1. 追加到 error_patterns.json（含 skill_id/phase/confidence/fix/prevention）
2. 更新 routing_weights.json（按 confidence 设 penalty）
3. 追加前查重 → 有则合并提升 confidence，无则新增
