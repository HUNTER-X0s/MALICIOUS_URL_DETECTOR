"""
report_sections/preliminary.py - Preliminary pages for URLSentinel PPD Report
Includes: Cover Page, Certificate, Declaration, Acknowledgement, Abstract,
Contents, List of Figures, List of Tables.
"""

from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from report_sections.common import (
    ASSETS_DIR, add_para, add_heading_1, add_heading_2,
    set_cell_background, set_table_borders, style_table_header, style_table_cells
)

def build_preliminary_pages(doc):
    # ==========================================
    # 1. COVER PAGE (No header/footer, unnumbered)
    # ==========================================
    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_title.paragraph_format.space_before = Pt(0)
    p_title.paragraph_format.space_after = Pt(12)
    p_title.paragraph_format.line_spacing = 1.25
    r_title = p_title.add_run("URLSENTINEL: AI-POWERED PHISHING AND MALICIOUS URL DETECTION WITH BLOCKCHAIN-BACKED THREAT INTELLIGENCE")
    r_title.font.name = 'Times New Roman'
    r_title.font.size = Pt(16)
    r_title.bold = True

    add_para(doc, "A Project Report Submitted in Partial Fulfillment of the Requirements for the Degree of",
             align=WD_ALIGN_PARAGRAPH.CENTER, space_after=4, space_before=10, font_size=11, italic=True)

    add_para(doc, "BACHELOR OF TECHNOLOGY",
             align=WD_ALIGN_PARAGRAPH.CENTER, space_after=2, space_before=2, font_size=13, bold=True)
    add_para(doc, "IN",
             align=WD_ALIGN_PARAGRAPH.CENTER, space_after=2, space_before=0, font_size=11, bold=True)
    add_para(doc, "COMPUTER SCIENCE AND ENGINEERING",
             align=WD_ALIGN_PARAGRAPH.CENTER, space_after=14, space_before=0, font_size=13, bold=True)

    # Logo
    logo_path = ASSETS_DIR / "gcek_logo.jpeg"
    if logo_path.exists():
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.paragraph_format.space_before = Pt(4)
        p_img.paragraph_format.space_after = Pt(14)
        run_img = p_img.add_run()
        run_img.add_picture(str(logo_path), width=Inches(1.85))

    # Team & Supervisor Table
    meta_tbl = doc.add_table(rows=1, cols=2)
    meta_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    meta_tbl.autofit = False

    # Left cell: Submitted by
    c_left = meta_tbl.cell(0, 0)
    c_left.width = Inches(3.6)
    p_sub = c_left.paragraphs[0]
    p_sub.paragraph_format.line_spacing = 1.2
    p_sub.paragraph_format.space_after = Pt(2)
    r_sub = p_sub.add_run("Submitted by:\n")
    r_sub.font.name = 'Times New Roman'
    r_sub.font.size = Pt(11)
    r_sub.bold = True

    students = [
        ("Anurag Swain", "2301110017"),
        ("Subhankar Swain", "2301110077"),
        ("Tanmay pany", "2301110086"),
        ("Biduvushan Sethi", "2301110023"),
        ("Sudeep Ghosh", "2301110080"),
    ]
    for name, reg in students:
        r_item = p_sub.add_run(f"• {name} ({reg})\n")
        r_item.font.name = 'Times New Roman'
        r_item.font.size = Pt(10)

    # Right cell: Under the guidance of
    c_right = meta_tbl.cell(0, 1)
    c_right.width = Inches(3.2)
    p_guide = c_right.paragraphs[0]
    p_guide.paragraph_format.line_spacing = 1.2
    p_guide.paragraph_format.space_after = Pt(2)
    r_guide = p_guide.add_run("Under the Guidance of:\n\n")
    r_guide.font.name = 'Times New Roman'
    r_guide.font.size = Pt(11)
    r_guide.bold = True

    r_gname = p_guide.add_run("Dr. Ashok Kumar Bhoi\n")
    r_gname.font.name = 'Times New Roman'
    r_gname.font.size = Pt(11)
    r_gname.bold = True

    r_gdes = p_guide.add_run("Assistant Professor\nDept. of Computer Science & Engineering\nGCEK, Bhawanipatna")
    r_gdes.font.name = 'Times New Roman'
    r_gdes.font.size = Pt(10)
    r_gdes.italic = True

    # Footer Institution
    add_para(doc, "DEPARTMENT OF COMPUTER SCIENCE AND ENGINEERING",
             align=WD_ALIGN_PARAGRAPH.CENTER, space_after=2, space_before=16, font_size=12, bold=True)
    add_para(doc, "GOVERNMENT COLLEGE OF ENGINEERING, KALAHANDI",
             align=WD_ALIGN_PARAGRAPH.CENTER, space_after=2, space_before=0, font_size=13, bold=True)
    add_para(doc, "BHAWANIPATNA, ODISHA – 766002",
             align=WD_ALIGN_PARAGRAPH.CENTER, space_after=4, space_before=0, font_size=11, bold=True)
    add_para(doc, "NOVEMBER 2026",
             align=WD_ALIGN_PARAGRAPH.CENTER, space_after=0, space_before=4, font_size=11, bold=True)

    doc.add_page_break()

    # ==========================================
    # 2. CERTIFICATE (Page i)
    # ==========================================
    add_para(doc, "GOVERNMENT COLLEGE OF ENGINEERING, KALAHANDI",
             align=WD_ALIGN_PARAGRAPH.CENTER, space_after=2, space_before=0, font_size=13, bold=True)
    add_para(doc, "DEPARTMENT OF COMPUTER SCIENCE AND ENGINEERING",
             align=WD_ALIGN_PARAGRAPH.CENTER, space_after=2, space_before=0, font_size=11, bold=True)
    add_para(doc, "BHAWANIPATNA, ODISHA – 766002",
             align=WD_ALIGN_PARAGRAPH.CENTER, space_after=14, space_before=0, font_size=10, italic=True)

    if logo_path.exists():
        p_cimg = doc.add_paragraph()
        p_cimg.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_cimg.paragraph_format.space_before = Pt(2)
        p_cimg.paragraph_format.space_after = Pt(10)
        rc_img = p_cimg.add_run()
        rc_img.add_picture(str(logo_path), width=Inches(1.2))

    p_cert = doc.add_paragraph()
    p_cert.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_cert.paragraph_format.space_before = Pt(6)
    p_cert.paragraph_format.space_after = Pt(14)
    rc_title = p_cert.add_run("CERTIFICATE")
    rc_title.font.name = 'Times New Roman'
    rc_title.font.size = Pt(15)
    rc_title.bold = True
    rc_title.underline = True

    add_para(doc,
        "This is to certify that the project report entitled \"URLSentinel: AI-Powered Phishing and Malicious URL Detection with "
        "Blockchain-Backed Threat Intelligence\" submitted by Anurag Swain (Regd. No. 2301110017), Subhankar Swain (Regd. No. 2301110077), "
        "Tanmay pany (Regd. No. 2301110086), Biduvushan Sethi (Regd. No. 2301110023), and Sudeep Ghosh (Regd. No. 2301110080) in partial fulfillment "
        "of the requirements for the award of the degree of Bachelor of Technology in Computer Science and Engineering at Government College of "
        "Engineering, Kalahandi, Bhawanipatna, is an authentic and bona fide record of work carried out by them under my guidance and supervision.",
        align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=10, font_size=11.5)

    add_para(doc,
        "To the best of my knowledge, the matter embodied in this report has not been submitted to any other university or institute for the award "
        "of any degree or diploma. The experimental results, multi-layered machine learning architectures, and cryptographic integrity verification "
        "frameworks presented herein represent the original engineering efforts of the students.",
        align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=24, font_size=11.5)

    # Signatures
    sig_tbl = doc.add_table(rows=1, cols=3)
    sig_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    sig_tbl.autofit = False

    sig_data = [
        ("Dr. Ashok Kumar Bhoi", "Supervisor & Asst. Professor\nDept. of CSE, GCEK"),
        ("Dr. Basanta Kumar Swain", "Professor In-Charge (PPD)\nDept. of CSE, GCEK"),
        ("Dr. Gopal Behera", "Head of Department\nDept. of CSE, GCEK"),
    ]
    for idx, (s_name, s_role) in enumerate(sig_data):
        cell = sig_tbl.cell(0, idx)
        cell.width = Inches(2.2)
        cp = cell.paragraphs[0]
        cp.alignment = WD_ALIGN_PARAGRAPH.CENTER
        cp.paragraph_format.line_spacing = 1.15
        r_line = cp.add_run("_____________________\n\n")
        r_line.font.name = 'Times New Roman'
        r_name = cp.add_run(f"{s_name}\n")
        r_name.font.name = 'Times New Roman'
        r_name.font.size = Pt(10.5)
        r_name.bold = True
        r_role = cp.add_run(s_role)
        r_role.font.name = 'Times New Roman'
        r_role.font.size = Pt(9.5)

    doc.add_page_break()

    # ==========================================
    # 3. DECLARATION (Page ii)
    # ==========================================
    p_dec = doc.add_paragraph()
    p_dec.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_dec.paragraph_format.space_before = Pt(8)
    p_dec.paragraph_format.space_after = Pt(14)
    rd_title = p_dec.add_run("DECLARATION")
    rd_title.font.name = 'Times New Roman'
    rd_title.font.size = Pt(15)
    rd_title.bold = True
    rd_title.underline = True

    add_para(doc,
        "We, the undersigned final year students of Bachelor of Technology in Computer Science and Engineering, Government College of "
        "Engineering, Kalahandi, Bhawanipatna, hereby declare that the project report entitled \"URLSentinel: AI-Powered Phishing and "
        "Malicious URL Detection with Blockchain-Backed Threat Intelligence\" is an original piece of engineering work executed by us "
        "under the supervision and guidance of Dr. Ashok Kumar Bhoi, Assistant Professor, Department of Computer Science and Engineering.",
        align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=10, font_size=11.5)

    add_para(doc,
        "We further confirm that this work has not been submitted previously in part or in full for the award of any other academic degree, diploma, "
        "or fellowship at any institution. All literature sources, secondary datasets, software libraries, and external research benchmarks used "
        "during this development have been duly referenced and acknowledged in accordance with academic integrity guidelines.",
        align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=18, font_size=11.5)

    # Student signatures
    st_tbl = doc.add_table(rows=5, cols=2)
    st_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    st_tbl.autofit = False

    for r_idx, (s_name, s_reg) in enumerate(students):
        c0 = st_tbl.cell(r_idx, 0)
        c0.width = Inches(3.8)
        p0 = c0.paragraphs[0]
        p0.paragraph_format.space_after = Pt(4)
        r0 = p0.add_run(f"{s_name}\nRegistration No: {s_reg}")
        r0.font.name = 'Times New Roman'
        r0.font.size = Pt(10.5)

        c1 = st_tbl.cell(r_idx, 1)
        c1.width = Inches(2.8)
        p1 = c1.paragraphs[0]
        p1.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        p1.paragraph_format.space_after = Pt(4)
        r1 = p1.add_run("Signature: ___________________")
        r1.font.name = 'Times New Roman'
        r1.font.size = Pt(10)

    add_para(doc, "Place: Bhawanipatna, Odisha\nDate: 16th November 2026",
             align=WD_ALIGN_PARAGRAPH.LEFT, space_before=16, space_after=0, font_size=11, bold=True)

    doc.add_page_break()

    # ==========================================
    # 4. ACKNOWLEDGEMENT (Page iii)
    # ==========================================
    p_ack = doc.add_paragraph()
    p_ack.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_ack.paragraph_format.space_before = Pt(8)
    p_ack.paragraph_format.space_after = Pt(14)
    ra_title = p_ack.add_run("ACKNOWLEDGEMENT")
    ra_title.font.name = 'Times New Roman'
    ra_title.font.size = Pt(15)
    ra_title.bold = True
    ra_title.underline = True

    add_para(doc,
        "The completion of this B.Tech Project for Product Development report on \"URLSentinel: AI-Powered Phishing and Malicious URL Detection "
        "with Blockchain-Backed Threat Intelligence\" marks a significant milestone in our engineering education. We take this opportunity to express "
        "our deep gratitude to all individuals whose continuous guidance, constructive feedback, and encouragement made this endeavor possible.",
        align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=10, font_size=11.5)

    add_para(doc,
        "First and foremost, we express our profound gratitude to our project supervisor, Dr. Ashok Kumar Bhoi, Assistant Professor, Department of "
        "Computer Science and Engineering, for his invaluable technical guidance, meticulous scrutiny, and constant encouragement throughout the "
        "phases of problem identification, architectural modeling, and experimental validation.",
        align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=10, font_size=11.5)

    add_para(doc,
        "We extend our sincere thanks to Dr. Basanta Kumar Swain, Professor In-Charge, Project for Product Development (PPD), for organizing "
        "systematic reviews and establishing rigorous project milestones that kept our product engineering on schedule.",
        align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=10, font_size=11.5)

    add_para(doc,
        "We are deeply thankful to Dr. Gopal Behera, Head of the Department of Computer Science and Engineering, for providing administrative "
        "support and creating a conducive research environment within the departmental computer laboratories.",
        align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=10, font_size=11.5)

    add_para(doc,
        "We express our highest regards and respect to Prof. (Dr.) Subhransu Sekhar Dash, Principal, Government College of Engineering, Kalahandi, "
        "for his visionary leadership, continuous patronage, and provision of state-of-the-art institutional infrastructure.",
        align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=10, font_size=11.5)

    add_para(doc,
        "Finally, we express our heartfelt thanks to our parents, family members, and classmates for their unwavering moral support, patience, "
        "and encouragement throughout our undergraduate studies.",
        align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=16, font_size=11.5)

    add_para(doc, "Project Team Members:\nAnurag Swain, Subhankar Swain, Tanmay pany, Biduvushan Sethi, Sudeep Ghosh",
             align=WD_ALIGN_PARAGRAPH.RIGHT, space_before=10, space_after=0, font_size=11, bold=True)

    doc.add_page_break()

    # ==========================================
    # 5. ABSTRACT (Page iv - VERBATIM FROM PROMPT)
    # ==========================================
    p_abs = doc.add_paragraph()
    p_abs.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_abs.paragraph_format.space_before = Pt(8)
    p_abs.paragraph_format.space_after = Pt(12)
    rab_title = p_abs.add_run("ABSTRACT")
    rab_title.font.name = 'Times New Roman'
    rab_title.font.size = Pt(15)
    rab_title.bold = True
    rab_title.underline = True

    add_para(doc, "Project Title : URLSentinel : AI-Powered Phishing and Malicious URL Detection with Blockchain-Backed Threat Intelligence",
             space_after=4, space_before=0, font_size=11, bold=True)
    add_para(doc, "Domain : AI/ML, Cybersecurity, Cloud Computing & Networking, Blockchain Technology, Browser Security, and Web Application Security",
             space_after=10, space_before=0, font_size=11, bold=True)

    add_para(doc,
        "The proposed system is an AI-powered cybersecurity platform for detecting and analyzing phishing, malicious, and suspicious URLs "
        "before they can cause harm to users. The system accepts a URL through a web dashboard, public API, or browser extension and evaluates "
        "it using a multi-layered detection pipeline that combines machine learning, threat intelligence, domain and network analysis, and "
        "explainable risk assessment. The machine-learning engine extracts lexical and structural URL features such as length, subdomain depth, "
        "special-character patterns, entropy, IP-based addressing, URL encoding, suspicious tokens, and typosquatting indicators, while external "
        "threat intelligence sources, DNS and domain metadata, TLS information, redirects, and reputation signals provide additional evidence. "
        "These signals are aggregated by a risk engine to generate a calibrated risk score, threat classification, confidence level, and "
        "human-readable explanation of the factors contributing to the decision. For active website analysis, untrusted URLs are processed in "
        "isolated and disposable scanning environments designed to limit SSRF, sandbox-escape, credential-exposure, and lateral-movement risks; "
        "the production application, databases, secrets, and blockchain signing infrastructure remain separated from the scanning environment. "
        "A browser-extension layer provides real-time protection by evaluating the current navigation and presenting safe, suspicious, or dangerous "
        "verdicts with user warnings when appropriate. To improve trust, auditability, and tamper evidence, the platform can cryptographically "
        "sign authoritative verdicts and store hashes of selected threat evidence and reports on a blockchain-backed registry, while detailed "
        "operational data remains in an off-chain database. The architecture therefore combines AI-based detection, automated threat intelligence, "
        "secure malware-analysis isolation, verifiable security results, and continuous monitoring into a unified platform. Evaluation focuses "
        "on detection precision, recall, F1-score, false-positive and false-negative rates, response latency, threat-intelligence agreement, "
        "and scanner containment effectiveness. The proposed system demonstrates a practical approach to building a scalable and defensible "
        "web-threat detection service capable of supporting end users, browser-based protection, and future community-driven threat intelligence sharing.",
        align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=10, font_size=11.5)

    add_para(doc,
        "Keywords: Phishing Detection, Malicious URL Detection, Machine Learning, Threat Intelligence, URL Risk Scoring, Browser Extension, "
        "Secure Sandbox, SSRF Protection, Cryptographic Verification, Blockchain",
        space_after=10, space_before=4, font_size=11, bold=True)

    add_para(doc,
        "Team Members: Anurag Swain (Reg. No. 2301110017), Subhankar Swain (Reg. No. 2301110077), Tanmay pany (Reg. No. 2301110086), "
        "Biduvushan Sethi (Reg. No. 2301110023), Sudeep Ghosh (Reg. No. 2301110080)",
        space_after=0, space_before=4, font_size=10.5, italic=True)

    doc.add_page_break()

    # ==========================================
    # 6. CONTENTS (Page v)
    # ==========================================
    p_toc = doc.add_paragraph()
    p_toc.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_toc.paragraph_format.space_before = Pt(8)
    p_toc.paragraph_format.space_after = Pt(12)
    rt_title = p_toc.add_run("CONTENTS")
    rt_title.font.name = 'Times New Roman'
    rt_title.font.size = Pt(15)
    rt_title.bold = True
    rt_title.underline = True

    toc_items = [
        ("Certificate", "i"),
        ("Declaration", "ii"),
        ("Acknowledgement", "iii"),
        ("Abstract", "iv"),
        ("List of Figures", "vi"),
        ("List of Tables", "vii"),
        ("CHAPTER 1: INTRODUCTION", "1"),
        ("    1.1 Motivation", "1"),
        ("    1.2 Problem Statement", "2"),
        ("    1.3 Objective", "3"),
        ("    1.4 Scope of the Project", "4"),
        ("    1.5 Overview of the System", "5"),
        ("CHAPTER 2: LITERATURE REVIEW", "7"),
        ("    2.1 Theoretical Background", "7"),
        ("    2.2 Summary of Existing Research Works (Table 2.1 Research Analysis)", "9"),
        ("    2.3 Research Gap and Relevance to Proposed System", "12"),
        ("CHAPTER 3: SYSTEM ANALYSIS", "14"),
        ("    3.1 Overall Description (Table 3.1 User Roles)", "14"),
        ("    3.2 Functional Requirements (FR-01 to FR-12)", "15"),
        ("    3.3 Non-Functional Requirements (Table 3.2 Non-Functional Specs)", "17"),
        ("    3.4 Feasibility Study", "19"),
        ("        3.4.1 Technical Feasibility", "19"),
        ("        3.4.2 Economic Feasibility", "20"),
        ("        3.4.3 Operational Feasibility", "20"),
        ("CHAPTER 4: METHODOLOGY", "22"),
        ("    4.1 System Workflow", "22"),
        ("    4.2 Data Collection and Processing", "23"),
        ("    4.3 URL Detection and Risk Assessment Approach", "25"),
        ("    4.4 Tools and Technologies Used", "27"),
        ("    4.5 Advantages of the Proposed Methodology", "28"),
        ("CHAPTER 5: SYSTEM DESIGN", "30"),
        ("    5.1 System Architecture", "30"),
        ("    5.2 Use Case Diagram", "32"),
        ("    5.3 Entity Relationship Diagram", "33"),
        ("    5.4 Activity Diagram", "35"),
        ("    5.5 Class Diagram", "36"),
        ("    5.6 Sequence Diagram", "38"),
        ("    5.7 Data Flow Diagram (Level 0 and Level 1)", "39"),
        ("CHAPTER 6: IMPLEMENTATION", "42"),
        ("    6.1 Technologies Used", "42"),
        ("    6.2 Module Description", "44"),
        ("    6.3 Algorithms Used for URL Detection and Risk Assessment", "47"),
        ("    6.4 API Endpoints (Table 6.1 API Specification)", "51"),
        ("    6.5 User Interface Design", "53"),
        ("CHAPTER 7: TESTING", "57"),
        ("    7.1 Testing Methodology", "57"),
        ("    7.2 Test Cases (Table 7.1 Detailed Test Cases)", "58"),
        ("    7.3 Test Results (Table 7.2 Results Summary)", "61"),
        ("    7.4 Performance Analysis", "62"),
        ("CHAPTER 8: CHALLENGES AND LIMITATIONS", "64"),
        ("    8.1 Challenges Faced During Development", "64"),
        ("    8.2 Limitations of the System", "66"),
        ("CHAPTER 9: RESULT AND ANALYSIS", "68"),
        ("    9.1 System Results", "68"),
        ("    9.2 URL Detection and Classification Analysis (2,000 URLs Evaluation)", "69"),
        ("    9.3 Performance and Usability Analysis", "72"),
        ("    9.4 Advantages of the System", "73"),
        ("CHAPTER 10: CONCLUSION", "75"),
        ("    10.1 Conclusion", "75"),
        ("    10.2 Future Scope", "76"),
        ("REFERENCES", "78"),
    ]

    toc_tbl = doc.add_table(rows=len(toc_items) + 1, cols=2)
    toc_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(toc_tbl)

    hdr = toc_tbl.rows[0]
    hdr.cells[0].paragraphs[0].add_run("Topic / Chapter Title")
    hdr.cells[1].paragraphs[0].add_run("Page No.")
    style_table_header(hdr, [5.5, 1.1])

    for idx, (title, page) in enumerate(toc_items):
        row = toc_tbl.rows[idx + 1]
        c0 = row.cells[0]
        c1 = row.cells[1]
        p0 = c0.paragraphs[0]
        p1 = c1.paragraphs[0]
        p1.alignment = WD_ALIGN_PARAGRAPH.RIGHT

        r0 = p0.add_run(title)
        r0.font.name = 'Times New Roman'
        r0.font.size = Pt(10)
        if title.startswith("CHAPTER") or title in ["Certificate", "Declaration", "Acknowledgement", "Abstract", "REFERENCES"]:
            r0.bold = True

        r1 = p1.add_run(page)
        r1.font.name = 'Times New Roman'
        r1.font.size = Pt(10)
        if title.startswith("CHAPTER") or title in ["Certificate", "Declaration", "Acknowledgement", "Abstract", "REFERENCES"]:
            r1.bold = True

    style_table_cells(toc_tbl, [5.5, 1.1])
    doc.add_page_break()

    # ==========================================
    # 7. LIST OF FIGURES (Page vi)
    # ==========================================
    p_lof = doc.add_paragraph()
    p_lof.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_lof.paragraph_format.space_before = Pt(8)
    p_lof.paragraph_format.space_after = Pt(12)
    rl_title = p_lof.add_run("LIST OF FIGURES")
    rl_title.font.name = 'Times New Roman'
    rl_title.font.size = Pt(15)
    rl_title.bold = True
    rl_title.underline = True

    fig_items = [
        ("Figure 5.1", "URLSentinel Overall System Architecture Diagram", "31"),
        ("Figure 5.2", "System Use Case Diagram with User Roles and Operational Boundaries", "33"),
        ("Figure 5.3", "Database Entity Relationship Diagram (Off-Chain Schema & Blockchain Anchors)", "34"),
        ("Figure 5.4", "URL Sentinel Activity Diagram (End-to-End Evaluation Workflow)", "36"),
        ("Figure 5.5", "Core Object-Oriented Class Diagram for Detection & Risk Engines", "37"),
        ("Figure 5.6", "System Sequence Diagram for Concurrent Multi-Engine URL Evaluation", "38"),
        ("Figure 5.7", "Data Flow Diagram Level 0 (Context Level Architecture)", "40"),
        ("Figure 5.8", "Data Flow Diagram Level 1 (Engine Pipeline & Sandbox Isolation Decomposition)", "41"),
        ("Figure 6.1", "Multi-Stage URL Feature Extraction Pipeline Architecture", "45"),
        ("Figure 6.2", "Cryptographic Verdict Attestation and Blockchain Verification Workflow", "46"),
        ("Figure 6.3", "URLSentinel Live Web Homepage Interface (FORTRESS v2.0 Production UI)", "54"),
        ("Figure 6.4", "URLSentinel Live Threat Scanner Active Verdict Card with Dynamic SVG Gauge", "55"),
        ("Figure 6.5", "URLSentinel Security Center & Zero-Trust SSRF Egress Isolation Specifications", "56"),
        ("Figure 6.6", "URLSentinel Zero-Retention Privacy Policy and Data Governance Center", "56"),
        ("Figure 6.7", "Interactive OpenAPI / Swagger Documentation Interface (/docs)", "57"),
        ("Figure 6.8", "Chromium Manifest V3 Browser Extension Real-Time Interception Warning Interface", "57"),
        ("Figure 7.1", "End-to-End Latency Pipeline Breakdown Across Analysis Engines", "63"),
        ("Figure 9.1", "Overall Detection Accuracy Comparison Across Paradigms (2,000 URLs Evaluation)", "70"),
        ("Figure 9.2", "Eight-Dimensional Radar Analysis of Detection Capabilities", "71"),
        ("Figure 9.3", "Confusion Matrix Heatmap for URLSentinel v2.1 (2,000 URL Benchmark)", "72"),
    ]

    fig_tbl = doc.add_table(rows=len(fig_items) + 1, cols=3)
    fig_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(fig_tbl)

    fhdr = fig_tbl.rows[0]
    fhdr.cells[0].paragraphs[0].add_run("Figure No.")
    fhdr.cells[1].paragraphs[0].add_run("Caption / Description")
    fhdr.cells[2].paragraphs[0].add_run("Page No.")
    style_table_header(fhdr, [1.3, 4.4, 0.9])

    for idx, (f_num, f_desc, f_pg) in enumerate(fig_items):
        row = fig_tbl.rows[idx + 1]
        c0, c1, c2 = row.cells[0], row.cells[1], row.cells[2]
        c2.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.RIGHT

        r0 = c0.paragraphs[0].add_run(f_num)
        r0.font.name = 'Times New Roman'
        r0.font.size = Pt(10)
        r0.bold = True

        r1 = c1.paragraphs[0].add_run(f_desc)
        r1.font.name = 'Times New Roman'
        r1.font.size = Pt(10)

        r2 = c2.paragraphs[0].add_run(f_pg)
        r2.font.name = 'Times New Roman'
        r2.font.size = Pt(10)

    style_table_cells(fig_tbl, [1.3, 4.4, 0.9])
    doc.add_page_break()

    # ==========================================
    # 8. LIST OF TABLES (Page vii)
    # ==========================================
    p_lot = doc.add_paragraph()
    p_lot.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_lot.paragraph_format.space_before = Pt(8)
    p_lot.paragraph_format.space_after = Pt(12)
    rlt_title = p_lot.add_run("LIST OF TABLES")
    rlt_title.font.name = 'Times New Roman'
    rlt_title.font.size = Pt(15)
    rlt_title.bold = True
    rlt_title.underline = True

    tbl_items = [
        ("Table 2.1", "Research Analysis of Existing Malicious URL and Phishing Detection Works", "10"),
        ("Table 3.1", "URLSentinel User Roles, Access Privileges, and Functional Responsibilities", "15"),
        ("Table 3.2", "Non-Functional System Specifications and Operational Quality Attributes", "18"),
        ("Table 6.1", "URLSentinel Core REST API Endpoints Specification", "52"),
        ("Table 7.1", "Comprehensive Test Suite Specification (TC-01 through TC-14)", "59"),
        ("Table 7.2", "Automated Pytest Test Suite Results and Quality Gate Verification Summary", "61"),
    ]

    tbl_tbl = doc.add_table(rows=len(tbl_items) + 1, cols=3)
    tbl_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(tbl_tbl)

    thdr = tbl_tbl.rows[0]
    thdr.cells[0].paragraphs[0].add_run("Table No.")
    thdr.cells[1].paragraphs[0].add_run("Description / Title")
    thdr.cells[2].paragraphs[0].add_run("Page No.")
    style_table_header(thdr, [1.3, 4.4, 0.9])

    for idx, (t_num, t_desc, t_pg) in enumerate(tbl_items):
        row = tbl_tbl.rows[idx + 1]
        c0, c1, c2 = row.cells[0], row.cells[1], row.cells[2]
        c2.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.RIGHT

        r0 = c0.paragraphs[0].add_run(t_num)
        r0.font.name = 'Times New Roman'
        r0.font.size = Pt(10)
        r0.bold = True

        r1 = c1.paragraphs[0].add_run(t_desc)
        r1.font.name = 'Times New Roman'
        r1.font.size = Pt(10)

        r2 = c2.paragraphs[0].add_run(t_pg)
        r2.font.name = 'Times New Roman'
        r2.font.size = Pt(10)

    style_table_cells(tbl_tbl, [1.3, 4.4, 0.9])
    doc.add_page_break()

    print("Preliminary pages built successfully.")
