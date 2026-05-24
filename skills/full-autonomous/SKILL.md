---

name: full-autonomous
description: Deepseek-Reasonix Autopilot v2.0 — 执行引擎驱动，全自动，无需手动命令
version: 2.0.0

---

<MANDATORY_EXECUTION_SCRIPT>

本 SKILL.md 定义我在 full-autonomous 模式下的行为。
所有机械步骤由引擎自动执行，我不需要敲任何命令。

## 引擎架构

```
run_pipeline.py          ← 我自动调用，无需用户介入
  init      → 看门狗 + state + snapshot + top-15
  pre-phase → 前置门禁验证
  post-phase  → 后置验证 + 更新 state
  complete  → 压缩 + 停看门狗 + 清理

watchdog.py              ← init 时自动启动
  协议检查 + 自动进化引擎（检测修复事件→入库）

compact_memories.py      ← complete 时自动调用
  四文件裁剪到上限
```

## 我的自动行为

### 会话启动时
自动调用 `run_pipeline.py init`，然后等待用户输入。

### 用户给出任务后
1. 输出 `[Auto] === 启动 ===`
2. 评估复杂度 (1-10) + 匹配类型 + 确定路径
3. 自动调用 `run_pipeline.py post-phase 0`

### Phase 转换
自动调用 pre-phase N → 我做推理 → 自动调用 post-phase N

| Phase | 我做推理 |
|-------|---------|
| 0 | 复杂度 + 类型 + 路径 |
| 1 | 查路由表，加载技能包 |
| 2a/2b | brainstorming → grill → H-3 → zoom-out → plan |
| 3 | 编码（遵守工具规则） + 测试 |
| 4 | 测试 → diagnose → 修复 |
| 5 | 自我回顾 + 写 skill_performance + experiences + 进化建议 |

### 任务完成时
自动调用 `run_pipeline.py complete`

## 路径

| 条件 | 路径 | 流程 |
|------|------|------|
| Quick (≤3) | skip Phase 1-2 | init → 3 → complete |
| Standard (4-7) | 标准 | init → 1→2a→3→4→complete |
| Full (≥8) | 完整 | init → 1→2b→3→4→complete |

Override: "直接回答"→Quick / "全自动"→Full

## 工具选择规则（Phase 3 编码时遵守）

| 场景 | 工具 |
|------|------|
| 读 1-5 文件 | `read_file` 并发 |
| 读 6-10 文件 | 拆批或 `explore` |
| 理解架构 | `explore` |
| ≥10 文件批量 | `explore` 分批 |
| 编码/修改 | `gitnexus-auto` → `multi_edit`（禁止串行 edit_file） |
| 批量编辑 | `multi_edit`（验证后写，失败回滚） |
| 独立命令 | `run_command` 并发 |

## 引用文件

| 路径 | 内容 |
|------|------|
| `scripts/run_pipeline.py` | 执行引擎 |
| `scripts/watchdog.py` | 看门狗 + 自动进化 |
| `scripts/compact_memories.py` | 记忆压缩 |
| `rules/01a-routing-quick-index.md` | 路由索引 |
| `rules/01-skill-routing-table.md` | 完整路由表 |
| `rules/03-output-format.md` | 输出模板 |
| `docs/extension-mechanisms.md` | 扩展机制 |
| `templates/hidden-needs-rules.json` | H-3 规则库 |
