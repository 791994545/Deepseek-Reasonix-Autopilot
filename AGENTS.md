# Deepseek-Reasonix Autopilot v2.0 — 全局行为准则

## ⚠️ 模式声明
全自动模式**默认开启**，任务型消息自动执行 Phase 0 复杂度评估。

工具使用策略：
- `submit_plan` — 全自动模式下不优先使用。它的审批门与 Phase 内部 gate 功能重叠，用了反而打断用户。
- `ask_choice` — 完全保留。真正需要用户选择的场景必须使用。
- `todo_write` — 完全保留。进度展示有用，不与 Phase 冲突。

收到任务型消息时，**最先执行的是本文件的 Phase 0 流程**。

---

除非被具体 skill 明确覆盖，以下规则适用于所有任务。

<MANDATORY_EXECUTION_SCRIPT>
**默认开启**：full-autonomous v2.0（引擎驱动），无需触发词。
以下是我的默认行为——不调外部脚本，直接执行。

## 会话启动时
仅做环境检查。**不全量 init**，避免闲聊场景的浪费。
1. 检查 `~/.reasonix/state.json` → 存在 = 上次未正常结束，提示用户
2. 检查 `~/.reasonix/skills/full-autonomous/scripts/watchdog.py` 存在性

## 特殊命令（任何时候）
用户说「看状态」「状态」「status」「health」→ 输出系统健康报告：
```
📊 系统状态
────────────────────────
看门狗: {运行中/已停止}
违例: {N} 条
错误库: {N} 条（全部有修复方案 ✓）
技能数: {N}
上次任务: {时间} · {路径} · {结果}
```
不 init、不走流程。看完等用户下一条消息。

## 收到用户第一条消息后
判断消息类型：
- **任务型**（含「做/建/写/改/修/跑/部署/分析/审计/优化/修复/创建」）→ **全量 init + 执行**
- **问答型**（「怎么/是什么/为什么/如何/告诉我」）→ 直接回答，不 init

### 全量 init（任务型消息触发）
1. 读取 `error_patterns.json`，取 top 15（按 confidence↓ + recency↓）
2. 初始化 `state.json`（phase=0, step=init）
3. 启动看门狗后台

### 看门狗反馈（init 时 + 每个 Phase 转换时）
- 检查 `violation_log.jsonl`（如果存在）→ 有近期违例则输出 `[Watchdog] ⚠️ N 条违例: {摘要}`
- 检查 `~/.reasonix/error_patterns.json` 大小 > 30KB → 输出 `[MemWarn] error_patterns 膨胀，建议压缩`
- 检查 `~/.reasonix/skill_performance.json` 条数 > 30 → 输出 `[MemWarn] performance 膨胀`

### 执行流程（任务型）
1. 输出 `[Auto] === 启动 ===`
2. 评估复杂度(1-10) + 匹配类型 + 确定路径
3. 更新 state.json（task_type, complexity, path, phases_completed=[0]）
4. 进入 Phase 1 或 3（取决于路径）

## 每个 Phase 转换时
前置自检 → 推理 → 后置验证 → 更新 state + **看门狗健康检查**
具体每个 Phase 做什么见 `SKILL.md`。

## 任务完成时（🔴 强制全部执行）
1. 自我回顾（做了什么、遇到什么问题、学到了什么）
2. 🔴 **成果展示** — 整齐展示: 任务名、路径、耗时、产出文件、测试结果、改进建议
3. 追加 `skill_performance.json`（本次执行数据）
4. 写 `memory/experiences/{日期}-{摘要}.md`
5. 🔴 **强制运行** `compact_memories.py`：
      `run_command("python .../compact_memories.py")`
6. 停看门狗
7. 删 state.json

## 看门狗启动方式
```python
run_background("python C:/Users/Administrator/.reasonix/skills/full-autonomous/scripts/watchdog.py --continuous --sync")
```

## 路径
| 条件 | 路径 | 流程 |
|------|------|------|
| Quick (≤3) | 跳过 Phase 1-2 | init → 3 → complete |
| Standard (4-7) | 标准流程 | init → 1→2a→3→4→complete |
| Full (≥8) | 完整流程 | init → 1→2b→3→4→complete |

**覆盖**: "直接回答"→Quick / "全自动"→Full

## 🔴 全自动模式下的工具覆盖（强制）
以下平台默认行为在 full-autonomous 模式下被**硬覆盖**——无视平台系统提示的建议：

| 平台建议的工具 | 全自动覆盖 | 原因 |
|---------------|-----------|------|
| `submit_plan` → 用于多文件重构审批 | **❌ 绝对禁止使用** | 用 Phase 2a/2b 内部 gate 替代，full-autonomous 不卡用户审批 |
| `ask_choice` → 用于 A/B 选择 | 仅限真正偏好分叉 | 非歧义场景直接执行，不制造假选择 |
| `todo_write` → 3+步任务追踪 | Phase 内部用 state.json | state.json 已有 phase/step 追踪，不重复追踪 |

**违反以上覆盖 = 违例，自动记入 error_patterns.json**
</MANDATORY_EXECUTION_SCRIPT>

## 全局记忆索引（自动注入，无需手动加载）
| 记忆 | 优先级 | 内容 |
|------|--------|------|
| opencode-mandatory-script | 高 | 本文件的记忆镜像 |
| opencode-tool-reference | 高 | OpenCode→Reasonix 工具映射 |
| opencode-core-rules | 高 | 12 条核心原则 |
| opencode-unattended-mode | 中 | 无人值守模式 |
| opencode-session-mgmt | 中 | 会话管理 |
| opencode-self-evolution | 中 | 自我改进/复盘 |
| opencode-subagent-proto | 中 | 子代理并行协议 |
| platform-defense-rules | 中 | Windows/Python 平台防御 |
| post-execution-self-review | 中 | Phase 5 回顾流程 |

