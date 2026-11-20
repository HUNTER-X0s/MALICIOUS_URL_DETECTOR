"""
report_sections/common.py - Shared styling, constants, and helper functions for PPD Report
"""

import os
from pathlib import Path
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

BASE_DIR = Path(r"z:\URLSentinel\URLSentinel_PPD_Report")
ASSETS_DIR = BASE_DIR / "assets"
DIAGRAMS_DIR = BASE_DIR / "diagrams"
DIAG_DIR = DIAGRAMS_DIR
CHARTS_DIR = BASE_DIR / "charts"
CHART_DIR = CHARTS_DIR
SCREENSHOTS_DIR = BASE_DIR / "screenshots"
SCREEN_DIR = SCREENSHOTS_DIR
DOCX_OUT = BASE_DIR / "URLSentinel_PPD_Report.docx"
PDF_OUT = BASE_DIR / "URLSentinel_PPD_Report.pdf"

CURRENT_DOC = None

def set_current_doc(doc):
    global CURRENT_DOC
    CURRENT_DOC = doc

def add_para(doc, text, bold=False, italic=False, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=6, space_before=0, font_size=12):
    global CURRENT_DOC
    CURRENT_DOC = doc
    p = doc.add_paragraph()
    p.alignment = align
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.space_before = Pt(space_before)
    p.paragraph_format.line_spacing = 1.18
    run = p.add_run(text)
    run.font.name = 'Times New Roman'
    run.font.size = Pt(font_size)
    run.bold = bold
    run.italic = italic
    return p

def add_bullet(*args):
    global CURRENT_DOC
    if len(args) == 1:
        doc = CURRENT_DOC
        text = args[0]
    elif len(args) >= 2:
        doc = args[0]
        text = args[1]
    else:
        return None
    if doc is None:
        return None
    p = doc.add_paragraph()
    p.paragraph_format.left_indent = Inches(0.25)
    p.paragraph_format.first_line_indent = Inches(-0.15)
    p.paragraph_format.space_before = Pt(1)
    p.paragraph_format.space_after = Pt(3)
    p.paragraph_format.line_spacing = 1.15
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    
    r_b = p.add_run("•  ")
    r_b.font.name = 'Times New Roman'
    r_b.font.size = Pt(11)
    r_b.bold = True
    
    r = p.add_run(text)
    r.font.name = 'Times New Roman'
    r.font.size = Pt(12)
    return p

def add_heading_1(doc, text):
    global CURRENT_DOC
    CURRENT_DOC = doc
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(18)
    p.paragraph_format.space_after = Pt(12)
    p.paragraph_format.keep_with_next = True
    run = p.add_run(text)
    run.font.name = 'Times New Roman'
    run.font.size = Pt(14)
    run.bold = True
    run.font.color.rgb = RGBColor(0, 0, 0)
    return p

def add_heading_2(doc, text):
    global CURRENT_DOC
    CURRENT_DOC = doc
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(12)
    p.paragraph_format.space_after = Pt(6)
    p.paragraph_format.keep_with_next = True
    run = p.add_run(text)
    run.font.name = 'Times New Roman'
    run.font.size = Pt(13)
    run.bold = True
    run.font.color.rgb = RGBColor(0, 0, 0)
    return p

def add_heading_3(doc, text):
    global CURRENT_DOC
    CURRENT_DOC = doc
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(8)
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.keep_with_next = True
    run = p.add_run(text)
    run.font.name = 'Times New Roman'
    run.font.size = Pt(12)
    run.bold = True
    run.font.color.rgb = RGBColor(0, 0, 0)
    return p

