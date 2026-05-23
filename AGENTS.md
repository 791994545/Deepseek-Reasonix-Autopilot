# Reasonix 全局行为准则

除非被具体 skill 明确覆盖，以下规则适用于所有任务。

<MANDATORY_EXECUTION_SCRIPT>
**默认开启**：full-autonomous 自动加载，无需触发词。
每次会话启动时按以下步骤执行，每步输出 [√]。

STEP 1: 启动看门狗（`run_background("python ~/.reasonix/scripts/watchdog.py")`）+ 加载 error_patterns.json + memory/experiences（最近 5 条）+ 扫描 <available_tools> + <available_skills> → [√]
STEP 2: 加载 9 条全局记忆（memory/global/）+ project-rules.md（如存在）→ [√]
注：不维护硬编码技能列表。Phase 1 由 skill-router 动态扫描 ~/.reasonix/skills/ 发现所有技能。
STEP 3: 根据用户第一条消息执行 Phase 0 复杂度评估（1-10）→ 自动进入对应路径:
  · Quick (≤3) → 直接执行，跳过 Phase 2/2.3/2.5/3.2/3.5/4.5
  · Standard (4-7) → 走标准流程（Phase 2a→2.3→2.5→3→4→4.5→5）
  · Full (≥8) → 走完整流程（Phase 2b→2.3→2.5→3→4→4.5→5）
  [√] 路径: {Quick|Standard|Full}

**覆盖规则**:
- 用户说"直接回答/快速回答/简单说" → 强制 Quick，跳过 Phase 0 评估
- 用户说"全自动/深度分析/认真分析" → 强制 Full，即使看起来只是简单问题
</MANDATORY_EXECUTION_SCRIPT>

## 全局记忆索引（自动注入，无需手动加载）
| 记忆 | 优先级 | 内容 |
|------|--------|------|
| opencode-mandatory-script | 高 | 本文件的记忆镜像 |
| opencode-tool-reference | 高 | OpenCode→Reasonix 工具映射 |
| opencode-core-rules | 高 | 12 条核心原则 |
| opencode-error-patterns | 中 | 已知错误模式 |
| opencode-unattended-mode | 中 | 无人值守模式 |
| opencode-session-mgmt | 中 | 会话管理 |
| opencode-self-evolution | 中 | 自我改进/复盘 |
| opencode-subagent-proto | 中 | 子代理并行协议 |
| opencode-skill-catalog | 低 | 技能全景清单 |

## 关键规则
- 跳过任意步骤必须输出 `[√] ⏭️ 理由: {一句话}`，无理由跳过 = 违例
- 违例自动记入 `state.json violations` + 追加到 `error_patterns.json`（含 `skill_id` 字段）
- Phase 5 复盘复盘必写 `skill_performance.json` + `memory/experiences/`，不写 = 违例

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
