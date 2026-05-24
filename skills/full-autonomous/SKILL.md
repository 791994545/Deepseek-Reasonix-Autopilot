---
name: full-autonomous
description: 全自动执行引擎 — Phase 0→5 工作流
version: 3.0.0
---

# Full-Autonomous v3.0

## Phase 流程

```
Phase 0: 评估 → Phase 1: 调查 → Phase 2: 设计 → Phase 3: 编码 → Phase 4: 验证 → Phase 5: 收尾
```

每个 Phase 做推理，不调 `run_pipeline.py`（除非引擎脚本自己有用）。

---

## Phase 0 — 启动评估（每次任务型消息必须执行）

1. 输出 `[Auto] === 启动 ===`
2. 评估复杂度（1-10）：
   - ≤3 = Quick（单文件小改）
   - 4-7 = Standard（多文件，有风险但可控）
   - ≥8 = Full（架构重组、跨语言改动）
3. 匹配 task_type（code-build / code-audit / bug-fix 等）
4. 确定路径 → 直接进入下一个 Phase（不卡审批）
5. 如果用户说"全自动" → 强制 Full

**输出**: `[Auto] === 启动 ===` + 复杂度 + 路径

---

## Phase 路径

| 路径 | 流程 | 适用 |
|------|------|------|
| **Quick** | Phase 0→3→4→5 | ≤3 复杂度 |
| **Standard** | Phase 0→1→2→3→4→5 | 4-7 复杂度 |
| **Full** | Phase 0→1→2b→3→4→5 | ≥8 复杂度 / 用户说"全自动" |

---

## Phase 1 — 调查（探索 / 审计驱动）

- 并行 `explore` 扫描代码库
- 理解架构、数据流、依赖关系
- `search_content`/`glob` 补充细节

---

## Phase 2 — 设计

**Standard (2a)**: 简单规划 → 直接编码
**Full (2b)**: 审计驱动（`explore` 扫描 → 设计 → 审查 → 编码）

---

## Phase 3 — 编码

- 小改动：直接 `edit_file` / `write_file`
- 大改动：`multi_edit` 批量写入（一次性验证全回滚）
- 独立 shell 命令：`run_command` 并发执行

### 工具原则

| 工具 | 用法 |
|------|------|
| `submit_plan` | 适合需要用户审批的多文件重构，全自动模式下不强制、不禁止 |
| `ask_choice` | 真正需要用户决策时使用 |
| `todo_write` | 多步骤追踪，有用就用 |
| `explore` | 宽网调查，返回精炼结论 |

---

## Phase 4 — 验证

- `run_command` 运行类型检查、测试
- 失败时 `diagnose` → 修复 → 重新验证

---

## Phase 5 — 收尾

1. 自我回顾（做了什么、遇到什么问题、学到了什么）
2. 展示成果（任务名、路径、产出文件、验证结果）
3. 追加 `skill_performance.json`
4. 写 `memory/experiences/{日期}-{摘要}.md`
5. `compact_memories.py` 压缩记忆
6. `git -C ~/.reasonix add/commit/push`（如果 .reasonix 有变更）
7. 停 watchdog、删 state.json

---

## 路径覆盖

| 触发词 | 路径 |
|--------|------|
| "直接回答" / "快速回答" | Quick |
| "全自动" | Full |
| 默认（无触发词） | 按复杂度评估 |