def add_image_box(doc, img_path, caption="", width_in=5.8):
    global CURRENT_DOC
    CURRENT_DOC = doc
    if os.path.exists(img_path):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before = Pt(6)
        p.paragraph_format.space_after = Pt(3)
        run = p.add_run()
        run.add_picture(str(img_path), width=Inches(width_in))
        if caption:
            cp = doc.add_paragraph()
            cp.alignment = WD_ALIGN_PARAGRAPH.CENTER
            cp.paragraph_format.space_before = Pt(2)
            cp.paragraph_format.space_after = Pt(8)
            crun = cp.add_run(caption)
            crun.font.name = 'Times New Roman'
            crun.font.size = Pt(10.5)
            crun.bold = True
            crun.italic = True
    else:
        print(f"Warning: Image not found: {img_path}")

def add_equation_box(*args):
    global CURRENT_DOC
    if len(args) == 2:
        doc = CURRENT_DOC
        formula, eq_num = args[0], args[1]
    elif len(args) >= 3:
        doc = args[0]
        formula, eq_num = args[1], args[2]
    else:
        return
    if doc is None:
        return
    tbl = doc.add_table(rows=1, cols=2)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    c0 = tbl.cell(0, 0)
    c1 = tbl.cell(0, 1)
    c0.width = Inches(4.8)
    c1.width = Inches(1.2)
    set_cell_background(c0, "F8F9FA")
    set_cell_background(c1, "F8F9FA")
    
    p0 = c0.paragraphs[0]
    p0.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p0.paragraph_format.space_before = Pt(3)
    p0.paragraph_format.space_after = Pt(3)
    r0 = p0.add_run(formula)
    r0.font.name = 'Times New Roman'
    r0.font.size = Pt(11)
    r0.font.italic = True
    
    p1 = c1.paragraphs[0]
    p1.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    p1.paragraph_format.space_before = Pt(3)
    p1.paragraph_format.space_after = Pt(3)
    r1 = p1.add_run(f"({eq_num})")
    r1.font.name = 'Times New Roman'
    r1.font.size = Pt(10.5)
    r1.bold = True
    
    set_table_borders(tbl)

def add_algorithm_box(*args):
    global CURRENT_DOC
    if len(args) == 4:
        doc = CURRENT_DOC
        title, input_desc, output_desc, steps = args[0], args[1], args[2], args[3]
    elif len(args) >= 5:
        doc = args[0]
        title, input_desc, output_desc, steps = args[1], args[2], args[3], args[4]
    else:
        return
    if doc is None:
        return
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell = tbl.cell(0, 0)
    cell.width = Inches(6.0)
    set_cell_background(cell, "FAFAFA")
    
    p0 = cell.paragraphs[0]
    p0.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p0.paragraph_format.space_before = Pt(3)
    p0.paragraph_format.space_after = Pt(2)
    r0 = p0.add_run(title)
    r0.font.name = 'Times New Roman'
    r0.font.size = Pt(10)
    r0.bold = True
    
    p_in = cell.add_paragraph()
    p_in.paragraph_format.space_before = Pt(1)
    p_in.paragraph_format.space_after = Pt(1)
    r_inl = p_in.add_run("Input: ")
    r_inl.font.name = 'Times New Roman'
    r_inl.font.size = Pt(9.5)
    r_inl.bold = True
    r_inv = p_in.add_run(input_desc)
    r_inv.font.name = 'Times New Roman'
    r_inv.font.size = Pt(9.5)
    r_inv.italic = True
    
    p_out = cell.add_paragraph()
    p_out.paragraph_format.space_before = Pt(1)
    p_out.paragraph_format.space_after = Pt(3)
    r_outl = p_out.add_run("Output: ")
    r_outl.font.name = 'Times New Roman'
    r_outl.font.size = Pt(9.5)
    r_outl.bold = True
    r_outv = p_out.add_run(output_desc)
    r_outv.font.name = 'Times New Roman'
    r_outv.font.size = Pt(9.5)
    r_outv.italic = True
    
    for step in steps:
        p_s = cell.add_paragraph()
        p_s.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p_s.paragraph_format.space_before = Pt(1)
        p_s.paragraph_format.space_after = Pt(1)
        p_s.paragraph_format.left_indent = Inches(0.15)
        p_s.paragraph_format.line_spacing = 1.1
        r_s = p_s.add_run(step)
        r_s.font.name = 'Consolas'
        r_s.font.size = Pt(8.5)
        r_s.font.color.rgb = RGBColor(20, 20, 20)
        
    set_table_borders(tbl)

