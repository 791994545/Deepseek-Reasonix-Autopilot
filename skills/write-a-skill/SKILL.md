---
name: write-a-skill
description: Create a new skill with 5-layer enforcement framework (fixed skeleton + dynamic content injection).
triggers: "create a skill", "new skill", "write a skill", "skill gap", "技能缺口", "创建技能"
---

# Write a Skill v2

<MANDATORY_EXECUTION_SCRIPT>
你必须严格按照以下步骤执行，每完成一步在本消息中输出 [√] 并附简要结果。
禁止跳过、合并、改变顺序。未输出 [√] 的步骤视为未执行。

## Phase 0: 需求分析
STEP 0.1: 输出 `[Auto] === write-a-skill v2 启动 ===` → [√]
STEP 0.2: 提取目标 skill 元数据：名称、描述、触发关键词、用途 → [√] 名称: {X}, 描述: {Y}, 关键词: {Z}
STEP 0.3: 评估目标 skill 复杂度（1-10 分）:
         - 步骤数量: 1-3(1) / 4-8(2) / 9+(3)
         - 分支逻辑: 无(1) / 简单(2) / 复杂(3)
         - 外部技能依赖: 0(1) / 1-3(2) / 4+(3)
         - 输出类型: 单一(1) / 多种(2) → [√] 复杂度: {N} → 级别: {simple≤4|medium 5-7|complex≥8}
STEP 0.4: 技能缺口检测：检查 available_skills 中是否已存在同名/同功能 skill → [√] 冲突: {无/有 → 提示用户}
=== Phase 0 PASSED ===

## Phase 1: 骨架生成
STEP 1.1: 从 templates/skill-skeleton.md 读取固定骨架模板 → [√]
STEP 1.2: 根据复杂度级别确定骨架参数:
         - simple → 1-Phase 结构（5-8 步 MANDATORY, 1 个 gate checklist）
         - medium → 2-Phase 结构（8-12 步 MANDATORY, 2 个 gate checklists）
         - complex → 3-Phase 结构（12-18 步 MANDATORY, 3 个 gate checklists, 自适应分支） → [√]
STEP 1.3: 填充固定骨架中的动态占位符:
         - {skill_name}: 技能名称
         - {description}: 技能描述
         - {triggers}: 触发关键词
         - {complexity}: 复杂度级别
         - {mandatory_steps}: 根据类型和复杂度生成的步骤
         - {gate_checklists}: 对应的门禁项
         - {output_templates}: 输出格式模板（至少包含 [Auto]✅、[自检]、[心跳]、<danger>）
         - {self_check_rules}: 自检规则
         - {file_references}: 文件引用 → [√]
=== Phase 1 PASSED ===

## Phase 2: 动态内容注入
STEP 2.1: 根据技能用途生成核心 MANDATORY 步骤:
         - 分析类 skill → 步骤模板: [提取→分析→输出]
         - 生成类 skill → 步骤模板: [输入→处理→生成→验证]
         - 操作类 skill → 步骤模板: [确认→执行→检查→回滚]
         - 测试类 skill → 步骤模板: [设置→执行→断言→报告]
         - 其他 → 自定义步骤 → [√]
STEP 2.2: 注入 5 层强制保障到每个步骤:
         L1: 每步必须输出 [√]
         L2: 每个 Phase 出口有门禁清单
         L3: 每 2 步/5 分钟自检
         L4: 输出格式模板化
         L5: 违例记录 → [√]
STEP 2.3: 生成门禁项（每个 Phase 出口 4-7 个可核验条目）→ [√]
STEP 2.4: 生成文件引用（包括该 skill 的 bundled resources）→ [√]
=== Phase 2 PASSED ===

## Phase 3: 校验
STEP 3.1: 检查所有必需节是否存在:
         - [ ] MANDATORY_EXECUTION_SCRIPT 块
         - [ ] 硬门禁清单（每个 Phase 出口）
         - [ ] 输出格式模板（至少 [Auto]、[自检]、[心跳]、<danger>）
         - [ ] 自检规则
         - [ ] 快速参考 → [√]
