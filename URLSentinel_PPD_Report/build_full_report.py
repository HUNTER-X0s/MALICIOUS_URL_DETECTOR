"""
build_full_report.py - Master Assembly Script for URLSentinel PPD Report
Generates URLSentinel_PPD_Report.docx and compiles URLSentinel_PPD_Report.pdf
"""

import os
import sys
import subprocess
from pathlib import Path

# Add URLSentinel_PPD_Report to sys.path
BASE_DIR = Path(r"z:\URLSentinel\URLSentinel_PPD_Report")
sys.path.insert(0, str(BASE_DIR))

import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.section import WD_SECTION

from report_sections.common import (
    DOCX_OUT, PDF_OUT, add_page_number
)
from report_sections.preliminary import build_preliminary_pages
from report_sections.chapter1_intro import build_chapter_1
from report_sections.chapter2_lit_review import build_chapter_2
from report_sections.chapter3_sys_analysis import build_chapter_3
from report_sections.chapter4_methodology import build_chapter_4
from report_sections.chapter5_sys_design import build_chapter_5
from report_sections.chapter6_implementation import build_chapter_6
from report_sections.chapter7_testing import build_chapter_7
from report_sections.chapter8_challenges import build_chapter_8
from report_sections.chapter9_results import build_chapter_9
from report_sections.chapter10_conclusion import build_chapter_10
from report_sections.references_section import build_references_section

def main():
    print("=" * 60)
    print("URLSentinel B.Tech PPD Report Generation")
    print("Government College of Engineering, Kalahandi, Bhawanipatna")
    print("=" * 60)

    doc = Document()

    # Section 1 Setup: A4, Margins: Left 1.25", Right 1.0", Top 1.0", Bottom 1.0"
    sec1 = doc.sections[0]
    sec1.page_width = Inches(8.27)
    sec1.page_height = Inches(11.69)
    sec1.left_margin = Inches(1.25)
    sec1.right_margin = Inches(1.0)
    sec1.top_margin = Inches(1.0)
    sec1.bottom_margin = Inches(1.0)

    # Configure Normal Style
    normal_style = doc.styles['Normal']
    normal_style.font.name = 'Times New Roman'
    normal_style.font.size = Pt(12)
    normal_style.font.color.rgb = RGBColor(0, 0, 0)
    normal_style.paragraph_format.line_spacing = 1.5
    normal_style.paragraph_format.space_after = Pt(6)
    normal_style.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY

    print("\n[1/12] Generating Preliminary Pages (Cover, Certificate, Declaration, Acknowledgement, Abstract, TOC)...")
    build_preliminary_pages(doc)

    # Create Section 2 for Chapters with Arabic Page Numbering
    sec2 = doc.add_section(WD_SECTION.NEW_PAGE)
    sec2.page_width = Inches(8.27)
    sec2.page_height = Inches(11.69)
    sec2.left_margin = Inches(1.25)
    sec2.right_margin = Inches(1.0)
    sec2.top_margin = Inches(1.0)
    sec2.bottom_margin = Inches(1.0)

    # Unlink footer and add page numbering
    sec2.footer.is_linked_to_previous = False
    footer_p = sec2.footer.paragraphs[0]
    footer_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    footer_run = footer_p.add_run()
    footer_run.font.name = 'Times New Roman'
    footer_run.font.size = Pt(10)
    add_page_number(footer_run)

    print("[2/12] Generating Chapter 1: INTRODUCTION...")
    build_chapter_1(doc)

    print("[3/12] Generating Chapter 2: LITERATURE REVIEW...")
    build_chapter_2(doc)

    print("[4/12] Generating Chapter 3: SYSTEM ANALYSIS...")
    build_chapter_3(doc)

    print("[5/12] Generating Chapter 4: METHODOLOGY...")
    build_chapter_4(doc)

    print("[6/12] Generating Chapter 5: SYSTEM DESIGN (Embedding Figs 5.1-5.8)...")
    build_chapter_5(doc)

    print("[7/12] Generating Chapter 6: IMPLEMENTATION (Embedding Algorithms 1-4, APIs, Figs 6.1-6.8)...")
    build_chapter_6(doc)

    print("[8/12] Generating Chapter 7: TESTING (Embedding Test Cases, Results, Fig 7.1)...")
    build_chapter_7(doc)

    print("[9/12] Generating Chapter 8: CHALLENGES AND LIMITATIONS...")
    build_chapter_8(doc)

    print("[10/12] Generating Chapter 9: RESULT AND ANALYSIS (Embedding Figs 9.1-9.3)...")
    build_chapter_9(doc)

    print("[11/12] Generating Chapter 10: CONCLUSION & FUTURE SCOPE...")
    build_chapter_10(doc)

    print("[12/12] Generating REFERENCES (IEEE Citations [1]-[30])...")
    build_references_section(doc)

    print(f"\nSaving DOCX to {DOCX_OUT}...")
    doc.save(str(DOCX_OUT))
    print(f"DOCX created successfully! File size: {os.path.getsize(DOCX_OUT):,} bytes")

    # Convert to PDF via Word COM
    print(f"\nCompiling PDF via Microsoft Word COM automation...")
    ps_script = BASE_DIR / "convert_to_pdf.ps1"
    ps_content = f"""
$word = New-Object -ComObject Word.Application
$word.Visible = $false
try {{
    $doc = $word.Documents.Open('{str(DOCX_OUT)}')
    $doc.SaveAs('{str(PDF_OUT)}', 17)
    $doc.Close()
    Write-Host "PDF Compilation Succeeded! Target: {str(PDF_OUT)}"
}} catch {{
    Write-Host "Word COM Error: $_"
    exit 1
}} finally {{
    $word.Quit()
}}
"""
    with open(ps_script, "w", encoding="utf-8") as f:
        f.write(ps_content)

    res = subprocess.run(["powershell", "-ExecutionPolicy", "Bypass", "-File", str(ps_script)], capture_output=True, text=True)
    print("PowerShell Output:")
    print(res.stdout)
    if res.stderr:
        print("PowerShell Stderr:", res.stderr)

    if os.path.exists(PDF_OUT):
        print(f"\nSUCCESS: PDF Generated! File size: {os.path.getsize(PDF_OUT):,} bytes")
    else:
        print("\nWARNING: PDF file not found at expected path.")

if __name__ == "__main__":
    main()