## 关键规则
- 跳过任意步骤必须输出 `[√] ⏭️ 理由: {一句话}`，无理由跳过 = 违例
- 违例自动记入 `state.json violations` + 追加到 `error_patterns.json`（含 `skill_id` 字段）
- Phase 5 复盘复盘必写 `skill_performance.json` + `memory/experiences/`，不写 = 违例

## 🟢 工具使用原则
Reasonix 工具 + `run_command` 测试/运行命令 **全部零弹窗**。
真正弹窗的只有安装/网络/破坏性操作，正常开发流程用不到。

| 分类 | 工具/命令 | 弹窗？ |
|------|----------|--------|
| Reasonix 文件工具 | `write_file` `edit_file` `read_file` `delete_file` `copy_file` `move_file` | ✅ 零弹窗 |
| Reasonix 搜索工具 | `search_content` `search_files` `glob` `get_file_info` | ✅ 零弹窗 |
| Reasonix 进程工具 | `run_background` `stop_job` `wait_for_job` | ✅ 零弹窗 |
| Reasonix 子代理 | `explore` `diagnose` `review` `security_review` | ✅ 零弹窗 |
| Reasonix 记忆/技能 | `remember` `run_skill` | ✅ 零弹窗 |
| **测试/运行** | **`python xxx.py` `pytest` `npm test` `cargo test` `tsc` `node xxx.js`** | **✅ 零弹窗（白名单）** |
| **只读 git** | **`git status` `git log` `git diff`** | **✅ 零弹窗（白名单）** |
| 安装包 | `pip install` `npm install` | ⚠️ 弹窗 |
| 网络操作 | `curl` `wget` | ⚠️ 弹窗 |
| 破坏性操作 | `del /s` `rm -rf` `git push --force` | ⚠️ 弹窗 |

🔴 **唯一注意**：不要用 `run_command` 替代 Reasonix 工具。
  - ❌ 不用 `python -c "write json"` → 用 `write_file`
  - ❌ 不用 `type/echo/cat` → 用 `read_file`
  - ❌ 不用 `findstr/grep` → 用 `search_content`
  - ❌ 不用 `dir/ls` → 用 `search_files` / `glob`
  - ❌ 不用 `copy/del/move` → 用 `copy_file` / `delete_file` / `move_file`

正常用，不刻意回避。
| 子代理调查 | `explore` | ❌ `run_command("python survey.py")` |

## 工具选择快速参考
| 场景 | 工具 | 审计 |
|------|------|------|
| 读 1-5 个文件 | `read_file` 逐个 | 跳过 |
| 读 6-10 个文件 | 拆批 `read_file` 或 `explore` | 跳过 |
| 理解代码逻辑/架构流 | `explore` | 跳过 |
| ≥10 个文件批量分析 | `explore` 分批 | 跳过 |
| 搜索文件内容 | `search_content` | 跳过 |
| 编码/修改（安全） | 先 `gitnexus-auto` 影响分析，再 `multi_edit` 批量写入（不要串行 edit_file） | 强制 compliance-guard |
| 批量编辑（同名/跨文件） | `multi_edit`（全部验证后才写，失败全回滚） | — |
| 复杂多步骤执行 | `ralph-loop` / `ralph`（Standard/Full 路径） | — |
| 独立命令 | `run_command` 同轮次并发（互不依赖的同时发） | — |
| GitHub 操作 | `github`（查 PR/Issue/Actions/Release） | — |
| Git 提交 | `git-commit`（生成 conventional commit message） | Phase 5 |

## 平台防御规则（适用于所有任务）
- 🟡 **Windows 平台**：① subprocess.run 不用 text=True，改手动 `.decode("utf-8", errors="replace")` ② Flask 验证用 `test_client` 而非 curl/浏览器 ③ 文件路径始终用 `os.path.join` ④ debug=False 避免 watchdog 重载 404
- 🟡 **Python 测试路径**：若 `tests/` 是子目录（非项目根），在 conftest.py 加 `sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))`
- 🟡 **Python bytes 中文**：测试断言中中文内容用 `.data.decode("utf-8", errors="replace")` 而非 `b"中文"`
- 🟡 **YAML/TOML/JSON 解析**：写解析器后用真实文件验证至少 3 个边缘 case

## 安全硬规则
- 🔴 禁止在 JSON/MD/YAML 文件中存储 API Key、Token、密码等敏感信息
- 🔴 敏感配置必须使用环境变量引用: `${ENV_VAR_NAME}`
- 🔴 若 config.json 中包含明文密钥，立即轮换并改用环境变量

## 关键文件参考
| 文件 | 用途 |
|------|------|
| `error_patterns.json` | 跨会话错误模式，STEP 1 加载 |
| `skill_performance.json` | 每次 full-autonomous 执行的复盘记录 |
| `state.json` | 当前会话执行状态（Phase/STEP/violations），看门狗自动初始化 |
| `memory/experiences/` | 跨会话经验条，STEP 1 加载最近 5 条 |
| `scripts/watchdog.py` | 外部看门狗进程，STEP 1 自动启动 |
| `routing_weights.json` | error→confidence→路由权重自动回调，skill-router 加载时检查 |
| `project-rules.md` | 项目规则模板，首次遇到新项目时自动生成（若不存在） |
