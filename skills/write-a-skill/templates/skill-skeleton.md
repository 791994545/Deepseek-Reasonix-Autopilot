<!--
  ═══════════════════════════════════════════════════
  固定骨架模板 — write-a-skill v2 产出每个 skill 的基底
  占位符由 write-a-skill 在 Phase 1-2 动态填充
  不可删减任何节
  ═══════════════════════════════════════════════════
-->
---
name: {skill_name}
description: {description}
triggers: {triggers}
---

# {skill_name}

<MANDATORY_EXECUTION_SCRIPT>
你必须严格按照以下步骤执行，每完成一步在本消息中输出 [√] 并附简要结果。
禁止跳过、合并、改变顺序。未输出 [√] 的步骤视为未执行。

{mandatory_steps}
</MANDATORY_EXECUTION_SCRIPT>

---

## 硬门禁清单

{gate_checklists}

---

## 输出格式模板

### 进度更新
```
[Auto] ✅ (N/M) 任务名 | 并行中: ...
[Auto] 🔄 失败 → 换方法
[Auto] ⏸ 阻塞: 原因
```

### 自检
```
[自检] Phase: {N} | 协议正常? [是/否] | 门禁通过? [是/否]
```

### 心跳
```
[心跳] (N/M) 进行中: ... | Phase: {N} | 自检: 正常
```

### 危险操作
```
<danger>
理由: ...
影响面: ...
回滚方案: ...
</danger>
```

---

## 自检规则

{self_check_rules}

---

## 快速参考

{file_references}
