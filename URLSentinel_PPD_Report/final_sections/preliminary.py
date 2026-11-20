"""
final_sections/preliminary.py - Preliminary pages for URLSentinel PPD Report
Rebuilt Cover Page, Certificate, Declaration, Acknowledgement, Abstract,
Contents (2 pages), List of Figures (1 page), List of Tables (1 page).
Total: exactly 9 preliminary pages.
"""

import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from report_sections.common import (
    ASSETS_DIR, add_para, set_cell_background, set_table_borders,
    style_table_header, style_table_cells
)

# Canonical student details - preserving strict lowercase 'pany' for Tanmay pany
STUDENTS = [
    ("ANURAG SWAIN", "2301110017"),
    ("SUBHANKAR SWAIN", "2301110077"),
    ("Tanmay pany", "2301110086"),
    ("BIDUVUSHAN SETHI", "2301110023"),
    ("SUDEEP GHOSH", "2301110080"),
]

def build_cover(doc):
    """Cover page: unnumbered, exact institutional styling."""
    add_para(doc, "A PROJECT FOR PRODUCT DEVELOPMENT REPORT",
             bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=0, space_after=2, font_size=13)
    add_para(doc, "ON",
             bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=1, space_after=3, font_size=11)
    add_para(doc, "URLSENTINEL: AI-POWERED PHISHING AND MALICIOUS URL DETECTION WITH BLOCKCHAIN-BACKED THREAT INTELLIGENCE",
             bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=2, space_after=12, font_size=14.5)

    add_para(doc, "SUBMITTED BY",
             bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=2, space_after=4, font_size=11)

    # Five student names stacked vertically (one line per student)
    for s_name, s_reg in STUDENTS:
        add_para(doc, f"{s_name.upper() if s_name != 'Tanmay pany' else 'Tanmay pany'} (REG. NO. - {s_reg})",
                 bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=1, space_after=1.5, font_size=10.5)

    add_para(doc, "Under The Esteemed Guidance of",
             italic=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=8, space_after=2, font_size=11)
    add_para(doc, "DR. ASHOK KUMAR BHOI (Asst. Professor)",
             bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=1, space_after=8, font_size=11.5)

    add_para(doc, "In partial fulfilment for the award of the degree",
             italic=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=2, space_after=1, font_size=10.5)
    add_para(doc, "Of",
             italic=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=1, space_after=1, font_size=10.5)
    add_para(doc, "BACHELOR OF TECHNOLOGY",
             bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=1, space_after=1, font_size=12.5)
    add_para(doc, "in",
             italic=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=1, space_after=1, font_size=10.5)
    add_para(doc, "COMPUTER SCIENCE AND ENGINEERING",
             bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=1, space_after=8, font_size=12.5)

    # Logo
    logo_path = ASSETS_DIR / "gcek_logo.png"
    if not logo_path.exists():
        logo_path = ASSETS_DIR / "gcek_logo.jpeg"
    if logo_path.exists():
        p_logo = doc.add_paragraph()
        p_logo.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_logo.paragraph_format.space_before = Pt(2)
        p_logo.paragraph_format.space_after = Pt(8)
        run_l = p_logo.add_run()
        run_l.add_picture(str(logo_path), width=Inches(1.55))

    add_para(doc, "GOVERNMENT COLLEGE OF ENGINEERING",
             bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=2, space_after=2, font_size=12.5)
    add_para(doc, "KALAHANDI, BHAWANIPATNA",
             bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=1, space_after=2, font_size=11.5)
    add_para(doc, "NOVEMBER 2026",
             bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=2, space_after=0, font_size=11)
    # No page break here because a Section Break follows immediately in master script


