---
name: pptx
description: "Presentation creation, editing, and analysis. When you need to work with presentations (.pptx files) for: (1) Creating new presentations, (2) Modifying or editing content, (3) Working with layouts, (4) Adding comments or speaker notes, or any other presentation tasks."
license: Proprietary. LICENSE.txt has complete terms
---

<MANDATORY_EXECUTION_SCRIPT>
你必须严格按照以下步骤执行，每完成一步输出 [√] 并附简要结果。
禁止跳过、合并、改变顺序。未输出 [√] 的步骤视为未执行。

## Gate 1: 分析输入
STEP 1.1: 输出 `[PPTX] === PPTX 启动 ===` → [√]
STEP 1.2: 确定任务类型：从零创建 / 基于模板编辑 / 分析提取 → [√] 类型: {创建/编辑/分析}
STEP 1.3: 若编辑现有 → 用 thumbnail.py + markitdown 分析 → [√]
          若从零创建 → 运行 design search 获取配色方案 → [√]
=== Gate 1 PASSED（输入已分析）===

## Gate 2: 执行
STEP 2.1: 根据类型执行：
         → 创建: pptxgenjs（JS）或 Python
         → 编辑: unpack → 修改 → pack
         → 分析: markitdown 提取 → [√]
STEP 2.2: 设计要点：配色鲜明、每页有视觉元素、避免纯文本 → [√]
=== Gate 2 PASSED（PPT 已生成）===

## Gate 3: QA + 验证
STEP 3.1: 转图片 → 目视检查布局、重叠、溢出 → [√]
          `soffice --headless --convert-to pdf output.pptx`
          `pdftoppm -jpeg -r 150 output.pdf slide`
STEP 3.2: 修复发现问题 → 重新验证 → [√]
STEP 3.3: 至少完成一轮 修复→验证 循环 → [√]
STEP 3.4: 输出 `[PPTX] 🏁 完成: {路径}` → [√]
=== Gate 3 PASSED（PPTX 完成）===
</MANDATORY_EXECUTION_SCRIPT>

---

## 硬门禁清单

### Gate 1 出口
- [ ] 任务类型: {创建/编辑/分析}
- [ ] 输入已分析（配色/模板）
- [✓] 本门禁所有项已勾选

全部满足后输出：`=== Gate 1 PASSED ===`

### Gate 2 出口
- [ ] PPT 已生成
- [ ] 设计质量达标
- [✓] 本门禁所有项已勾选

全部满足后输出：`=== Gate 2 PASSED ===`

### Gate 3 出口
- [ ] 视觉 QA 完成
- [ ] 问题已修复
- [ ] 至少一轮 修复→验证 循环
- [✓] 本门禁所有项已勾选

全部满足后输出：`=== Gate 3 PASSED ===`

---

## 输出格式模板
```
[PPTX] === PPTX 启动 ===
[PPTX] 类型: 创建 | 配色: 已生成
[PPTX] ✅ PPT 已生成: output.pptx
[PPTX] 🔍 QA: 发现 2 个布局问题 → 已修复
[PPTX] 🏁 完成: output.pptx
```

---

## Quick Reference

| Task | Guide |
|------|-------|
| read_file/analyze content | `python3 -m markitdown presentation.pptx` |
| edit_file or create from template | read_file [editing.md](editing.md) |
| Create from scratch | read_file [pptxgenjs.md](pptxgenjs.md) |
| Generate design system | `python3 skills/pptx/scripts/design/search.py "<topic>" --design-system` |

### Reading Content
```bash
python3 -m markitdown presentation.pptx
python3 scripts/thumbnail.py presentation.pptx
python3 scripts/unpack.py presentation.pptx unpacked/
```

### Converting to Images (for QA)
```bash
soffice --headless --convert-to pdf output.pptx
pdftoppm -jpeg -r 150 output.pdf slide
```

---

## Design Ideas

### Generate Design System (Recommended)
```bash
python3 skills/pptx/scripts/design/search.py "<topic> <industry>" --design-system -p "Name"
```

### Before Starting
- **Dominance over equality**: One color dominates (60-70%), 1-2 supporting, one accent
- **Dark/light contrast**: Dark for title+conclusion, light for content
- **Visual motif**: Pick ONE distinctive element and repeat it across all slides

### For Each Slide
- **Every slide needs a visual element** — image, chart, icon, or shape
- Vary layouts: two-column, icon+text rows, 2x2 grid, half-bleed image

### Avoid
- Repeating the same layout
- Centering body text
- Text-only slides (plain title + bullets)
- Low-contrast elements
- Horizontal lines between title and body

---

## QA (Required)

**Assume there are problems. Your job is to find them.**

### Content QA
```bash
python3 -m markitdown output.pptx | grep -iE "xxxx|lorem|ipsum|placeholder"
```
PowerShell: `Select-String -Pattern "xxxx|lorem|ipsum"`

### Visual QA (USE SUBAGENTS)
Convert slides to images, then dispatch subagent with fresh eyes to inspect for:
- Overlapping elements
- Text overflow
- Uneven gaps (<0.3" or nearly touching)
- Insufficient margins (<0.5" from edges)
- Low-contrast text/icons

### Verification Loop
1. Generate → Convert → Inspect
2. List issues
3. Fix
4. Re-verify affected slides
5. Repeat until no new issues

**Do not declare success until ≥1 fix-and-verify cycle complete.**

---

## Dependencies
- `pip3 install "markitdown[pptx]"`
- `pip3 install Pillow`
- `npm install pptxgenjs`
- LibreOffice + Poppler (PDF conversion)

For editing workflow, see [editing.md](editing.md). For PptxGenJS, see [pptxgenjs.md](pptxgenjs.md).