STEP 3.2: 检查 MANDATORY 脚本可执行性:
         - 每步以可核验的动作为结尾
         - 所有 [√] 有明确的完成条件
         - 编号连续无跳跃 → [√]
STEP 3.3: 检查门禁项可核验性: 每项必须是"是/否"可明确判断的 → [√]
STEP 3.4: 输出验证报告: {通过/发现 N 个问题} → [√]
=== Phase 3 PASSED ===

## Phase 4: 交付
STEP 4.1: 在目标路径创建 SKILL.md 文件 → [√] 路径: {path}
STEP 4.2: 若复杂度为 medium 或 complex → 创建 rules/ 和 docs/ 子目录及内容 → [√]
STEP 4.3: 注册 skill（如需更新 opencode 配置）→ [√]
STEP 4.4: 输出交付报告: {包含 5 层保障的完整性确认} → [√]
STEP 4.5: 执行 self-improving 复盘（记录技能生成经验）→ [√]
STEP 4.6: 通知用户 → [√]
=== Phase 4 PASSED ===
</MANDATORY_EXECUTION_SCRIPT>

---

## 五层强制保障（自洽）

write-a-skill 自身和它产出的每一个 skill，都必须包含这 5 层：

| 层 | 自身保障 | 产出保障 |
|----|---------|---------|
| L1 剧本化 | 本文件的 MANDATORY 脚本 | 生成的 skill 也有 MANDATORY 脚本 |
| L2 看门狗 | 产出时 Phase 3 做完整性校验 | 生成的 skill 含硬门禁清单 |
| L3 自检 | Phase 2 每步后检查 | 生成的 skill 含自检规则 |
| L4 模板化 | 本文件全程使用 [Auto] 等模板 | 生成的 skill 含输出格式模板 |
| L5 自学习 | Phase 4 执行 self-improving 复盘 | 生成的 skill 引用 error_patterns 机制 |

---

## 固定骨架结构

每个由 write-a-skill 生成的 skill 都遵循以下固定结构，不可删减任何节。

```
skill-name/
├── SKILL.md (必须有)
│   ├── YAML frontmatter (name, description, triggers)
│   ├── <MANDATORY_EXECUTION_SCRIPT> (必须有)
│   ├── ## 硬门禁清单 (必须有)
│   ├── ## 输出格式模板 (必须有)
│   ├── ## 自检规则 (complex 级别强制, simple/medium 选配)
│   └── ## 快速参考 (必须有)
├── rules/ (medium+ 级别)
│   ├── 01-gate-checklists.md
│   └── 02-output-format.md
├── docs/ (complex 级别)
│   └── execution-flow.md
└── templates/ (按需)
    └── ...
```

### 动态占位符表

| 占位符 | 注入来源 | 示例值 |
|--------|---------|--------|
| `{skill_name}` | 用户输入 | `my-analyzer` |
| `{description}` | 用户输入 | `分析 Python 代码复杂度` |
| `{triggers}` | 用户输入 | `"analyze code", "复杂度分析"` |
| `{complexity}` | Phase 0 评估 | `simple` |
| `{mandatory_steps}` | Phase 2.1 模板 | 见下 |
| `{gate_checklists}` | Phase 2.3 生成 | `4-7 个可核验条目` |
| `{output_templates}` | 通用模板 | `[Auto] ✅ / [自检] / [心跳] / <danger>` |
| `{self_check_rules}` | 复杂度对应 | `每 2 步或 5 分钟` |
| `{file_references}` | 生成的文件列表 | `rules/, docs/, scripts/` |

---

## 步骤模板库（Phase 2.1 注入用）

### 分析类 skill 步骤模板
```
STEP 1: 收集输入数据 → [√]
STEP 2: 执行分析 → [√]
STEP 3: 输出分析结果（格式: ...）→ [√]
```

