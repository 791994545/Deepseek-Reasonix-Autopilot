---
name: zoom-out
description: Get a global perspective on unfamiliar code before making changes. Map architecture, data flow, and key abstractions. Use when exploring new codebases or before significant modifications.
allowed-tools: read_file,search_content,search_files
---

> **Reasonix 注意**: 此 skill 功能等价于内置 `explore` 工具。纯代码探索直接用 `explore({task:\"...\"})` 更轻量。

<MANDATORY_EXECUTION_SCRIPT>
你必须严格按照以下步骤执行，每完成一步输出 [√] 并附简要结果。
禁止跳过、合并、改变顺序。未输出 [√] 的步骤视为未执行。

## Gate 1: 入口点 + 数据流
STEP 1.1: 输出 `[ZoomOut] === Zoom Out 启动 ===` → [√]
STEP 1.2: 找到项目入口文件、路由、控制器 → [√] 入口: {文件列表}
STEP 1.3: 追踪数据从输入到存储的完整路径 → [√] 数据流: {描述}
=== Gate 1 PASSED（入口+数据流已映射）===

## Gate 2: 抽象 + 依赖
STEP 2.1: 识别核心模型、服务、接口 → [√] 核心抽象: {N} 个
STEP 2.2: 映射模块间依赖关系 → [√] 依赖图: {描述}
=== Gate 2 PASSED（抽象+依赖已识别）===

## Gate 3: 热点路径 + 记录
STEP 3.1: 找到最频繁执行的代码路径 → [√] 热点: {描述}
STEP 3.2: 输出架构总结 → [√]
          `[ZoomOut] 🏁 入口: {N} | 核心抽象: {M} | 热点: {K}`
STEP 3.3: 若发现重大架构问题 → 记录到 error_patterns.json 或项目规则 → [√]
=== Gate 3 PASSED（Zoom Out 完成）===
</MANDATORY_EXECUTION_SCRIPT>

---

## 五层强制保障

| 层 | 机制 | 位置 |
|----|------|------|
| 1 | 剧本化指令 — MANDATORY 脚本 | 本文件顶部 |
| 3 | Gate 3 强制输出架构总结 | 本文件 Gate 3 |
| 4 | 最小化上下文 | 参考移至 `details.md` |
| 5 | 架构问题自动记录 | Gate 3 → error_patterns / 项目规则 |

---

## 硬门禁清单

### Gate 1 出口
- [ ] 入口点已映射: {N} 个
- [ ] 数据流已追踪
- [✓] 本门禁所有项已勾选

全部满足后输出：`=== Gate 1 PASSED ===`

### Gate 2 出口
- [ ] 核心抽象已识别: {N} 个
- [ ] 依赖关系已映射
- [✓] 本门禁所有项已勾选

全部满足后输出：`=== Gate 2 PASSED ===`

### Gate 3 出口
- [ ] 热点路径已找到
- [ ] 架构总结已输出
- [ ] 问题已记录（如有）
- [✓] 本门禁所有项已勾选

全部满足后输出：`=== Gate 3 PASSED ===`

---

## 输出格式模板

### 启动
```
[ZoomOut] === Zoom Out 启动 ===
[ZoomOut] 项目: {名称}
```

### 入口
```
[ZoomOut] 🚪 入口: src/main.py, src/routes/ (5 个)
```

### 数据流
```
[ZoomOut] 🔄 数据流: HTTP → Router → Controller → Service → DB
```

### 抽象
```
[ZoomOut] 🧩 核心: UserModel, OrderService, PaymentGateway (接口)
```

### 依赖
```
[ZoomOut] 🔗 依赖图: Service 层依赖 Model 层 → 无循环依赖
```

### 汇总
```
[ZoomOut] 🏁 入口: 3 | 核心抽象: 12 | 热点: orderService.create()
```

---

## 关键规则

### 工具限制
- 只能使用 read_file / search_content / search_files — 不改代码
- 不运行命令
- 不修改文件

### 输出要求
- 每次探索后给出架构总结
- 重点标记：对当前任务有影响的发现
- 发现反模式或技术债 → 记录到项目规则

---

See `details.md` for full documentation.