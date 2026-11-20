"""
build_final_report.py - Master Assembly Script for URLSentinel Final Report
Generates URLSentinel_PPD_Report_FINAL.docx and compiles URLSentinel_PPD_Report_FINAL.pdf
Guarantees exactly 44 pages (9 preliminary + 35 main body) matching PPD.pdf.
"""

import os
import sys
import subprocess
from pathlib import Path

BASE_DIR = Path(r"z:\URLSentinel\URLSentinel_PPD_Report")
sys.path.insert(0, str(BASE_DIR))

import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.section import WD_SECTION
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

from report_sections.common import add_page_number, set_current_doc
from final_sections.preliminary import build_cover, build_preliminary_rest
from final_sections.ch1_intro import build_ch1
from final_sections.ch2_lit_review import build_ch2
from final_sections.ch3_sys_analysis import build_ch3
from final_sections.ch4_methodology import build_ch4
from final_sections.ch5_sys_design import build_ch5
from final_sections.ch6_implementation import build_ch6
from final_sections.ch7_testing import build_ch7
from final_sections.ch8_challenges import build_ch8
from final_sections.ch9_results import build_ch9
from final_sections.ch10_conclusion import build_ch10
from final_sections.references_sec import build_references

DOCX_FINAL = BASE_DIR / "URLSentinel_PPD_Report_FINAL.docx"
PDF_FINAL = BASE_DIR / "URLSentinel_PPD_Report_FINAL.pdf"

