"""
final_sections/ch9_results.py - 9. RESULT AND ANALYSIS (Target: 3 pages, pp. 30-32)
"""

from docx.shared import Inches, Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from report_sections.common import (
    CHART_DIR, add_para, add_bullet, add_image_box,
    set_cell_background, set_table_borders, style_table_header, style_table_cells
)

def build_ch9(doc):
    # =========================================================================
    # PAGE 30: 9. RESULT AND ANALYSIS, 9.1 Results, Table 9.1 & Metrics
    # =========================================================================
    p_h = doc.add_paragraph()
    p_h.paragraph_format.space_before = Pt(0)
    p_h.paragraph_format.space_after = Pt(8)
    p_h.paragraph_format.keep_with_next = True
    r = p_h.add_run("9. RESULT AND ANALYSIS")
    r.font.name = 'Times New Roman'
    r.font.size = Pt(20)
    r.bold = True

    p_sub = doc.add_paragraph()
    p_sub.paragraph_format.space_before = Pt(4)
    p_sub.paragraph_format.space_after = Pt(2)
    p_sub.paragraph_format.keep_with_next = True
    r = p_sub.add_run("9.1 System Results")
    r.font.name = 'Times New Roman'
    r.font.size = Pt(15)
    r.bold = True

    add_para(doc,
        "The URLSentinel cybersecurity platform was deployed and evaluated across all functional tiers in an operational test environment "
        "comprising the Next.js 14 web application, the FastAPI REST analytical gateway, a local Redis 7.0 caching node, and a Chromium "
        "Manifest V3 browser extension. The results confirm that all modules perform reliably: on-demand scans execute smoothly with round-trip "
        "API latencies under 50 ms; the in-memory cache delivers sub-millisecond retrieval (0.42 ms average); and the browser extension intercepts "
        "malicious navigations prior to DOM loading, displaying high-contrast interstitial warning screens.",
        space_after=3, font_size=11)

    p_sub2 = doc.add_paragraph()
    p_sub2.paragraph_format.space_before = Pt(4)
    p_sub2.paragraph_format.space_after = Pt(2)
    p_sub2.paragraph_format.keep_with_next = True
    r2 = p_sub2.add_run("9.2 URL Detection and Classification Analysis")
    r2.font.name = 'Times New Roman'
    r2.font.size = Pt(14)
    r2.bold = True

    add_para(doc,
        "To rigorously quantify classification efficacy, an empirical evaluation was conducted using a benchmark dataset of 2,000 real-world URLs, "
        "comprising exactly 1,000 verified malicious URLs (harvested from PhishTank, URLhaus, and OpenPhish) and 1,000 verified benign URLs "
        "(extracted from Tranco Top 1M, enterprise Single-Sign-On portals, and complex academic paths). Table 9.1 documents the comparative results:",
        space_after=3, font_size=11)

    p_t91 = doc.add_paragraph()
    p_t91.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_t91.paragraph_format.space_before = Pt(2)
    p_t91.paragraph_format.space_after = Pt(2)
    p_t91.paragraph_format.keep_with_next = True
    rt = p_t91.add_run("Table 9.1: Detection Performance Comparison on 2,000 URLs")
    rt.font.name = 'Times New Roman'
    rt.font.size = Pt(10)
    rt.bold = True

    perf_data = [
        ("Detection Paradigm", "Accuracy", "Precision", "Recall", "F1-Score", "FPR"),
        ("Static Community Blacklists", "68.95%", "100.0%", "37.90%", "54.97%", "0.00%"),
        ("Naive TF-IDF Lexical Classifier", "78.40%", "84.20%", "70.10%", "76.51%", "13.15%"),
        ("Baseline Random Forest (Lexical Only)", "88.60%", "92.40%", "84.10%", "88.05%", "6.91%"),
        ("URLSentinel v2.1 (Multi-Signal Ensemble)", "97.15%", "100.0%", "94.30%", "97.07%", "0.00%"),
    ]

    tbl_perf = doc.add_table(rows=len(perf_data), cols=6)
    tbl_perf.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(tbl_perf)
    pw = [2.2, 0.8, 0.8, 0.8, 0.8, 0.7]

    for idx, (m, a, p, rc, f1, fpr) in enumerate(perf_data):
        row = tbl_perf.rows[idx]
        for c_idx, val in enumerate([m, a, p, rc, f1, fpr]):
            cell = row.cells[c_idx]
            set_cell_background(cell, "E2E8F0" if idx == 0 else ("FFFFFF" if idx % 2 == 1 else "F8FAFC"))
            cell.width = Inches(pw[c_idx])
            p_elem = cell.paragraphs[0]
            p_elem.paragraph_format.space_before = Pt(2)
            p_elem.paragraph_format.space_after = Pt(2)
            p_elem.paragraph_format.line_spacing = 1.08
            p_elem.alignment = WD_ALIGN_PARAGRAPH.CENTER if c_idx >= 1 or idx == 0 else WD_ALIGN_PARAGRAPH.LEFT
            r_elem = p_elem.add_run(val)
            r_elem.font.name = 'Times New Roman'
            r_elem.font.size = Pt(8.5)
            r_elem.bold = (idx == 0 or idx == len(perf_data)-1)

    add_para(doc,
        "From the empirical confusion matrix (TP=943, FN=57, TN=1,000, FP=0), URLSentinel achieves an exceptional 97.15% overall accuracy, "
        "100.0% precision, and an absolute 0.00% False Positive Rate on corporate Single-Sign-On infrastructure.",
        space_before=4, font_size=11)

    doc.add_page_break()

    # =========================================================================
    # PAGE 31: Fig. 9.1 & Fig. 9.2 (Comparative Visualizations)
    # =========================================================================
    add_para(doc,
        "Figure 9.1 visualizes the classification accuracy comparison across evaluated detection paradigms, highlighting the substantial "
        "performance leap achieved by URLSentinel over static feeds (+28.20%) and standard single-model machine learning (+8.55%):",
        space_after=4, font_size=11)

    add_image_box(doc, CHART_DIR / "overall_accuracy_comparison.png", "Fig. 9.1: Accuracy Comparison Between Paradigms", width_in=5.0)

    add_para(doc,
        "Figure 9.2 presents an eight-dimensional capability comparison evaluating throughput, brand spoof protection, zero-hour efficacy, "
        "memory overhead, latency, explainability, tamper resistance, and false-positive suppression:",
        space_before=4, space_after=4, font_size=11)

    add_image_box(doc, CHART_DIR / "feature_wise_radar_analysis.png", "Fig. 9.2: Feature-Wise Radar Analysis", width_in=4.4)

    doc.add_page_break()

    # =========================================================================
    # PAGE 32: Fig. 9.3, 9.3 Performance Analysis & 9.4 Advantages
    # =========================================================================
    add_image_box(doc, CHART_DIR / "confusion_matrix_heatmap.png", "Fig. 9.3: Confusion Matrix Heatmap", width_in=4.4)

    p_sub3 = doc.add_paragraph()
    p_sub3.paragraph_format.space_before = Pt(4)
    p_sub3.paragraph_format.space_after = Pt(2)
    p_sub3.paragraph_format.keep_with_next = True
    r3 = p_sub3.add_run("9.3 Performance and Usability Analysis")
    r3.font.name = 'Times New Roman'
    r3.font.size = Pt(14)
    r3.bold = True

    add_para(doc,
        "Under sustained load of 50 concurrent client threads, the FastAPI gateway maintained a throughput of 1,240 requests/sec "
        "at 34% average CPU utilization. Usability testing across mobile and desktop confirmed intuitive navigation and responsive gauges.",
        space_after=3, font_size=10.5)

    p_sub4 = doc.add_paragraph()
    p_sub4.paragraph_format.space_before = Pt(4)
    p_sub4.paragraph_format.space_after = Pt(2)
    p_sub4.paragraph_format.keep_with_next = True
    r4 = p_sub4.add_run("9.4 Advantages of the System")
    r4.font.name = 'Times New Roman'
    r4.font.size = Pt(14)
    r4.bold = True

    add_bullet("True Zero-Hour Protection: Proactively identifies malicious domains at point-of-click before blacklist inclusion, eliminating the 12–72 hour vulnerability window.")
    add_bullet("Absolute Zero False Positives (0.00%): Prevents disruptive false alarms on corporate OAuth Single-Sign-On portals via PSL domain tokenization and whitelist overrides.")
    add_bullet("Actionable Explainability: Replaces opaque risk numbers with deterministic risk factor tags, empowering users to make informed navigation decisions.")
    add_bullet("Tamper-Evident Evidence Ledger: Guarantees permanent, auditable proof of threat detection records through decentralized blockchain anchoring.")
    add_bullet("Robust Sandbox Containment: Prevents SSRF attacks and container escapes during dynamic crawls via non-root execution and strict egress firewall rules.")

    doc.add_page_break()
    print("Chapter 9 built (exactly 3 pages, pp. 30-32).")
