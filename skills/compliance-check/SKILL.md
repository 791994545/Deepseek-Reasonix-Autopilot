---
name: compliance-check
description: Run compliance checks before key milestones — validates Rule 0 (skill pre-check), Rule 2 (simplicity), Rule 8 (read before write), Rule 9 (test intent), and danger operations. Called automatically at Gate checkpoints by full-autonomous. Triggers: any Gate transition, pre-commit, pre-delivery.
allowed-tools: run_command, read_file, search_files, search_content
---

<MANDATORY_EXECUTION_SCRIPT>
你必须严格按照以下步骤执行，每完成一步输出 [√] 并附简要结果。
禁止跳过、合并、改变顺序。未输出 [√] 的步骤视为未执行。

## Gate 1: 需求锚点 + 安全设计
STEP 1.1: 输出 `[Compliance] === Compliance Check 启动 ===` → [√]
STEP 1.2: 检查需求锚点是否已记录（至少 1 个不可覆盖锚点）→ [√] {已记录/缺失}
         → 缺失则 ❌ 强制暂停
STEP 1.3: 若为 Full 路径 → 检查 security-best-practices 已执行 → [√] {已执行/未执行}
         → 未执行则 ❌ 强制暂停
=== Gate 1 PASSED（锚点+安全通过）===

## Gate 2: 规则检查
STEP 2.1: Rule 0 — 检查当前任务是否命中技能触发词，对应 skill 是否已加载
         → 未加载则暂停，加载后再继续 → [√] {合规/已纠正}
STEP 2.2: Rule 8 — 检查本次修改涉及的每个文件是否已读取
         → 未读文件存在则暂停，读取后再继续 → [√] {合规/已纠正}
STEP 2.3: Rule 2 — 检查代码是否最小：无未请求的抽象层、框架引入、过量代码
         → 存在违规则暂停修正 → [√] {合规/已纠正}
STEP 2.4: Rule 9 — 检查测试是否覆盖边界条件而非仅主路径
         → 覆盖不足则暂停补充 → [√] {合规/已纠正}
=== Gate 2 PASSED（规则检查通过）===

## Gate 3: 危险操作审计
STEP 3.1: 扫描本次操作是否包含破坏性命令（rm -rf / DROP TABLE / force push / 付费API）→ [√]
STEP 3.2: 若有危险操作 → 检查是否已输出 `<danger>` 标签及回滚方案
         → 缺失则 ❌ 暂停 → [√] {安全/已添加标签}
=== Gate 3 PASSED（危险审计通过）===

## Gate 4: 自检 + 报告
STEP 4.1: 汇总以上所有检查结果 → [√]
          `[Compliance] 🏁 检查报告 | ✅ N 通过 | ⚠️ M 警告 | ❌ P 失败`
STEP 4.2: 警告反复出现 2 次 → 升级为 ❌ 阻塞 → [√]
STEP 4.3: 结果记录到 error_patterns.json（如有违规）→ [√]
=== Gate 4 PASSED（合规检查完成）===
</MANDATORY_EXECUTION_SCRIPT>

---

## 五层强制保障

| 层 | 机制 | 位置 |
|----|------|------|
| 1 | 剧本化指令 — MANDATORY 脚本 | 本文件顶部 |
| 3 | Gate 4 强制汇总 + 重复违规升级 | 本文件 Gate 4 |
| 4 | 最小化上下文 | 参考移至 `details.md` |
| 5 | 违规自动记录 + 置信度追踪 | `opencode-error-patterns` 全局记忆 |

---

## 硬门禁清单

### Gate 1 出口
- [ ] 需求锚点已确认: {已记录/缺失}
- [ ] 安全审查已执行（Full 路径）: {是/否/不适用}
- [✓] 本门禁所有项已勾选

全部满足后输出：`=== Gate 1 PASSED ===`

### Gate 2 出口
- [ ] Rule 0 技能预检: {合规/已纠正}
- [ ] Rule 8 读后才写: {合规/已纠正}
- [ ] Rule 2 简单优先: {合规/已纠正}
- [ ] Rule 9 测试意图: {合规/已纠正}
- [✓] 本门禁所有项已勾选

全部满足后输出：`=== Gate 2 PASSED ===`

### Gate 3 出口
- [ ] 危险操作已扫描: {N} 条
- [ ] `<danger>` 标签已检查: {安全/已添加}
- [✓] 本门禁所有项已勾选

全部满足后输出：`=== Gate 3 PASSED ===`

### Gate 4 出口
- [ ] 检查报告已输出
- [ ] 重复违规已升级（如有）
- [ ] 违规已记录到 error_patterns.json
- [✓] 本门禁所有项已勾选

全部满足后输出：`=== Gate 4 PASSED ===`

---

## 输出格式模板

### 启动
```
[Compliance] === Compliance Check 启动 ===
[Compliance] 检查节点: {Gate X / pre-commit / pre-delivery}
```

### 逐项检查
```
[Compliance] ✅ Gate 1: 需求锚点已记录
[Compliance] ❌ Rule 8: 文件未读取: src/main.py — 暂停，先读取
[Compliance] ⚠️ Rule 2: 发现未请求的 IRepository 接口
```

### 危险操作
```
[Compliance] 🔍 危险扫描: 发现 2 条破坏性命令
[Compliance] ✅ 命令1: rm -rf ./dist — 已含 <danger> 标签
[Compliance] ❌ 命令2: DROP TABLE users — 缺少 <danger> — 已添加
```

### 汇总
```
[Compliance] 🏁 检查报告 | ✅ 5 通过 | ⚠️ 1 警告 | ❌ 0 失败
[Compliance] ℹ️ 警告升级: Rule 2 同一违规出现 2 次 → 升级为 ❌ 阻塞
```

---

## 检查项判定

| 判定 | 含义 | 动作 |
|------|------|------|
| ✅ | 通过 | 无操作，继续 |
| ⚠️ | 警告 | 暂停当前任务，修正后继续 |
| ❌ | 失败 | 强制暂停，标记硬阻塞，不可跳过 |
| ⚠️→❌ | 同项反复 2 次 | 升级为阻塞，切换备选策略 |

---

See `details.md` for full documentation.