### 生成类 skill 步骤模板
```
STEP 1: 确认输入参数 → [√]
STEP 2: 执行生成逻辑 → [√]
STEP 3: 验证输出完整性 → [√]
STEP 4: 写入输出文件 → [√]
```

### 操作类 skill 步骤模板
```
STEP 1: 确认操作范围和影响 → [√]
STEP 2: 输出 <danger> 标签（如适用）→ [√]
STEP 3: 执行操作 → [√]
STEP 4: 验证结果 → [√]
STEP 5: 回滚（如失败）→ [√]
```

### 测试类 skill 步骤模板
```
STEP 1: 设置测试环境 → [√]
STEP 2: 执行测试 → [√]
STEP 3: 断言结果 → [√]
STEP 4: 生成测试报告 → [√]
```

### 复合类 skill（medium/complex）额外模板
```
每个 Phase 可选分支:
- 正常路径 → 标准步骤
- 错误路径 → 回溯到上一 Phase
- 技能缺口 → 触发 write-a-skill（递归）
```

---

## 硬门禁清单

### Phase 0 出口
- [ ] skill 元数据已提取: 名称 / 描述 / 触发关键词 / 用途
- [ ] 复杂度已评估: N 分 → {simple|medium|complex}
- [ ] 技能冲突检查: {无/有}
- [✓] 本门禁所有项已勾选
=== Phase 0 PASSED ===

### Phase 1 出口
- [ ] 固定骨架模板已读取
- [ ] 复杂度参数已确定
- [ ] 所有动态占位符已填充
- [✓] 本门禁所有项已勾选
=== Phase 1 PASSED ===

### Phase 2 出口
- [ ] 步骤类型已匹配（分析/生成/操作/测试/其他）
- [ ] 5 层强制保障已注入到每一步
- [ ] 门禁项已生成（每个 Phase 出口 4-7 项）
- [ ] 文件引用已生成
- [✓] 本门禁所有项已勾选
=== Phase 2 PASSED ===

### Phase 3 出口
- [ ] 所有必需节已存在（5 项必检）
- [ ] MANDATORY 脚本可执行（连续编号、可核验完成条件）
- [ ] 门禁项可核验（是/否可明确判断）
- [ ] 验证报告已输出: {通过/问题列表}
- [✓] 本门禁所有项已勾选
=== Phase 3 PASSED ===

### Phase 4 出口
- [ ] SKILL.md 已写入: {路径}
- [ ] rules/docs 目录已创建（medium+ 级别）
- [ ] 交付报告已输出（含 5 层保障完整性确认）
- [ ] self-improving 复盘已记录
- [ ] 用户已收到通知
- [✓] 本门禁所有项已勾选
=== Phase 4 PASSED ===

---

## 输出格式模板

```
[Auto] ✅ Phase 0 完成 | 技能: {X}, 复杂度: {Y}
[Auto] 🔄 Phase 2.2 注入失败 → 重试
[Auto] ⏸ 技能冲突: {Z} 已存在
[自检] Phase: 2 | MANDATORY 完整? [是/否] | 门禁通过? [是/否]
[心跳] (3/8) 进行中: 步骤注入 | Phase: 2
[协议违规] 检测到缺失: {缺失项}
```

---

## 自检规则

| 触发 | 检查项 |
|------|--------|
| 每完成 2 个 STEP | 最近 3 条消息含 [Auto]? Phase 门禁通过? |
| Phase 出口 | 门禁清单全部勾选? |
| 发现违例 | 记录到 error_patterns.json |

---

## 冲突裁决

1. 本 SKILL.md 的 MANDATORY_SCRIPT（最高）
2. 本 SKILL.md body
3. AGENTS.md 冲突解决表

---

## 快速参考

| 文件 | 用途 |
|------|------|
| `templates/skill-skeleton.md` | 固定骨架模板（生成的 skill 以此为基底） |
