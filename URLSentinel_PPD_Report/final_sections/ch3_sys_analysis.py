"""
final_sections/ch3_sys_analysis.py - 3. SYSTEM ANALYSIS (Target: 3 pages, pp. 8-10)
"""

from docx.shared import Inches, Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from report_sections.common import (
    add_para, add_bullet, set_cell_background, set_table_borders,
    style_table_header, style_table_cells
)

def build_ch3(doc):
    # 3. SYSTEM ANALYSIS
    p_h = doc.add_paragraph()
    p_h.paragraph_format.space_before = Pt(0)
    p_h.paragraph_format.space_after = Pt(10)
    p_h.paragraph_format.keep_with_next = True
    r = p_h.add_run("3. SYSTEM ANALYSIS")
    r.font.name = 'Times New Roman'
    r.font.size = Pt(20)
    r.bold = True

    # 3.1 Overall Description
    p_sub = doc.add_paragraph()
    p_sub.paragraph_format.space_before = Pt(8)
    p_sub.paragraph_format.space_after = Pt(4)
    p_sub.paragraph_format.keep_with_next = True
    r = p_sub.add_run("3.1 Overall Description")
    r.font.name = 'Times New Roman'
    r.font.size = Pt(16)
    r.bold = True

    add_para(doc,
        "URLSentinel is an enterprise-grade cybersecurity platform that automates real-time detection, forensic analysis, and cryptographic "
        "auditability of malicious and phishing web destinations. The system operates across three interconnected operational layers: "
        "a client-facing presentation layer (web dashboard and Chromium browser extension), an asynchronous API gateway and detection engine "
        "(FastAPI and Scikit-learn), and an immutable ledger and caching layer (Redis and Ethereum smart contracts). "
        "The system serves four primary user roles, each possessing distinct operational privileges as outlined in Table 3.1.")

    p_t31 = doc.add_paragraph()
    p_t31.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_t31.paragraph_format.space_before = Pt(6)
    p_t31.paragraph_format.space_after = Pt(3)
    p_t31.paragraph_format.keep_with_next = True
    rt = p_t31.add_run("Table 3.1: User Role")
    rt.font.name = 'Times New Roman'
    rt.font.size = Pt(11)
    rt.bold = True

    roles = [
        ("User Role", "Access Privilege", "Key Capabilities & Responsibilities"),
        ("End User\n(Consumer/Employee)", "Client-side / Low", "Submit on-demand URL scans; browse with active browser extension protection; receive real-time interstitial warnings on dangerous links; view risk factors."),
        ("Security Analyst\n(SOC Incident Responder)", "Audit / Medium-High", "Inspect deep forensic telemetry (entropy scores, DGA ratios, token lengths); export structured threat reports in JSON; verify blockchain evidence receipts."),
        ("Platform Administrator\n(System Engineer)", "Full Administrative", "Manage threat feed synchronization crons; trigger model retraining pipelines; configure rate limits; monitor container health; oversee smart contracts."),
        ("Enterprise API Client\n(M2M Integration)", "Token-Authenticated", "Submit high-throughput batch URL scans; consume automated machine-readable JSON verdicts; integrate threat feeds into email gateways and SIEM firewalls."),
    ]

    tbl_r = doc.add_table(rows=len(roles), cols=3)
    tbl_r.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(tbl_r)
    rw = [1.8, 1.5, 3.2]

    for idx, (r_name, r_priv, r_cap) in enumerate(roles):
        row = tbl_r.rows[idx]
        for c_idx, val in enumerate([r_name, r_priv, r_cap]):
            cell = row.cells[c_idx]
            set_cell_background(cell, "E2E8F0" if idx == 0 else ("FFFFFF" if idx % 2 == 1 else "F8FAFC"))
            cell.width = Inches(rw[c_idx])
            p = cell.paragraphs[0]
            p.paragraph_format.space_before = Pt(3)
            p.paragraph_format.space_after = Pt(3)
            p.paragraph_format.line_spacing = 1.12
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER if c_idx == 1 or idx == 0 else WD_ALIGN_PARAGRAPH.LEFT
            r = p.add_run(val)
            r.font.name = 'Times New Roman'
            r.font.size = Pt(9.5)
            r.bold = (idx == 0)

    # 3.2 Functional Requirements
    p_sub = doc.add_paragraph()
    p_sub.paragraph_format.space_before = Pt(10)
    p_sub.paragraph_format.space_after = Pt(4)
    p_sub.paragraph_format.keep_with_next = True
    r = p_sub.add_run("3.2 Functional Requirements")
    r.font.name = 'Times New Roman'
    r.font.size = Pt(16)
    r.bold = True

    add_para(doc, "The functional requirements describe the fundamental operational capabilities of the platform:")
    add_bullet("FR-01 (Multi-Channel Ingestion): Accept candidate URLs via web interface, REST API (/api/v1/scan), or browser extension.")
    add_bullet("FR-02 (Canonical Normalization): Perform RFC 3986 canonicalization, resolving percent-encodings and converting Punycode IDN glyphs.")
    add_bullet("FR-03 (Lexical Feature Extraction): Compute 25+ structural metrics, including length, path depth, and special character counts in <1.5 ms.")
    add_bullet("FR-04 (Entropy Computation): Calculate Shannon entropy H(S) across domain and path tokens to detect randomized obfuscation.")
    add_bullet("FR-05 (Brand Protection): Compute Levenshtein distance against 50+ high-value corporate brands to flag typosquatting.")
    add_bullet("FR-06 (DGA Analysis): Measure consonant-to-vowel distribution ratios to identify algorithmically generated domain names.")
    add_bullet("FR-07 (ML Classification): Evaluate feature vectors with an Ensemble Random Forest to predict malicious probability P(malicious).")
    add_bullet("FR-08 (Threat Intel Matching): Query in-memory threat feeds (URLhaus, OpenPhish) with O(1) hash matching.")
    add_bullet("FR-09 (Risk Engine Synthesis): Aggregate ML probabilities, heuristics, and feed data into a normalized score (0–100) and verdict.")
    add_bullet("FR-10 (Explainable Risk Telemetry): Generate plain-language justifications detailing exact risk factors contributing to the score.")
    add_bullet("FR-11 (Browser Navigation Interception): Intercept malicious links before DOM rendering via Manifest V3 and display warning screens.")
    add_bullet("FR-12 (Blockchain Evidence Anchoring): Compute SHA-256 evidence digests and anchor verdicts to an EVM smart contract ledger.")

    # 3.3 Non-Functional Requirements
    p_sub = doc.add_paragraph()
    p_sub.paragraph_format.space_before = Pt(10)
    p_sub.paragraph_format.space_after = Pt(4)
    p_sub.paragraph_format.keep_with_next = True
    r = p_sub.add_run("3.3 Non-Functional Requirements")
    r.font.name = 'Times New Roman'
    r.font.size = Pt(16)
    r.bold = True

    add_para(doc, "Table 3.2 details the operational quality attributes, latency constraints, and security standards enforced by the system.")

    p_t32 = doc.add_paragraph()
    p_t32.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_t32.paragraph_format.space_before = Pt(6)
    p_t32.paragraph_format.space_after = Pt(3)
    p_t32.paragraph_format.keep_with_next = True
    rt2 = p_t32.add_run("Table 3.2: Non-Functional Requirement Table")
    rt2.font.name = 'Times New Roman'
    rt2.font.size = Pt(11)
    rt2.bold = True

    nfrs = [
        ("Attribute", "Requirement"),
        ("Performance", "Core feature extraction <1.5 ms; total API response latency <50 ms; browser extension lookup <20 ms."),
        ("Scalability", "Asynchronous stateless architecture supporting >1,000 requests/sec under horizontal worker scaling."),
        ("Usability", "FORTRESS v2.0 high-contrast UI; WCAG 2.1 AA compliance; responsive dark/light layout with dynamic SVG gauges."),
        ("Maintainability", "Fully typed codebase with Python Pydantic v2 and TypeScript; modular containerized microservices."),
        ("Reliability", "99.9% uptime target; Redis caching with in-memory fallback; graceful degradation under external feed failures."),
        ("Availability", "Accessible anytime via cloud/Docker deployment; healthcheck probe (/healthz) for automated orchestrators."),
    ]

    tbl_n = doc.add_table(rows=len(nfrs), cols=2)
    tbl_n.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(tbl_n)
    nw = [2.0, 4.5]

    for idx, (attr, req) in enumerate(nfrs):
        row = tbl_n.rows[idx]
        for c_idx, val in enumerate([attr, req]):
            cell = row.cells[c_idx]
            set_cell_background(cell, "E2E8F0" if idx == 0 else ("FFFFFF" if idx % 2 == 1 else "F8FAFC"))
            cell.width = Inches(nw[c_idx])
            p = cell.paragraphs[0]
            p.paragraph_format.space_before = Pt(3)
            p.paragraph_format.space_after = Pt(3)
            p.paragraph_format.line_spacing = 1.12
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER if c_idx == 0 or idx == 0 else WD_ALIGN_PARAGRAPH.LEFT
            r = p.add_run(val)
            r.font.name = 'Times New Roman'
            r.font.size = Pt(9.5)
            r.bold = (idx == 0)

    # 3.4 Feasibility Study
    p_sub = doc.add_paragraph()
    p_sub.paragraph_format.space_before = Pt(10)
    p_sub.paragraph_format.space_after = Pt(4)
    p_sub.paragraph_format.keep_with_next = True
    r = p_sub.add_run("3.4 Feasibility Study")
    r.font.name = 'Times New Roman'
    r.font.size = Pt(16)
    r.bold = True

    add_para(doc, "A three-part feasibility assessment confirmed the practical viability of implementing URLSentinel at GCEK:")

    p_f1 = doc.add_paragraph()
    p_f1.paragraph_format.space_before = Pt(4)
    p_f1.paragraph_format.space_after = Pt(2)
    p_f1.paragraph_format.keep_with_next = True
    rf1 = p_f1.add_run("3.4.1 Technical Feasibility")
    rf1.font.name = 'Times New Roman'
    rf1.font.size = Pt(13)
    rf1.bold = True
    add_para(doc,
        "The system utilizes widely supported, mature open-source technologies: Python 3.12, FastAPI, Scikit-learn, Next.js 14, and Chromium "
        "WebExtensions APIs. Hardware requirements are minimal, executing comfortably on standard 2-vCPU / 4GB RAM servers without GPU dependency.")

    p_f2 = doc.add_paragraph()
    p_f2.paragraph_format.space_before = Pt(4)
    p_f2.paragraph_format.space_after = Pt(2)
    p_f2.paragraph_format.keep_with_next = True
    rf2 = p_f2.add_run("3.4.2 Economic Feasibility")
    rf2.font.name = 'Times New Roman'
    rf2.font.size = Pt(13)
    rf2.bold = True
    add_para(doc,
        "Development and operational costs are near zero. All libraries, frameworks, and threat intelligence feeds (URLhaus, OpenPhish) "
        "are open-source and free for educational and research usage. Blockchain verification is executed on a local EVM network, eliminating gas fees.")

    p_f3 = doc.add_paragraph()
    p_f3.paragraph_format.space_before = Pt(4)
    p_f3.paragraph_format.space_after = Pt(2)
    p_f3.paragraph_format.keep_with_next = True
    rf3 = p_f3.add_run("3.4.3 Operational Feasibility")
    rf3.font.name = 'Times New Roman'
    rf3.font.size = Pt(13)
    rf3.bold = True
    add_para(doc,
        "The system requires zero user training. The browser extension operates autonomously in the background, and the web scanner "
        "features an intuitive, role-based design suitable for both non-technical consumers and enterprise SOC analysts.")

    doc.add_page_break()
    print("Chapter 3 built (pages 8-10).")
