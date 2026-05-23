---
name: slides
description: Create and edit presentation slide decks (`.pptx`) with PptxGenJS, bundled layout helpers, and render/validation utilities. Use when tasks involve building a new PowerPoint deck, recreating slides from screenshots/PDFs/reference decks, modifying slide content while preserving editable output, adding charts/diagrams/visuals, or diagnosing layout issues such as overflow, overlaps, and font substitution.
---

<MANDATORY_EXECUTION_SCRIPT>
你必须严格按照以下步骤执行，每完成一步输出 [√] 并附简要结果。
禁止跳过、合并、改变顺序。未输出 [√] 的步骤视为未执行。

## Gate 1: 分析输入
STEP 1.1: 输出 `[Slides] === Slides 启动 ===` → [√]
STEP 1.2: 确定任务类型：新建 / 基于参考重建 / 编辑 → [√] 类型: {新建/重建/编辑}
STEP 1.3: 新建 → 设画布比例（默认 16:9 LAYOUT_WIDE）→ [√]
STEP 1.4: 重建 → 先渲染参考源对比几何布局 → [√]
=== Gate 1 PASSED（输入已分析）===

## Gate 2: 执行
STEP 2.1: 复制 `assets/pptxgenjs_helpers/` 到工作目录 → [√]
STEP 2.2: 用 PptxGenJS（非 python-pptx）生成，交付 .pptx + 源 .js → [√]
STEP 2.3: 设计规则：显式主题字体、使用 autoFontSize/calcTextBox、不用内置 fit/autoFit → [√]
STEP 2.4: 包含 `warnIfSlideHasOverlaps` + `warnIfSlideElementsOutOfBounds` 验证 → [√]
=== Gate 2 PASSED（PPT 已生成）===

## Gate 3: 验证 + 交付
STEP 3.1: 渲染 PNG → `python3 scripts/render_slides.py deck.pptx` → [√]
STEP 3.2: 溢出检查 → `python3 scripts/slides_test.py deck.pptx` → [√]
STEP 3.3: 修复所有布局问题后交付 → [√]
STEP 3.4: 输出 `[Slides] 🏁 完成: {路径}` → [√]
=== Gate 3 PASSED（Slides 完成）===
</MANDATORY_EXECUTION_SCRIPT>

---

## 硬门禁清单

### Gate 1 出口
- [ ] 任务类型: {新建/重建/编辑}
- [ ] 画布比例已设置
- [✓] 本门禁所有项已勾选

全部满足后输出：`=== Gate 1 PASSED ===`

### Gate 2 出口
- [ ] Helper 已复制
- [ ] PptxGenJS 已生成
- [ ] 设计规则已遵守
- [ ] 验证函数已包含
- [✓] 本门禁所有项已勾选

全部满足后输出：`=== Gate 2 PASSED ===`

### Gate 3 出口
- [ ] 渲染检查通过
- [ ] 溢出检查通过
- [ ] 问题已修复
- [✓] 本门禁所有项已勾选

全部满足后输出：`=== Gate 3 PASSED ===`

---

## 输出格式模板
```
[Slides] === Slides 启动 ===
[Slides] 类型: 新建 | 比例: 16:9
[Slides] ✅ 已生成: deck.pptx + deck.js
[Slides] ✅ 渲染: 12 页 | 溢出: 0
[Slides] 🏁 完成: output/deck.pptx
```

---

## Overview

Use PptxGenJS for slide authoring. Keep work in a task-local directory. Only copy final artifacts to the requested destination after rendering and validation pass.

## Bundled Resources
- `assets/pptxgenjs_helpers/`: Copy into workspace and import locally
- `scripts/render_slides.py`: Rasterize .pptx to per-slide PNGs
- `scripts/slides_test.py`: Detect content overflow
- `scripts/create_montage.py`: Contact-sheet montage
- `scripts/detect_font.py`: Report missing/substituted fonts
- `scripts/ensure_raster_image.py`: Convert SVG/EMF/HEIC to PNGs
- `references/pptxgenjs-helpers.md`: API details

## Authoring Rules
- Set theme fonts explicitly
- Use `autoFontSize`, `calcTextBox` helpers (NOT built-in `fit`/`autoFit`)
- Use bullet options, not literal `•`
- Use `imageSizingCrop`/`imageSizingContain` (NOT built-in image sizing)
- Use `latexToSvgDataUri()` for equations, `codeToRuns()` for code blocks
- Prefer native PowerPoint charts for simple visuals (reviewers can edit)
- Include both overlap + out-of-bounds warnings in JS

## Validation Commands
```bash
python3 scripts/render_slides.py deck.pptx --output_dir rendered
python3 scripts/create_montage.py --input_dir rendered --output_file montage.png
python3 scripts/slides_test.py deck.pptx
python3 scripts/detect_font.py deck.pptx --json
```

## Recreate or Edit Existing Slides
- Render source deck first to compare geometry
- Match original aspect ratio
- Preserve editability (text stays text, charts stay native)
- Use `ensure_raster_image.py` for vector/odd image formats