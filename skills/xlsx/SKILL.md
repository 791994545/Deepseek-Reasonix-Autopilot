---
name: xlsx
description: "Use this skill any time a spreadsheet file is the primary input or output. This means any task where the user wants to: open, read, edit, or fix an existing .xlsx, .xlsm, .csv, or .tsv file (e.g., adding columns, computing formulas, formatting, charting, cleaning messy data); create a new spreadsheet from scratch or from other data sources; or convert between tabular file formats."
license: Proprietary. LICENSE.txt has complete terms
---

<MANDATORY_EXECUTION_SCRIPT>
你必须严格按照以下步骤执行，每完成一步输出 [√] 并附简要结果。
禁止跳过、合并、改变顺序。未输出 [√] 的步骤视为未执行。

## Gate 1: 分析输入
STEP 1.1: 输出 `[XLSX] === XLSX 启动 ===` → [√]
STEP 1.2: 确定任务类型：创建 / 编辑 / 分析 / 转换 → [√] 类型: {创建/编辑/分析/转换}
STEP 1.3: 若是编辑/分析 → 用 pandas 或 openpyxl 读取 → [√] 已读: {N} 行, {M} 列
=== Gate 1 PASSED（输入已分析）===

## Gate 2: 执行
STEP 2.1: 选择工具：
         → 数据分析/批量操作: pandas
         → 公式/格式/Excel 特性: openpyxl → [√]
STEP 2.2: 使用 Excel 公式而非硬编码值（保持动态可更新）→ [√]
STEP 2.3: 处理后保存 → [√]
STEP 2.4: 若含公式 → 运行 `python scripts/recalc.py output.xlsx` 重算 → [√]
          检查错误（#REF! / #DIV/0! / #VALUE! / #NAME?）→ [√]
=== Gate 2 PASSED（处理完成）===

## Gate 3: 验证 + 交付
STEP 3.1: 验证输出（公式无错误、格式正确、数据完整）→ [√]
STEP 3.2: 输出 `[XLSX] 🏁 完成: {路径}` → [√]
=== Gate 3 PASSED（XLSX 完成）===
</MANDATORY_EXECUTION_SCRIPT>

---

## 硬门禁清单

### Gate 1 出口
- [ ] 任务类型: {创建/编辑/分析/转换}
- [ ] 输入已读取
- [✓] 本门禁所有项已勾选

全部满足后输出：`=== Gate 1 PASSED ===`

### Gate 2 出口
- [ ] 处理已完成
- [ ] 使用公式而非硬编码
- [ ] 公式重算完成（如有）
- [ ] 零公式错误
- [✓] 本门禁所有项已勾选

全部满足后输出：`=== Gate 2 PASSED ===`

### Gate 3 出口
- [ ] 验证通过
- [✓] 本门禁所有项已勾选

全部满足后输出：`=== Gate 3 PASSED ===`

---

## 输出格式模板
```
[XLSX] === XLSX 启动 ===
[XLSX] 类型: 创建 | 列: 12, 行: 200
[XLSX] ✅ 公式使用: SUM/AVERAGE/VLOOKUP | 错误: 0
[XLSX] ✅ 重算通过
[XLSX] 🏁 完成: output.xlsx
```

---

## Requirements for Outputs

### Professional Font
- Use consistent font (Arial, Times New Roman)

### Zero Formula Errors
- Every Excel model delivered with ZERO formula errors

### Preserve Existing Templates
- Exactly match existing format/style/conventions
- Template conventions ALWAYS override these guidelines

### Financial Model Color Standards
| Element | Color |
|---------|-------|
| Hardcoded inputs | Blue text (0,0,255) |
| Formulas | Black text (0,0,0) |
| Same-worksheet links | Green text (0,128,0) |
| External links | Red text (255,0,0) |
| Key assumptions | Yellow fill (255,255,0) |

### Number Formatting
- Years: text strings
- Currency: `$#,##0`, specify units in headers
- Zeros: display as `-`
- Percentages: `0.0%`
- Multiples: `0.0x`
- Negative: parentheses `(123)`

### Formula Construction
- Place ALL assumptions in separate cells
- Use cell references, not hardcoded values in formulas
- Verify all cell references, no off-by-one errors
- Test with zero/negative edge cases
- No circular references

---

## Common Workflow

```python
# Data analysis with pandas
import pandas as pd
df = pd.read_excel('file.xlsx')
df.to_excel('output.xlsx', index=False)

# Create with openpyxl (formulas + formatting)
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment
wb = Workbook()
sheet = wb.active
sheet['A1'] = 'Hello'
sheet['B2'] = '=SUM(A1:A10)'  # Use formulas, not hardcoded values
sheet.column_dimensions['A'].width = 20
wb.save('output.xlsx')

# Edit existing
from openpyxl import load_workbook
wb = load_workbook('existing.xlsx')
sheet = wb.active
sheet['A1'] = 'New Value'
wb.save('modified.xlsx')

# Recalculate formulas (MANDATORY if using formulas)
# python scripts/recalc.py output.xlsx
```

### Excel vs Python: Cell/Column Rules
- Cell indices are 1-based (row=1, column=1 = A1)
- Use `data_only=True` to read computed values (but don't save with it)
- For large files: `read_only=True` or `write_only=True`
- DataFrame col 0 = Excel col A (col_index + 1 in Excel)
- DataFrame row 0 = Excel row 2 (row_index + 2 in Excel, header + data)

### Formula Verification
- [ ] Test 2-3 sample references
- [ ] Column mapping correct
- [ ] NaN/None handled
- [ ] No division by zero
- [ ] Cross-sheet references use correct format (Sheet1!A1)

## Dependencies
- pandas: data analysis
- openpyxl: formulas + formatting
- LibreOffice: formula recalculation via `scripts/recalc.py`