def build_preliminary_rest(doc):
    """Builds preliminary pages i through viii."""

    # =========================================================================
    # 2. CERTIFICATE (Page i)
    # =========================================================================
    p_c = doc.add_paragraph()
    p_c.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_c.paragraph_format.space_before = Pt(8)
    p_c.paragraph_format.space_after = Pt(14)
    rc = p_c.add_run("CERTIFICATE")
    rc.font.name = 'Times New Roman'
    rc.font.size = Pt(20)
    rc.bold = True

    add_para(doc,
        "This is to certify that the project entitled “URLSentinel: AI-Powered Phishing and Malicious URL Detection with "
        "Blockchain-Backed Threat Intelligence” is a bonafide work carried out by the following students of B.Tech in "
        "Computer Science and Engineering (7th Semester) at Government College of Engineering, Kalahandi (GCEK), "
        "Bhawanipatna during the academic year 2025–2026:",
        align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=8, font_size=12)

    for s_name, s_reg in STUDENTS:
        p_st = doc.add_paragraph()
        p_st.paragraph_format.left_indent = Inches(0.4)
        p_st.paragraph_format.space_after = Pt(2)
        p_st.paragraph_format.space_before = Pt(0)
        disp_name = s_name if s_name == "Tanmay pany" else s_name.upper()
        r_st = p_st.add_run(f"• {disp_name} (Reg. No. - {s_reg})")
        r_st.font.name = 'Times New Roman'
        r_st.font.size = Pt(11)
        r_st.bold = True

    add_para(doc,
        "The work presented in this project report is original and has been carried out under my supervision. This project has "
        "not been submitted, either in part or in full, to any other institution or university for the award of any degree.",
        align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_before=8, space_after=32, font_size=12)

    # Signature blocks
    sig_tbl = doc.add_table(rows=1, cols=2)
    sig_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    sig_tbl.autofit = False

    c0 = sig_tbl.cell(0, 0)
    c0.width = Inches(3.3)
    p0 = c0.paragraphs[0]
    p0.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p0.paragraph_format.line_spacing = 1.15
    p0.add_run("Signature\n\n\n").font.name = 'Times New Roman'
    r_a = p0.add_run("Dr. Ashok Kumar Bhoi\n")
    r_a.bold = True
    r_a.font.name = 'Times New Roman'
    p0.add_run("(Asst. Professor)\n(Supervisor)").font.name = 'Times New Roman'

    c1 = sig_tbl.cell(0, 1)
    c1.width = Inches(3.3)
    p1 = c1.paragraphs[0]
    p1.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p1.paragraph_format.line_spacing = 1.15
    p1.add_run("Signature\n\n\n").font.name = 'Times New Roman'
    r_b = p1.add_run("Dr. Basanta Kumar Swain\n")
    r_b.bold = True
    r_b.font.name = 'Times New Roman'
    p1.add_run("(Professor In-Charge)\n(Project For Product Development)").font.name = 'Times New Roman'

    p_hod = doc.add_paragraph()
    p_hod.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_hod.paragraph_format.space_before = Pt(28)
    p_hod.paragraph_format.line_spacing = 1.15
    p_hod.add_run("Signature\n\n\n").font.name = 'Times New Roman'
    r_h = p_hod.add_run("Dr. Gopal Behera\n")
    r_h.bold = True
    r_h.font.name = 'Times New Roman'
    p_hod.add_run("(Head of the Department CSE)").font.name = 'Times New Roman'

    doc.add_page_break()

    # =========================================================================
    # 3. DECLARATION (Page ii)
    # =========================================================================
    p_d = doc.add_paragraph()
    p_d.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_d.paragraph_format.space_before = Pt(8)
    p_d.paragraph_format.space_after = Pt(14)
    rd = p_d.add_run("DECLARATION")
    rd.font.name = 'Times New Roman'
    rd.font.size = Pt(20)
    rd.bold = True

    add_para(doc,
        "We hereby declare that the project entitled “URLSentinel: AI-Powered Phishing and Malicious URL Detection with "
        "Blockchain-Backed Threat Intelligence” is a genuine and original work carried out by us under the guidance of "
        "Dr. Ashok Kumar Bhoi, Assistant Professor, Department of Computer Science and Engineering, Government College "
        "of Engineering, Kalahandi (GCEK), Bhawanipatna.",
        align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=10, font_size=12)

    add_para(doc,
        "We further declare that this project report has not been submitted, either in part or in full, to any other institution or "
        "university for the award of any degree or diploma. All the information and data presented in this report are true to the "
        "best of our knowledge and belief. The resources used from anywhere else have been properly cited.",
        align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=28, font_size=12)

    for s_name, s_reg in STUDENTS:
        p_dec = doc.add_paragraph()
        p_dec.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        p_dec.paragraph_format.space_after = Pt(2.5)
        p_dec.paragraph_format.space_before = Pt(0)
        disp_name = s_name if s_name == "Tanmay pany" else s_name.upper()
        r_dc = p_dec.add_run(f"{disp_name} (Reg. No. - {s_reg})")
        r_dc.font.name = 'Times New Roman'
        r_dc.font.size = Pt(11)
        r_dc.bold = True

    doc.add_page_break()

    # =========================================================================
    # 4. ACKNOWLEDGEMENT (Page iii)
    # =========================================================================
    p_ack = doc.add_paragraph()
    p_ack.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_ack.paragraph_format.space_before = Pt(8)
    p_ack.paragraph_format.space_after = Pt(14)
    ra = p_ack.add_run("ACKNOWLEDGEMENT")
    ra.font.name = 'Times New Roman'
    ra.font.size = Pt(20)
    ra.bold = True

    add_para(doc,
        "We extend our heartfelt gratitude to everyone who contributed to the successful conceptualization, engineering, "
        "and empirical verification of the URLSentinel project. We are profoundly indebted to our esteemed project guide, "
        "Dr. Ashok Kumar Bhoi, Assistant Professor, Department of Computer Science and Engineering, for his visionary guidance, "
        "constructive critiques, and relentless technical encouragement throughout the development lifecycle.",
        align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=8, font_size=12)

    add_para(doc,
        "We convey our sincere appreciation to Dr. Basanta Kumar Swain, Professor In-Charge, Project For Product Development, "
        "for establishing robust academic rigor, continuous milestone reviews, and methodological guidance that elevated the "
        "engineering quality of our project.",
        align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=8, font_size=12)

    add_para(doc,
        "We express our deep gratitude to Dr. Gopal Behera, Head of the Department of Computer Science and Engineering, and to "
        "all respected faculty members and technical staff of the department for providing excellent computing infrastructure, "
        "encouraging autonomous research, and extending continuous administrative support.",
        align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=8, font_size=12)

    add_para(doc,
        "Finally, we express our profound gratitude to our families and friends for their enduring patience, moral encouragement, "
        "and support throughout the duration of this B.Tech Project for Product Development.",
        align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=24, font_size=12)

    for s_name, s_reg in STUDENTS:
        p_ak = doc.add_paragraph()
        p_ak.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        p_ak.paragraph_format.space_after = Pt(2.5)
        p_ak.paragraph_format.space_before = Pt(0)
        disp_name = s_name if s_name == "Tanmay pany" else s_name.upper()
        r_ak = p_ak.add_run(f"{disp_name} (Reg. No. - {s_reg})")
        r_ak.font.name = 'Times New Roman'
        r_ak.font.size = Pt(11)
        r_ak.bold = True

    doc.add_page_break()

    # =========================================================================
    # 5. ABSTRACT (Page iv: Exactly 1 page)
    # =========================================================================
    p_ab = doc.add_paragraph()
    p_ab.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_ab.paragraph_format.space_before = Pt(8)
    p_ab.paragraph_format.space_after = Pt(12)
    rab = p_ab.add_run("ABSTRACT")
    rab.font.name = 'Times New Roman'
    rab.font.size = Pt(20)
    rab.bold = True

    add_para(doc,
        "The World Wide Web has become the primary vector for credential harvesting, financial fraud, and malware distribution, "
        "accounting for over 70% of enterprise cyber attacks. Conventional defenses rely on centralized blocklists and reputation "
        "databases that suffer from a 12 to 72-hour zero-hour detection lag, leaving users vulnerable during critical attack phases. "
        "This project presents URLSentinel, a high-throughput, security-first cybersecurity platform combining real-time machine learning, "
        "deterministic brand protection, and blockchain-anchored evidence verification to achieve proactive zero-hour malicious URL detection.",
        align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=6, font_size=11.5)

    add_para(doc,
        "URLSentinel features a sub-millisecond lexical feature extraction engine evaluating 25+ syntactic, structural, and information-theoretic "
        "properties, including Shannon entropy, consonant-to-vowel ratios, and Public Suffix List tokenization. An algorithmic brand protection "
        "engine calculates Levenshtein edit distances against monitored enterprise brands, eliminating typosquatting attacks while maintaining an "
        "absolute 0.00% False Positive Rate on corporate Single-Sign-On portals. An Ensemble Random Forest classifier delivers 97.15% overall "
        "accuracy, 100% precision, and 94.30% recall across 2,000 verified URLs. Core analytical inference executes in 1.39 milliseconds.",
        align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=6, font_size=11.5)

    add_para(doc,
        "To guarantee forensic integrity, URLSentinel anchors SHA-256 evidence digests into an EVM smart contract ledger, creating permanent, "
        "tamper-evident audit trails. A lightweight Chromium Manifest V3 extension intercepts navigations inline without DOM overhead, while "
        "active crawler containers enforce non-root execution and strict egress firewall rules to eliminate Server-Side Request Forgery risks. "
        "URLSentinel bridges the gap between academic detection models and production cybersecurity infrastructure.",
        align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=8, font_size=11.5)

    p_kw = doc.add_paragraph()
    p_kw.paragraph_format.space_before = Pt(4)
    p_kw.paragraph_format.space_after = Pt(12)
    r_kwt = p_kw.add_run("Keywords: ")
    r_kwt.bold = True
    r_kwt.font.name = 'Times New Roman'
    r_kwt.font.size = Pt(11)
    r_kw = p_kw.add_run("Phishing Detection, Malicious URL, Machine Learning, Threat Intelligence, Blockchain, Browser Security, SSRF Prevention.")
    r_kw.font.name = 'Times New Roman'
    r_kw.font.size = Pt(11)

    for s_name, s_reg in STUDENTS:
        p_abs = doc.add_paragraph()
        p_abs.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        p_abs.paragraph_format.space_after = Pt(2)
        p_abs.paragraph_format.space_before = Pt(0)
        disp_name = s_name if s_name == "Tanmay pany" else s_name.upper()
        r_abx = p_abs.add_run(f"{disp_name} (Reg. No. - {s_reg})")
        r_abx.font.name = 'Times New Roman'
        r_abx.font.size = Pt(10.5)
        r_abx.bold = True

    doc.add_page_break()

    # =========================================================================
    # 6. TABLE OF CONTENTS (Pages v and vi: Exactly 2 pages)
    # =========================================================================
    # Part 1: Preliminary + Chapters 1-4 (Page v)
    p_t1 = doc.add_paragraph()
    p_t1.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_t1.paragraph_format.space_before = Pt(8)
    p_t1.paragraph_format.space_after = Pt(12)
    rt1 = p_t1.add_run("CONTENT")
    rt1.font.name = 'Times New Roman'
    rt1.font.size = Pt(20)
    rt1.bold = True

    toc_part1 = [
        ("CONTENTS", "PAGE NO.", True),
        ("CERTIFICATE", "i", False),
        ("DECLARATION", "ii", False),
        ("ACKNOWLEDGEMENT", "iii", False),
        ("ABSTRACT", "iv", False),
        ("CONTENTS", "v", False),
        ("LIST OF FIGURES", "vii", False),
        ("LIST OF TABLES", "viii", False),
        ("1. INTRODUCTION", "1", True),
        ("1.1 Motivation", "1", False),
        ("1.2 Problem Statement", "2", False),
        ("1.3 Objective", "2", False),
        ("1.4 Scope of the Project", "3", False),
        ("1.5 Overview of the System", "3", False),
        ("2. LITERATURE REVIEW", "4", True),
        ("2.1 Theoretical Background", "4", False),
        ("2.2 Summary of Existing Research Works", "6", False),
        ("2.3 Research Gap and Relevance to Proposed System", "7", False),
        ("3. SYSTEM ANALYSIS", "8", True),
        ("3.1 Overall Description", "8", False),
        ("3.2 Functional Requirements", "9", False),
        ("3.3 Non-Functional Requirements", "9", False),
        ("3.4 Feasibility Study", "10", False),
        ("3.4.1 Technical Feasibility", "10", False),
        ("3.4.2 Economic Feasibility", "10", False),
        ("3.4.3 Operational Feasibility", "10", False),
        ("4. METHODOLOGY", "11", True),
        ("4.1 System Workflow", "11", False),
        ("4.2 Data Collection and Processing", "11", False),
        ("4.3 URL Detection and Risk Assessment Approach", "12", False),
        ("4.4 Tools and Technologies Used", "13", False),
        ("4.5 Advantages of the Proposed Methodology", "13", False),
    ]

    tbl_c1 = doc.add_table(rows=len(toc_part1), cols=2)
    tbl_c1.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(tbl_c1)
    c_widths = [5.4, 1.1]

    for idx, (title, page_num, is_bold) in enumerate(toc_part1):
        row = tbl_c1.rows[idx]
        cell_t = row.cells[0]
        cell_p = row.cells[1]
        
        if idx == 0:
            set_cell_background(cell_t, "E2E8F0")
            set_cell_background(cell_p, "E2E8F0")
        else:
            set_cell_background(cell_t, "FFFFFF" if idx % 2 == 1 else "F8FAFC")
            set_cell_background(cell_p, "FFFFFF" if idx % 2 == 1 else "F8FAFC")

        cell_t.width = Inches(c_widths[0])
        cell_p.width = Inches(c_widths[1])

        pt = cell_t.paragraphs[0]
        pt.paragraph_format.space_before = Pt(2.5)
        pt.paragraph_format.space_after = Pt(2.5)
        pt.paragraph_format.line_spacing = 1.12
        rt = pt.add_run(title)
        rt.font.name = 'Times New Roman'
        rt.font.size = Pt(10)
        rt.bold = is_bold

        pp = cell_p.paragraphs[0]
        pp.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        pp.paragraph_format.space_before = Pt(2.5)
        pp.paragraph_format.space_after = Pt(2.5)
        pp.paragraph_format.line_spacing = 1.12
        rp = pp.add_run(page_num)
        rp.font.name = 'Times New Roman'
        rp.font.size = Pt(10)
        rp.bold = is_bold

    doc.add_page_break()

    # Part 2: Chapters 5-10 + Reference (Page vi)
    p_t2 = doc.add_paragraph()
    p_t2.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_t2.paragraph_format.space_before = Pt(8)
    p_t2.paragraph_format.space_after = Pt(12)
    rt2 = p_t2.add_run("CONTENT (Continued)")
    rt2.font.name = 'Times New Roman'
    rt2.font.size = Pt(20)
    rt2.bold = True

    toc_part2 = [
        ("CONTENTS", "PAGE NO.", True),
        ("5. SYSTEM DESIGN", "14", True),
        ("5.1 System Architecture", "14", False),
        ("5.2 Use Case Diagram", "15", False),
        ("5.3 Entity Relationship Diagram (ERD)", "16", False),
        ("5.4 Activity Diagram", "17", False),
        ("5.5 Class Diagram", "18", False),
        ("5.6 Sequence Diagram", "19", False),
        ("5.7 Data Flow Diagram (DFD)", "19", False),
        ("6. IMPLEMENTATION", "20", True),
        ("6.1 Technologies Used", "20", False),
        ("6.2 Module Description", "21", False),
        ("6.3 Algorithms Used for URL Detection and Risk Assessment", "22", False),
        ("6.4 API Endpoints", "23", False),
        ("6.5 User Interface Design", "24", False),
        ("7. TESTING", "25", True),
        ("7.1 Testing Methodology", "25", False),
        ("7.2 Test Cases", "25", False),
        ("7.3 Test Results", "26", False),
        ("7.4 Micro-Benchmark & Latency Analysis", "27", False),
        ("8. CHALLENGES AND LIMITATIONS", "28", True),
        ("8.1 Challenges Faced During Development", "28", False),
        ("8.2 Limitations of the System", "29", False),
        ("9. RESULT AND ANALYSIS", "30", True),
        ("9.1 System Results", "30", False),
        ("9.2 URL Detection Analysis", "31", False),
        ("9.3 Performance and Usability Analysis", "32", False),
        ("9.4 Advantages of the System", "32", False),
        ("10. CONCLUSION", "33", True),
        ("10.1 Conclusion", "33", False),
        ("10.2 Future Scope", "33", False),
        ("REFERENCE", "34", True),
    ]

    tbl_c2 = doc.add_table(rows=len(toc_part2), cols=2)
    tbl_c2.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(tbl_c2)

    for idx, (title, page_num, is_bold) in enumerate(toc_part2):
        row = tbl_c2.rows[idx]
        cell_t = row.cells[0]
        cell_p = row.cells[1]
        
        if idx == 0:
            set_cell_background(cell_t, "E2E8F0")
            set_cell_background(cell_p, "E2E8F0")
        else:
            set_cell_background(cell_t, "FFFFFF" if idx % 2 == 1 else "F8FAFC")
            set_cell_background(cell_p, "FFFFFF" if idx % 2 == 1 else "F8FAFC")

        cell_t.width = Inches(c_widths[0])
        cell_p.width = Inches(c_widths[1])

        pt = cell_t.paragraphs[0]
        pt.paragraph_format.space_before = Pt(2.5)
        pt.paragraph_format.space_after = Pt(2.5)
        pt.paragraph_format.line_spacing = 1.12
        rt = pt.add_run(title)
        rt.font.name = 'Times New Roman'
        rt.font.size = Pt(10)
        rt.bold = is_bold

        pp = cell_p.paragraphs[0]
        pp.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        pp.paragraph_format.space_before = Pt(2.5)
        pp.paragraph_format.space_after = Pt(2.5)
        pp.paragraph_format.line_spacing = 1.12
        rp = pp.add_run(page_num)
        rp.font.name = 'Times New Roman'
        rp.font.size = Pt(10)
        rp.bold = is_bold

    doc.add_page_break()

    # =========================================================================
    # 7. LIST OF FIGURES (Page vii: Exactly 1 page)
    # =========================================================================
    p_lf = doc.add_paragraph()
    p_lf.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_lf.paragraph_format.space_before = Pt(8)
    p_lf.paragraph_format.space_after = Pt(12)
    rlf = p_lf.add_run("List of Figure")
    rlf.font.name = 'Times New Roman'
    rlf.font.size = Pt(20)
    rlf.bold = True

    figs_list = [
        ("Sl. No.", "Figure Number", "Figure Title", "Page No.", True),
        ("01.", "Fig. 5.1", "System Architecture Diagram", "14", False),
        ("02.", "Fig. 5.2", "Use-Case Diagram", "15", False),
        ("03.", "Fig. 5.3", "Entity Relationship Diagram (ERD)", "16", False),
        ("04.", "Fig. 5.4", "Activity Diagram", "17", False),
        ("05.", "Fig. 5.5", "Class Diagram", "18", False),
        ("06.", "Fig. 5.6", "Sequence Diagram", "19", False),
        ("07.", "Fig. 5.7", "Data Flow Diagram (Level 0)", "19", False),
        ("08.", "Fig. 5.8", "Data Flow Diagram (Level 1)", "19", False),
        ("09.", "Fig. 6.1", "Feature Extraction Pipeline Architecture", "20", False),
        ("10.", "Fig. 6.2", "Blockchain Verification Workflow", "21", False),
        ("11.", "Fig. 6.3", "URLSentinel Web Dashboard Interface", "24", False),
        ("12.", "Fig. 6.4", "Live Threat Scanner Active Verdict Card", "24", False),
        ("13.", "Fig. 7.1", "Evaluation Latency Pipeline Breakdown", "27", False),
        ("14.", "Fig. 9.1", "Accuracy Comparison Between Paradigms", "31", False),
        ("15.", "Fig. 9.2", "Feature-Wise Radar Analysis", "31", False),
        ("16.", "Fig. 9.3", "Confusion Matrix Heatmap", "32", False),
    ]

    tbl_f = doc.add_table(rows=len(figs_list), cols=4)
    tbl_f.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(tbl_f)
    f_widths = [0.8, 1.4, 3.4, 0.9]

    for idx, (sl, fnum, ftitle, fpage, is_h) in enumerate(figs_list):
        row = tbl_f.rows[idx]
        for c_idx, val in enumerate([sl, fnum, ftitle, fpage]):
            cell = row.cells[c_idx]
            set_cell_background(cell, "E2E8F0" if is_h else ("FFFFFF" if idx % 2 == 1 else "F8FAFC"))
            cell.width = Inches(f_widths[c_idx])
            p = cell.paragraphs[0]
            p.paragraph_format.space_before = Pt(3)
            p.paragraph_format.space_after = Pt(3)
            p.paragraph_format.line_spacing = 1.15
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER if c_idx in [0, 1, 3] else WD_ALIGN_PARAGRAPH.LEFT
            r = p.add_run(val)
            r.font.name = 'Times New Roman'
            r.font.size = Pt(10)
            r.bold = is_h

    doc.add_page_break()

    # =========================================================================
    # 8. LIST OF TABLES (Page viii: Exactly 1 page)
    # =========================================================================
    p_lt = doc.add_paragraph()
    p_lt.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_lt.paragraph_format.space_before = Pt(8)
    p_lt.paragraph_format.space_after = Pt(12)
    rlt = p_lt.add_run("List of Tables")
    rlt.font.name = 'Times New Roman'
    rlt.font.size = Pt(20)
    rlt.bold = True

    tables_list = [
        ("Sl. No.", "Table Number", "Table Title", "Page No.", True),
        ("01.", "Table 2.1", "Research Analysis of Literature", "05", False),
        ("02.", "Table 3.1", "User Roles and Access Privileges", "08", False),
        ("03.", "Table 3.2", "Non-Functional System Specifications", "09", False),
        ("04.", "Table 6.1", "Core REST API Endpoints Specification", "23", False),
        ("05.", "Table 7.1", "Test Cases Specification", "25", False),
        ("06.", "Table 7.2", "Automated Pytest Test Suite Results", "26", False),
        ("07.", "Table 7.3", "Microsecond Latency Breakdown per Stage", "27", False),
        ("08.", "Table 9.1", "Detection Performance Comparison on 2,000 URLs", "30", False),
    ]

    tbl_t = doc.add_table(rows=len(tables_list), cols=4)
    tbl_t.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(tbl_t)
    t_widths = [0.8, 1.4, 3.4, 0.9]

    for idx, (sl, tnum, ttitle, tpage, is_h) in enumerate(tables_list):
        row = tbl_t.rows[idx]
        for c_idx, val in enumerate([sl, tnum, ttitle, tpage]):
            cell = row.cells[c_idx]
            set_cell_background(cell, "E2E8F0" if is_h else ("FFFFFF" if idx % 2 == 1 else "F8FAFC"))
            cell.width = Inches(t_widths[c_idx])
            p = cell.paragraphs[0]
            p.paragraph_format.space_before = Pt(3.5)
            p.paragraph_format.space_after = Pt(3.5)
            p.paragraph_format.line_spacing = 1.15
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER if c_idx in [0, 1, 3] else WD_ALIGN_PARAGRAPH.LEFT
            r = p.add_run(val)
            r.font.name = 'Times New Roman'
            r.font.size = Pt(10)
            r.bold = is_h

    # No page break at the end of List of Tables because Section Break follows
    print("Preliminary pages built (8 pages i-viii).")
