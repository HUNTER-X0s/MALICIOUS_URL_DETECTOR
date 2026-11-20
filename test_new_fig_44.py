import docx
from docx.shared import Inches
import xml.etree.ElementTree as ET
import subprocess
import pypdf
import os

DOC_IN = os.path.abspath(r'z:\URLSentinel\URLSentinel_PPD_Report\test_budget_44.docx')
DOC_OUT = os.path.abspath(r'z:\URLSentinel\URLSentinel_PPD_Report\test_budget_44_new_fig.docx')
PDF_OUT = os.path.abspath(r'z:\URLSentinel\URLSentinel_PPD_Report\test_budget_44_new_fig.pdf')
NEW_IMG = r'z:\URLSentinel\URLSentinel_PPD_Report\diagrams\Fig_5_1_System_Architecture.png'

doc = docx.Document(DOC_IN)

with open(NEW_IMG, 'rb') as f:
    new_blob = f.read()

# Replace image blob in related_parts['rId11']
part = doc.part.related_parts['rId11']
part._blob = new_blob

# Update cx and cy in paragraph 209 (or whichever paragraph has blip rId11)
# Aspect ratio is 3588 / 1941 = 1.8485
# Width: 6.20 inches = 5669280 EMU
# Height: 6.20 / 1.8485 = 3.354 inches = 3066928 EMU
for p in doc.paragraphs:
    xml = p._element.xml
    if 'rId11' in xml:
        # find extent
        for elem in p._element.iter():
            if elem.tag.endswith('extent'):
                elem.attrib['cx'] = '5669280'
                elem.attrib['cy'] = '3066928'
                print("Updated extent to cx=5669280 (6.20 in), cy=3066928 (3.35 in)")

doc.save(DOC_OUT)
print("Saved test_budget_44_new_fig.docx")

ps_script = f'''
$word = New-Object -ComObject Word.Application
$word.Visible = $false
try {{
    $doc = $word.Documents.Open('{DOC_OUT}')
    $doc.SaveAs([ref]'{PDF_OUT}', [ref]17)
    $doc.Close([ref]0)
    Write-Host "Exported to PDF successfully!"
}} finally {{
    $word.Quit()
    [System.Runtime.Interopservices.Marshal]::ReleaseComObject($word) | Out-Null
}}
'''

with open('export_test_new_fig.ps1', 'w', encoding='utf-8') as f:
    f.write(ps_script)

res = subprocess.run(['powershell', '-ExecutionPolicy', 'Bypass', '-File', 'export_test_new_fig.ps1'], capture_output=True, text=True)
print("PowerShell output:", res.stdout)

reader = pypdf.PdfReader(PDF_OUT)
print(f"Total pages with new Fig 5.1: {len(reader.pages)}")

# Check chapter pages
chapters = [
    "1. INTRODUCTION",
    "2. LITERATURE REVIEW",
    "3. SYSTEM ANALYSIS",
    "4. METHODOLOGY",
    "5. SYSTEM DESIGN",
    "6. IMPLEMENTATION",
    "7. TESTING",
    "8. CHALLENGES",
    "9. RESULT AND ANALYSIS",
    "10. CONCLUSION"
]

for ch in chapters:
    found = [idx + 1 for idx, page in enumerate(reader.pages) if ch in page.extract_text()]
    print(f"{ch:25s} -> Page(s): {found}")
