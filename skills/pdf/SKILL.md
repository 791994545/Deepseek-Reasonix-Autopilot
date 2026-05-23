---
name: pdf
description: Comprehensive PDF manipulation toolkit for extracting text and tables, creating new PDFs, merging/splitting documents, and handling forms. When you need to fill in a PDF form or programmatically process, generate, or analyze PDF documents at scale.
license: Proprietary. LICENSE.txt has complete terms
---

<MANDATORY_EXECUTION_SCRIPT>
你必须严格按照以下步骤执行，每完成一步输出 [√] 并附简要结果。
禁止跳过、合并、改变顺序。未输出 [√] 的步骤视为未执行。

## Gate 1: 分析输入
STEP 1.1: 输出 `[PDF] === PDF 启动 ===` → [√]
STEP 1.2: 确定任务类型：提取内容 / 创建 / 合并拆分 / 表单填写 → [√] 类型: {提取/创建/合并/表单}
STEP 1.3: 若是读取 → 用 pypdf/pdfplumber 提取 → [√] 已读取 {N} 页
=== Gate 1 PASSED（输入已分析）===

## Gate 2: 执行
STEP 2.1: 根据任务类型选择工具并执行：
         → 提取: pdfplumber（文本/表格）
         → 创建: reportlab（CJK 字体注册）
         → 合并/拆分: pypdf 或 qpdf
         → 表单: 参照 FORMS.md → [√]
STEP 2.2: 处理完成 → [√]
=== Gate 2 PASSED（处理完成）===

## Gate 3: 验证 + 交付
STEP 3.1: 验证输出文件可打开、内容正确 → [√]
STEP 3.2: 输出 `[PDF] 🏁 完成: {路径}` → [√]
=== Gate 3 PASSED（PDF 完成）===
</MANDATORY_EXECUTION_SCRIPT>

---

## 硬门禁清单

### Gate 1 出口
- [ ] 任务类型: {提取/创建/合并/表单}
- [ ] 输入文件已分析
- [✓] 本门禁所有项已勾选

全部满足后输出：`=== Gate 1 PASSED ===`

### Gate 2 出口
- [ ] 处理已完成
- [✓] 本门禁所有项已勾选

全部满足后输出：`=== Gate 2 PASSED ===`

### Gate 3 出口
- [ ] 输出已验证
- [✓] 本门禁所有项已勾选

全部满足后输出：`=== Gate 3 PASSED ===`

---

## 输出格式模板
```
[PDF] === PDF 启动 ===
[PDF] 类型: 提取 | 页码: 12
[PDF] ✅ 已提取: output.xlsx
[PDF] 🏁 完成: output.xlsx
```

---

## Python Libraries

### pypdf - Basic Operations
```python
from pypdf import PdfReader, PdfWriter

# read_file
reader = PdfReader("document.pdf")
text = ""
for page in reader.pages:
    text += page.extract_text()

# Merge
writer = PdfWriter()
for pdf_file in ["doc1.pdf", "doc2.pdf"]:
    reader = PdfReader(pdf_file)
    for page in reader.pages:
        writer.add_page(page)
with open("merged.pdf", "wb") as output:
    writer.write(output)

# Split
reader = PdfReader("input.pdf")
for i, page in enumerate(reader.pages):
    writer = PdfWriter()
    writer.add_page(page)
    with open(f"page_{i+1}.pdf", "wb") as output:
        writer.write(output)

# Rotate
page = reader.pages[0]
page.rotate(90)
```

### pdfplumber - Text and Table Extraction
```python
import pdfplumber

with pdfplumber.open("document.pdf") as pdf:
    for page in pdf.pages:
        text = page.extract_text()
        tables = page.extract_tables()
```

### reportlab - Create PDFs
```python
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, KeepTogether, Image
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.colors import HexColor
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# Register CJK font
def register_cjk_font():
    import os, platform
    system = platform.system()
    if system == "Windows":
        paths = ["C:/Windows/Fonts/msyh.ttc"]
    elif system == "Darwin":
        paths = ["/System/Library/Fonts/PingFang.ttc"]
    else:
        paths = ["/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"]
    for p in paths:
        if os.path.exists(p):
            pdfmetrics.registerFont(TTFont("CJKFont", p, subfontIndex=0))
            return "CJKFont"
    return None

cjk_font = register_cjk_font()

# Professional styles
PRIMARY = HexColor('#1a365d')
ACCENT = HexColor('#2b6cb0')
styles = {
    'title': ParagraphStyle('Title', fontName=cjk_font, fontSize=28, textColor=PRIMARY, alignment=1),
    'h1': ParagraphStyle('H1', fontName=cjk_font, fontSize=20, textColor=PRIMARY, spaceBefore=24),
    'body': ParagraphStyle('Body', fontName=cjk_font, fontSize=11, spaceAfter=10),
}

doc = SimpleDocTemplate("report.pdf", pagesize=letter,
    leftMargin=0.75*inch, rightMargin=0.75*inch)
story = []
story.append(Paragraph("标题 Title", styles['title']))
story.append(Spacer(1, 20))
story.append(Paragraph("正文...", styles['body']))
doc.build(story)
```

### Pagination Best Practices
- **Use PageBreak ONLY once** (after cover page)
- **No KeepTogether** on headings/paragraphs — let content flow naturally
- **KeepTogether** for images+captions and small tables
- **Large tables** → use LongTable(repeatRows=1)

---

## Command-Line Tools

### pdftotext
```bash
pdftotext input.pdf output.txt
pdftotext -layout input.pdf output.txt
pdftotext -f 1 -l 5 input.pdf output.txt
```

### qpdf
```bash
qpdf --empty --pages file1.pdf file2.pdf -- merged.pdf
qpdf input.pdf --pages . 1-5 -- pages1-5.pdf
qpdf --password=mypassword --decrypt encrypted.pdf decrypted.pdf
```

---

## Common Tasks

### Extract Text from Scanned PDFs
```python
import pytesseract
from pdf2image import convert_from_path
images = convert_from_path('scanned.pdf')
for i, image in enumerate(images):
    text = pytesseract.image_to_string(image)
```

### Add Watermark
```python
watermark = PdfReader("watermark.pdf").pages[0]
reader = PdfReader("document.pdf")
writer = PdfWriter()
for page in reader.pages:
    page.merge_page(watermark)
    writer.add_page(page)
```

### Password Protection
```python
writer.encrypt("userpassword", "ownerpassword")
```

---

## Quick Reference

| Task | Best Tool |
|------|-----------|
| Merge PDFs | pypdf / qpdf |
| Split PDFs | pypdf / qpdf |
| Extract text | pdfplumber |
| Extract tables | pdfplumber |
| Create PDFs | reportlab |
| OCR scanned | pytesseract + pdf2image |
| Fill forms | See FORMS.md |

For advanced usage, see REFERENCE.md and FORMS.md.