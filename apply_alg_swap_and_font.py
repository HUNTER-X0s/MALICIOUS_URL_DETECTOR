import docx
from docx.shared import Pt, Inches, RGBColor
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
import copy

DOC_PATH = r'z:\URLSentinel\URLSentinel_PPD_Report\URLSentinel_PPD_Report_FINAL_BACKUP.docx'
doc = docx.Document(DOC_PATH)

table12 = doc.tables[12]
table13 = doc.tables[13]

print(f"Table 12 rows: {len(table12.rows)}")
print(f"Table 13 rows: {len(table13.rows)}")

# Print current headers
for i, r in enumerate(table12.rows):
    print(f"Table 12 row {i}: {r.cells[0].paragraphs[0].text[:50]}")
for i, r in enumerate(table13.rows):
    print(f"Table 13 row {i}: {r.cells[0].paragraphs[0].text[:50]}")

# Current:
# Table 12 row 0: Algorithm 1
# Table 12 row 1: Algorithm 2
# Table 12 row 2: Algorithm 4
# Table 13 row 0: Algorithm 3

# We want:
# Table 12 row 2: Algorithm 3
# Table 13 row 0: Algorithm 4

# Extract xml elements or paragraphs of Table 12 row 2 and Table 13 row 0
alg4_elm = copy.deepcopy(table12.rows[2]._tr)
alg3_elm = copy.deepcopy(table13.rows[0]._tr)

# Replace Table 12 row 2 with alg3_elm
table12.rows[2]._tr.getparent().replace(table12.rows[2]._tr, alg3_elm)

# Replace Table 13 row 0 with alg4_elm
table13.rows[0]._tr.getparent().replace(table13.rows[0]._tr, alg4_elm)

print("\nAfter swap:")
for i, r in enumerate(table12.rows):
    print(f"Table 12 row {i}: {r.cells[0].paragraphs[0].text[:50]}")
for i, r in enumerate(table13.rows):
    print(f"Table 13 row {i}: {r.cells[0].paragraphs[0].text[:50]}")

# Now format Table 12 and Table 13 paragraphs
# Font: Times New Roman
# Title: 12pt bold
# Input / Output: 11pt
# Steps: 11pt regular, line_spacing=1.05, space_after=1.0 pt
def format_alg_cell(cell):
    for p_idx, p in enumerate(cell.paragraphs):
        p.paragraph_format.line_spacing = 1.05
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(1.0)
        
        text = p.text.strip()
        if p_idx == 0:
            # Title
            p.paragraph_format.space_before = Pt(3)
            p.paragraph_format.space_after = Pt(2)
            for r in p.runs:
                r.font.name = 'Times New Roman'
                r.font.size = Pt(12)
                r.font.bold = True
                r.font.color.rgb = RGBColor(0, 0, 0)
        elif text.startswith('Input:') or text.startswith('Output:'):
            p.paragraph_format.space_after = Pt(1.5)
            # Make label bold, rest regular
            for r in p.runs:
                r.font.name = 'Times New Roman'
                r.font.size = Pt(11)
                r.font.color.rgb = RGBColor(0, 0, 0)
        else:
            for r in p.runs:
                r.font.name = 'Times New Roman'
                r.font.size = Pt(11)
                r.font.color.rgb = RGBColor(0, 0, 0)

for row in table12.rows:
    format_alg_cell(row.cells[0])

for row in table13.rows:
    format_alg_cell(row.cells[0])

# Also check cantSplit on rows
for t in [table12, table13]:
    for row in t.rows:
        trPr = row._tr.get_or_add_trPr()
        if trPr.find(qn('w:cantSplit')) is None:
            trPr.append(OxmlElement('w:cantSplit'))

doc.save(DOC_PATH)
print(f"Successfully saved updated {DOC_PATH}!")
