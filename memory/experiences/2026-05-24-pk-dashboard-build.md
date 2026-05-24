# PK: Skill Route Dashboard 构建复盘

## 做了什么
按 pk-prompt.md 构建了完整的 Skill Route Dashboard Web 应用：
- Flask 后端（6 个页面 + 6 个 API 端点）
- 7 个 Jinja2 模板（base + 6 功能页）
- CSS 深色主题 + 4 个 JS 交互脚本（SortableJS/Chart.js/HTMX）
- 29 个 pytest 测试（单元测试 + 集成测试）
- 完整 README 文档

## 使用了什么数据源
1. skills/*/SKILL.md - 实时扫描 113 个技能
2. rules/*-routing-*.md - 路由表 markdown 解析
3. skill_performance.json - mtime 缓存读取
4. error_patterns.json - confidence 排序
5. routing_weights.json - 读写（原子写入）
6. memory/experiences/*.md - 时间线展示
7. git log - 提交记录（通过 git -C 命令）

## 遇到什么问题
1. description 解析：_extract_description 函数 frontmatter 解析逻辑 bug（初始在第一个 --- 就 break 了）
2. Chinese bytes：Python 3 不支持 bytes 中文字面量
3. 测试 import 路径：测试在 project/tests/ 下需添加 sys.path
4. Windows Flask debug 重载器导致路由 404

## 如何解决的
1. 重写 frontmatter 解析逻辑：先找 --- 进入，再找 --- 退出
2. 用 decode() 替代 bytes 字面量
3. conftest.py 中添加 sys.path.insert
4. 用 test_client 验证路由正确性

## 下次注意
- Flask debug=True 在 Windows 不兼容 run_background
- 测试中用 decode() 而非 bytes 字面量检查中文内容