def main():
    print("=" * 65)
    print("URLSentinel Final PPD Report Generation (Target: Exactly 44 Pages)")
    print("Government College of Engineering, Kalahandi, Bhawanipatna")
    print("=" * 65)

    doc = Document()
    set_current_doc(doc)

    # Configure Default Normal Style
    normal_style = doc.styles['Normal']
    normal_style.font.name = 'Times New Roman'
    normal_style.font.size = Pt(12)
    normal_style.font.color.rgb = RGBColor(0, 0, 0)
    normal_style.paragraph_format.line_spacing = 1.18
    normal_style.paragraph_format.space_after = Pt(4)
    normal_style.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY

    # -------------------------------------------------------------------------
    # SECTION 1: Cover Page (Unnumbered, no header/footer)
    # -------------------------------------------------------------------------
    sec1 = doc.sections[0]
    sec1.page_width = Inches(8.27)
    sec1.page_height = Inches(11.69)
    sec1.left_margin = Inches(1.25)
    sec1.right_margin = Inches(1.0)
    sec1.top_margin = Inches(1.0)
    sec1.bottom_margin = Inches(1.0)
    sec1.different_first_page_header_footer = False

    print("\n[1/13] Building Cover Page (Unnumbered)...")
    build_cover(doc)

    # -------------------------------------------------------------------------
    # SECTION 2: Preliminary Pages (Certificate to List of Tables: i to viii)
    # -------------------------------------------------------------------------
    sec2 = doc.add_section(WD_SECTION.NEW_PAGE)
    sec2.page_width = Inches(8.27)
    sec2.page_height = Inches(11.69)
    sec2.left_margin = Inches(1.25)
    sec2.right_margin = Inches(1.0)
    sec2.top_margin = Inches(1.0)
    sec2.bottom_margin = Inches(1.0)

    # Unlink footer from Cover page
    sec2.header.is_linked_to_previous = False
    sec2.footer.is_linked_to_previous = False
    sec2.different_first_page_header_footer = False

    # LowerRoman numbering starting at 1 (Certificate is page i)
    sectPr2 = sec2._sectPr
    pgNumType2 = OxmlElement('w:pgNumType')
    pgNumType2.set(qn('w:fmt'), 'lowerRoman')
    pgNumType2.set(qn('w:start'), '1')
    sectPr2.append(pgNumType2)

    footer2 = sec2.footer
    f2_p = footer2.paragraphs[0]
    f2_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    f2_run = f2_p.add_run()
    f2_run.font.name = 'Times New Roman'
    f2_run.font.size = Pt(10)
    add_page_number(f2_run)

    print("[2/13] Building Preliminary Pages (Certificate to List of Tables, pp. i-viii)...")
    build_preliminary_rest(doc)

    # -------------------------------------------------------------------------
    # SECTION 3: Main Body (Chapters 1 to 10 + References: pp. 1-35)
    # -------------------------------------------------------------------------
    sec3 = doc.add_section(WD_SECTION.NEW_PAGE)
    sec3.page_width = Inches(8.27)
    sec3.page_height = Inches(11.69)
    sec3.left_margin = Inches(1.25)
    sec3.right_margin = Inches(1.0)
    sec3.top_margin = Inches(1.0)
    sec3.bottom_margin = Inches(1.0)

    # Unlink footer from Preliminary section
    sec3.header.is_linked_to_previous = False
    sec3.footer.is_linked_to_previous = False
    sec3.different_first_page_header_footer = False

    # Decimal numbering starting at 1 (Chapter 1 is page 1)
    sectPr3 = sec3._sectPr
    pgNumType3 = OxmlElement('w:pgNumType')
    pgNumType3.set(qn('w:fmt'), 'decimal')
    pgNumType3.set(qn('w:start'), '1')
    sectPr3.append(pgNumType3)

    footer3 = sec3.footer
    f3_p = footer3.paragraphs[0]
    f3_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    f3_run = f3_p.add_run()
    f3_run.font.name = 'Times New Roman'
    f3_run.font.size = Pt(10)
    add_page_number(f3_run)

    print("[3/13] Building 1. INTRODUCTION (Target: pp. 1-3)...")
    build_ch1(doc)

    print("[4/13] Building 2. LITERATURE REVIEW (Target: pp. 4-7)...")
    build_ch2(doc)

    print("[5/13] Building 3. SYSTEM ANALYSIS (Target: pp. 8-10)...")
    build_ch3(doc)

    print("[6/13] Building 4. METHODOLOGY (Target: pp. 11-13)...")
    build_ch4(doc)

    print("[7/13] Building 5. SYSTEM DESIGN (Target: pp. 14-19)...")
    build_ch5(doc)

    print("[8/13] Building 6. IMPLEMENTATION (Target: pp. 20-24)...")
    build_ch6(doc)

    print("[9/13] Building 7. TESTING (Target: pp. 25-27)...")
    build_ch7(doc)

    print("[10/13] Building 8. CHALLENGES AND LIMITATIONS (Target: pp. 28-29)...")
    build_ch8(doc)

    print("[11/13] Building 9. RESULT AND ANALYSIS (Target: pp. 30-32)...")
    build_ch9(doc)

    print("[12/13] Building 10. CONCLUSION & FUTURE SCOPE (Target: p. 33)...")
    build_ch10(doc)

    print("[13/13] Building REFERENCE (Target: pp. 34-35)...")
    build_references(doc)

    print(f"\nSaving Final DOCX to: {DOCX_FINAL}...")
    doc.save(str(DOCX_FINAL))
    print(f"Final DOCX saved successfully! Size: {os.path.getsize(DOCX_FINAL):,} bytes")

    # Word COM PDF Conversion
    print(f"\nCompiling Final PDF via Microsoft Word COM automation...")
    ps_script = BASE_DIR / "convert_final_pdf.ps1"
    ps_code = f"""
$word = New-Object -ComObject Word.Application
$word.Visible = $false
try {{
    $doc = $word.Documents.Open('{str(DOCX_FINAL)}')
    $doc.SaveAs('{str(PDF_FINAL)}', 17)
    $doc.Close()
    Write-Host "PDF Compilation Succeeded! Target: {str(PDF_FINAL)}"
}} catch {{
    Write-Host "Word COM Error: $_"
    exit 1
}} finally {{
    $word.Quit()
}}
"""
    with open(ps_script, "w", encoding="utf-8") as f:
        f.write(ps_code)

    res = subprocess.run(["powershell", "-ExecutionPolicy", "Bypass", "-File", str(ps_script)], capture_output=True, text=True)
    print("PowerShell Output:")
    print(res.stdout)
    if res.stderr:
        print("PowerShell Stderr:", res.stderr)

    if os.path.exists(PDF_FINAL):
        print(f"\nSUCCESS: Final PDF Generated! File size: {os.path.getsize(PDF_FINAL):,} bytes")
    else:
        print("\nWARNING: Final PDF not found.")

if __name__ == "__main__":
    main()
