---
name: docx
description: "Comprehensive document creation, editing, and analysis with support for tracked changes, comments, formatting preservation, and text extraction. When you need to work with professional documents (.docx files) for: (1) Creating new documents, (2) Modifying or editing content, (3) Working with tracked changes, (4) Adding comments, or any other document tasks."
license: Proprietary. LICENSE.txt has complete terms
---

<MANDATORY_EXECUTION_SCRIPT>
你必须严格按照以下步骤执行，每完成一步输出 [√] 并附简要结果。
禁止跳过、合并、改变顺序。未输出 [√] 的步骤视为未执行。

## Gate 1: 分析输入
STEP 1.1: 输出 `[DOCX] === DOCX 启动 ===` → [√]
STEP 1.2: 确定任务类型：创建新文档 / 编辑现有文档 / 提取内容 → [√] 类型: {创建/编辑/提取}
STEP 1.3: 若是编辑现有文档 → 用 pandoc 提取文本或解压 XML → [√] 已分析
STEP 1.4: 检查依赖可用性（npm docx / pandoc / soffice）→ [√]
=== Gate 1 PASSED（输入已分析）===

## Gate 2: 执行
STEP 2.1: 创建或编辑文档 → [√]
STEP 2.2: 使用正确方法：
         → 新建：JavaScript + npm docx
         → 编辑：unpack → 编辑 XML → pack
         → 提取：pandoc 或解压 → [√]
=== Gate 2 PASSED（文档已生成/修改）===

## Gate 3: 验证 + 交付
STEP 3.1: 验证文档可打开（soffice 转 PDF 或 pandoc 提取检查）→ [√] {通过/失败}
STEP 3.2: 确认内容完整 → [√]
STEP 3.3: 输出 `[DOCX] 🏁 完成: {路径}` → [√]
=== Gate 3 PASSED（DOCX 完成）===
</MANDATORY_EXECUTION_SCRIPT>

---

## 硬门禁清单

### Gate 1 出口
- [ ] 任务类型: {创建/编辑/提取}
- [ ] 输入已分析
- [ ] 依赖已检查
- [✓] 本门禁所有项已勾选

全部满足后输出：`=== Gate 1 PASSED ===`

### Gate 2 出口
- [ ] 文档已生成/修改
- [ ] 使用正确方法
- [✓] 本门禁所有项已勾选

全部满足后输出：`=== Gate 2 PASSED ===`

### Gate 3 出口
- [ ] 文档验证通过
- [ ] 内容完整
- [✓] 本门禁所有项已勾选

全部满足后输出：`=== Gate 3 PASSED ===`

---

## 输出格式模板
```
[DOCX] === DOCX 启动 ===
[DOCX] 类型: 创建新文档 | 依赖: ✅
[DOCX] ✅ 文档已生成: output.docx
[DOCX] ✅ 验证通过
[DOCX] 🏁 完成: output.docx
```

---

以下为完整参考文档：

## Quick Reference

| Task | Approach |
|------|----------|
| read_file/analyze content | `pandoc` or unpack for raw XML |
| Create new document | Use `docx-js` - see Creating New Documents below |
| edit_file existing document | Unpack → edit XML → repack - see Editing Existing Documents below |

### Converting .doc to .docx
```bash
soffice --headless --convert-to docx document.doc
```

### Reading Content
```bash
pandoc --track-changes=all document.docx -o output.md
python scripts/unpack.py document.docx unpacked/
```

### Converting to Images
```bash
soffice --headless --convert-to pdf document.docx
pdftoppm -jpeg -r 150 document.pdf page
```

### Accepting Tracked Changes
```bash
python scripts/accept_changes.py input.docx output.docx
```

---

## Creating New Documents

Generate .docx files with JavaScript. Install as a project dependency: `npm install docx`

**⚠️ CRITICAL: In docx-js, use JavaScript escapes (`\"`) for quotes. NEVER use XML entities (`&#x201C;`) - they will appear as literal garbage text.**

### Setup
```javascript
const { Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell, ImageRun,
        Header, Footer, AlignmentType, PageOrientation, LevelFormat, ExternalHyperlink,
        TableOfContents, HeadingLevel, BorderStyle, WidthType, ShadingType,
        VerticalAlign, PageNumber, PageBreak } = require('docx');

const doc = new Document({ sections: [{ children: [/* content */] }] });
Packer.toBuffer(doc).then(buffer => fs.writeFileSync("doc.docx", buffer));
```