def add_code_block(doc, code_text):
    global CURRENT_DOC
    CURRENT_DOC = doc
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell = tbl.cell(0, 0)
    set_cell_background(cell, "F5F5F5")
    cp = cell.paragraphs[0]
    cp.alignment = WD_ALIGN_PARAGRAPH.LEFT
    cp.paragraph_format.space_before = Pt(4)
    cp.paragraph_format.space_after = Pt(4)
    cp.paragraph_format.line_spacing = 1.15
    run = cp.add_run(code_text)
    run.font.name = 'Consolas'
    run.font.size = Pt(9.5)
    run.font.color.rgb = RGBColor(30, 30, 30)
    set_table_borders(tbl)
    doc.add_paragraph().paragraph_format.space_after = Pt(4)

def set_cell_background(cell, fill_hex):
    shading_xml = f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>'
    cell._tc.get_or_add_tcPr().append(parse_xml(shading_xml))

def set_table_borders(table):
    tblPr = table._tbl.tblPr
    borders = parse_xml(
        f'<w:tblBorders {nsdecls("w")}>\n'
        f'  <w:top w:val="single" w:sz="6" w:space="0" w:color="333333"/>\n'
        f'  <w:bottom w:val="single" w:sz="6" w:space="0" w:color="333333"/>\n'
        f'  <w:left w:val="none"/>\n'
        f'  <w:right w:val="none"/>\n'
        f'  <w:insideH w:val="single" w:sz="4" w:space="0" w:color="CCCCCC"/>\n'
        f'  <w:insideV w:val="none"/>\n'
        f'</w:tblBorders>'
    )
    tblPr.append(borders)

def style_table_header(row, col_widths=None):
    for i, cell in enumerate(row.cells):
        set_cell_background(cell, "EAEAEA")
        if col_widths and i < len(col_widths):
            cell.width = Inches(col_widths[i])
        for p in cell.paragraphs:
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p.paragraph_format.space_before = Pt(4)
            p.paragraph_format.space_after = Pt(4)
            for r in p.runs:
                r.font.name = 'Times New Roman'
                r.font.size = Pt(10)
                r.bold = True

def style_table_cells(table, col_widths=None):
    for r_idx, row in enumerate(table.rows[1:]):
        bg = "FFFFFF" if r_idx % 2 == 0 else "F9F9F9"
        for c_idx, cell in enumerate(row.cells):
            set_cell_background(cell, bg)
            if col_widths and c_idx < len(col_widths):
                cell.width = Inches(col_widths[c_idx])
            for p in cell.paragraphs:
                p.paragraph_format.space_before = Pt(3)
                p.paragraph_format.space_after = Pt(3)
                p.paragraph_format.line_spacing = 1.15
                for r in p.runs:
                    r.font.name = 'Times New Roman'
                    r.font.size = Pt(9.5)

def add_page_number(run):
    fldChar1 = OxmlElement('w:fldChar')
    fldChar1.set(qn('w:fldCharType'), 'begin')
    instrText = OxmlElement('w:instrText')
    instrText.set(qn('xml:space'), 'preserve')
    instrText.text = 'PAGE'
    fldChar2 = OxmlElement('w:fldChar')
    fldChar2.set(qn('w:fldCharType'), 'separate')
    fldChar3 = OxmlElement('w:fldChar')
    fldChar3.set(qn('w:fldCharType'), 'end')
    r = run._r
    r.append(fldChar1)
    r.append(instrText)
    r.append(fldChar2)
    r.append(fldChar3)