### Page Size
```javascript
// docx-js defaults to A4, not US Letter
// Always set page size explicitly
sections: [{
  properties: {
    page: {
      size: { width: 12240, height: 15840 }, // US Letter in DXA
      margin: { top: 1440, right: 1440, bottom: 1440, left: 1440 }
    }
  },
  children: [/* content */]
}]
```

### Fonts and CJK Support
```javascript
// For CJK documents: configure both ASCII and East Asian fonts
const doc = new Document({
  styles: {
    default: {
      document: {
        run: {
          font: { ascii: "Arial", hAnsi: "Arial", eastAsia: "Microsoft YaHei" },
          size: 24
        }
      }
    }
  }
});
```

### Lists (use LevelFormat, never unicode bullets)
```javascript
const doc = new Document({
  numbering: {
    config: [
      { reference: "bullets",
        levels: [{ level: 0, format: LevelFormat.BULLET, text: "•", alignment: AlignmentType.LEFT,
          style: { paragraph: { indent: { left: 720, hanging: 360 } } } }] },
    ]
  }
});
```

### Tables
```javascript
// CRITICAL: Set both columnWidths AND cell width
// CRITICAL: Use cantSplit: true to prevent row splitting
// CRITICAL: Use ShadingType.CLEAR not SOLID
new Table({
  width: { size: 100, type: WidthType.PERCENTAGE },
  columnWidths: [4680, 4680],
  rows: [
    new TableRow({
      cantSplit: true,
      children: [
        new TableCell({
          width: { size: 4680, type: WidthType.DXA },
          shading: { fill: "D5E8F0", type: ShadingType.CLEAR },
          margins: { top: 80, bottom: 80, left: 120, right: 120 },
          children: [new Paragraph({ children: [new TextRun("Cell")] })]
        })
      ]
    })
  ]
})
```

### Images
```javascript
// type parameter is REQUIRED
new Paragraph({
  children: [new ImageRun({
    type: "png",
    data: fs.readFileSync("image.png"),
    transformation: { width: 200, height: 150 },
    altText: { title: "Title", description: "Desc", name: "Name" }
  })]
})
```

### Page Breaks
```javascript
// PageBreak must be inside a Paragraph
new Paragraph({ children: [new PageBreak()] })
```

### Table of Contents
```javascript
// Headings must use HeadingLevel ONLY
new TableOfContents("Table of Contents", { hyperlink: true, headingStyleRange: "1-3" })
```

### Critical Rules for docx-js
- Set page size explicitly (docx-js defaults to A4)
- Configure CJK fonts for Chinese/Japanese/Korean
- Use JavaScript escapes for quotes (`\"` not XML entities)
- Never use `\n` - use separate Paragraph elements
- Never use unicode bullets - use LevelFormat.BULLET
- PageBreak must be in Paragraph
- ImageRun requires `type`
- Always set table `width` + `columnWidths`
- Use ShadingType.CLEAR not SOLID
- Set keepNext: false on headings to prevent whitespace issues
- Set cantSplit: true on table rows

---

## Editing Existing Documents

### Step 1: Unpack
```bash
python scripts/unpack.py document.docx unpacked/
```

### Step 2: edit_file XML
- Use edit_file tool directly for string replacement
- Use smart quotes: `&#x201C;` `&#x201D;` `&#x2018;` `&#x2019;`
- Add comments: `python scripts/comment.py unpacked/ 0 "text"`

### Step 3: Pack
```bash
python scripts/pack.py unpacked/ output.docx --original document.docx
```

### Tracked Changes
```xml
<w:ins w:id="1" w:author="AI Assistant" w:date="2025-01-01T00:00:00Z">
  <w:r><w:t>inserted text</w:t></w:r>
</w:ins>
<w:del w:id="2" w:author="AI Assistant" w:date="2025-01-01T00:00:00Z">
  <w:r><w:delText>deleted text</w:delText></w:r>
</w:del>
```

---

## Dependencies
- pandoc: Text extraction
- docx: `npm install docx`
- LibreOffice: PDF conversion
- Poppler: `pdftoppm` for images