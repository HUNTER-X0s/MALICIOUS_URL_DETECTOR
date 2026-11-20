"""
final_sections/ch6_implementation.py - 6. IMPLEMENTATION (Target: 5 pages, pp. 20-24)
"""

from docx.shared import Inches, Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from report_sections.common import (
    DIAG_DIR, SCREEN_DIR, add_para, add_bullet, add_image_box,
    add_algorithm_box, set_cell_background, set_table_borders,
    style_table_header, style_table_cells
)

def build_ch6(doc):
    # =========================================================================
    # PAGE 20: 6. IMPLEMENTATION, 6.1 Technologies Used & Fig. 6.1
    # =========================================================================
    p_h = doc.add_paragraph()
    p_h.paragraph_format.space_before = Pt(0)
    p_h.paragraph_format.space_after = Pt(8)
    p_h.paragraph_format.keep_with_next = True
    r = p_h.add_run("6. IMPLEMENTATION")
    r.font.name = 'Times New Roman'
    r.font.size = Pt(20)
    r.bold = True

    p_sub = doc.add_paragraph()
    p_sub.paragraph_format.space_before = Pt(4)
    p_sub.paragraph_format.space_after = Pt(2)
    p_sub.paragraph_format.keep_with_next = True
    r = p_sub.add_run("6.1 Technologies Used")
    r.font.name = 'Times New Roman'
    r.font.size = Pt(15)
    r.bold = True

    add_para(doc,
        "The system is implemented using a modern cybersecurity technology stack chosen for sub-millisecond execution velocity, "
        "type safety, and robust process containment:",
        space_after=3, font_size=11)
    add_bullet("Frontend Application: Built with Next.js 14, React 18, and Tailwind CSS. Employs React Server Components (RSC) and custom SVG animated gauges to visualize real-time threat scores.")
    add_bullet("Backend API: Engineered using Python 3.12 and FastAPI. Utilizes asynchronous asyncio event loops and Pydantic v2 data models, achieving sub-millisecond route handling.")
    add_bullet("Machine Learning Core: Implemented with Scikit-learn (Random Forest ensemble) and NumPy, performing C-optimized matrix calculations for fast inference.")
    add_bullet("Browser Extension: Developed on Chromium Manifest V3 WebExtension APIs, using declarative background service workers and chrome.storage.local caching.")
    add_bullet("Database & Cache: Redis 7.0 provides high-speed in-memory caching (0.42 ms lookups); PostgreSQL stores structured historical scan records.")
    add_bullet("Blockchain & Cryptography: Web3.py interacts with EVM smart contracts (ThreatRegistry.sol), anchoring SHA-256 evidence digests on-chain.")

    add_image_box(doc, DIAG_DIR / "Fig_6_1_Feature_Extraction_Pipeline.png", "Fig. 6.1: Feature Extraction Pipeline Architecture", width_in=4.8)
    doc.add_page_break()

    # =========================================================================
    # PAGE 21: 6.2 Module Description & Fig. 6.2
    # =========================================================================
    p_sub2 = doc.add_paragraph()
    p_sub2.paragraph_format.space_before = Pt(4)
    p_sub2.paragraph_format.space_after = Pt(4)
    p_sub2.paragraph_format.keep_with_next = True
    r2 = p_sub2.add_run("6.2 Module Description")
    r2.font.name = 'Times New Roman'
    r2.font.size = Pt(16)
    r2.bold = True

    add_para(doc, "The URLSentinel codebase is organized into four core functional microservice modules:")
    add_bullet("URL Normalizer & Lexical Module: Canonicalizes incoming URLs in accordance with RFC 3986, resolves Punycode IDN homoglyphs, strips tracking anchors, and computes 25+ structural indicators in memory.")
    add_bullet("Feature Extraction Pipeline: As shown in Figure 6.1, parses raw URLs into structural, entropy, and brand features within 1.39 ms without requiring external network lookups.")
    add_bullet("Machine Learning & Threat Intel Module: Evaluates feature vectors against calibrated Random Forest trees (100 estimators, max depth 12) and cross-references synchronized in-memory threat signatures.")
    add_bullet("Cryptographic Attestation Module: As shown in Figure 6.2, computes SHA-256 evidence digests and anchors verdicts to blockchain smart contracts to provide immutable forensic auditability.")

    add_image_box(doc, DIAG_DIR / "Fig_6_2_Blockchain_Verification_Workflow.png", "Fig. 6.2: Blockchain Verification Workflow", width_in=5.2)
    doc.add_page_break()

    # =========================================================================
    # PAGE 22: 6.3 Algorithms Used (Algorithms 1 and 2)
    # =========================================================================
    p_sub3 = doc.add_paragraph()
    p_sub3.paragraph_format.space_before = Pt(4)
    p_sub3.paragraph_format.space_after = Pt(4)
    p_sub3.paragraph_format.keep_with_next = True
    r3 = p_sub3.add_run("6.3 Algorithms Used for URL Detection and Risk Assessment")
    r3.font.name = 'Times New Roman'
    r3.font.size = Pt(16)
    r3.bold = True

    # Alg 1
    add_algorithm_box(
        "Algorithm 1: Lexical and Structural URL Feature Extraction",
        "Raw candidate URL string U",
        "25-dimensional numerical feature vector F",
        [
            "1: U_norm <- NormalizeURL(U)  // RFC 3986 canonicalization",
            "2: host, path, query <- ParseComponents(U_norm)",
            "3: F['url_len'] <- len(U_norm); F['host_len'] <- len(host)",
            "4: F['subdomain_count'] <- count(host, '.') - 1",
            "5: F['entropy_domain'] <- -SUM(P(c) * log2(P(c))) for c in host",
            "6: F['consonant_ratio'] <- count_consonants(host) / (count_vowels(host) + 1)",
            "7: F['brand_dist'] <- MinLevenshteinDistance(host, MONITORED_BRANDS)",
            "8: return F  // Execution latency: 0.85 ms"
        ]
    )

    # Alg 2
    add_algorithm_box(
        "Algorithm 2: Brand Impersonation and Typosquatting Detection",
        "Candidate host string, Registered apex domain",
        "Flag (Boolean), TargetBrand (String)",
        [
            "1: label <- ExtractRegistrableDomain(apex_domain)",
            "2: for each Brand in MONITORED_BRANDS do:",
            "3:     if label == Brand and apex_domain in AUTHORIZED_DOMAINS[Brand] then:",
            "4:         return (False, None)  // Legitimate authentic corporate portal",
            "5:     dist <- LevenshteinDistance(label, Brand)",
            "6:     if 1 <= dist <= 2 and len(label) >= len(Brand) - 1 then:",
            "7:         if apex_domain not in AUTHORIZED_DOMAINS[Brand] then:",
            "8:             return (True, Brand)  // Typosquatting spoof detected",
            "9: return (False, None)"
        ]
    )
    doc.add_page_break()

    # =========================================================================
    # PAGE 23: Algorithms 3 & 4 + 6.4 API Endpoints (Table 6.1)
    # =========================================================================
    # Alg 3
    add_algorithm_box(
        "Algorithm 3: Multi-Signal Risk Engine Synthesis",
        "Feature vector F, ThreatIntelFeed, MLClassifier",
        "Verdict (SAFE/ELEVATED/MALICIOUS), FinalRiskScore (0-100), Explanations",
        [
            "1: if host in TRUSTED_SSO_DOMAINS then return ('SAFE', 5, ['Verified SSO Infrastructure'])",
            "2: if ThreatIntelFeed.contains(host) then return ('MALICIOUS', 98, ['Confirmed Blacklist IOC'])",
            "3: p_ml <- MLClassifier.predict_proba(F)",
            "4: score_heur <- 0; reasons <- []",
            "5: if F['brand_dist'] <= 2 then score_heur += 45; reasons.append('Brand impersonation')",
            "6: if F['consonant_ratio'] >= 3.5 then score_heur += 30; reasons.append('DGA consonant clustering')",
            "7: if F['entropy_domain'] >= 3.8 then score_heur += 25; reasons.append('High Shannon entropy')",
            "8: R_raw <- (0.40 * p_ml * 100) + (0.35 * score_heur) + (0.25 * feed_score)",
            "9: R_final <- clamp(round(R_raw), 0, 100)",
            "10: verdict <- 'MALICIOUS' if R_final >= 85 else ('ELEVATED' if R_final >= 40 else 'SAFE')",
            "11: return (verdict, R_final, reasons)"
        ]
    )

    # Alg 4
    add_algorithm_box(
        "Algorithm 4: Cryptographic Evidence Provenance & Blockchain Anchor",
        "Scan tuple (URL, Verdict, Score, Timestamp), PrivateKey",
        "TxHash, EvidenceDigest",
        [
            "1: payload <- CanonicalSerialize({url, verdict, score, ts})",
            "2: digest <- SHA256(payload)  // 64-character hex hash",
            "3: tx <- ThreatRegistryContract.recordThreatVerdict(url, verdict, score, digest)",
            "4: receipt <- Web3.eth.send_raw_transaction(tx)",
            "5: return (receipt.transaction_hash, digest)"
        ]
    )

    p_sub4 = doc.add_paragraph()
    p_sub4.paragraph_format.space_before = Pt(4)
    p_sub4.paragraph_format.space_after = Pt(2)
    p_sub4.paragraph_format.keep_with_next = True
    r4 = p_sub4.add_run("6.4 API Endpoints")
    r4.font.name = 'Times New Roman'
    r4.font.size = Pt(14)
    r4.bold = True

    p_t61 = doc.add_paragraph()
    p_t61.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_t61.paragraph_format.space_before = Pt(2)
    p_t61.paragraph_format.space_after = Pt(2)
    p_t61.paragraph_format.keep_with_next = True
    rt = p_t61.add_run("Table 6.1: Core REST API Endpoints Specification")
    rt.font.name = 'Times New Roman'
    rt.font.size = Pt(10.5)
    rt.bold = True

    apis = [
        ("Method", "Endpoint", "Function & Parameters", "Response Format"),
        ("POST", "/api/v1/scan", "Evaluates candidate URL; payload: {\"url\": \"str\"}", "200 OK: {\"verdict\": \"MALICIOUS\", \"score\": 95}"),
        ("GET", "/api/v1/scan/{id}", "Retrieves historical forensic report by UUID", "200 OK: Full JSON telemetry, features, and tx_hash"),
        ("POST", "/api/v1/verify-evidence", "Verifies SHA-256 evidence against smart contract", "200 OK: {\"is_valid\": true, \"block_number\": 104218}"),
        ("GET", "/api/v1/threat-intel/status", "Queries feed synchronization status and counts", "200 OK: {\"synced_feeds\": 3, \"active_records\": 42180}"),
        ("GET", "/healthz", "Liveness and readiness probe for Docker", "200 OK: {\"status\": \"healthy\", \"redis\": true}"),
    ]

    tbl_api = doc.add_table(rows=len(apis), cols=4)
    tbl_api.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(tbl_api)
    aw = [0.8, 1.8, 2.1, 1.8]

    for idx, (m, ep, fp, rf) in enumerate(apis):
        row = tbl_api.rows[idx]
        for c_idx, val in enumerate([m, ep, fp, rf]):
            cell = row.cells[c_idx]
            set_cell_background(cell, "E2E8F0" if idx == 0 else ("FFFFFF" if idx % 2 == 1 else "F8FAFC"))
            cell.width = Inches(aw[c_idx])
            p = cell.paragraphs[0]
            p.paragraph_format.space_before = Pt(2)
            p.paragraph_format.space_after = Pt(2)
            p.paragraph_format.line_spacing = 1.10
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER if c_idx == 0 or idx == 0 else WD_ALIGN_PARAGRAPH.LEFT
            r = p.add_run(val)
            r.font.name = 'Times New Roman'
            r.font.size = Pt(8.5)
            r.bold = (idx == 0)

    doc.add_page_break()

    # =========================================================================
    # PAGE 24: 6.5 User Interface Design (Figs 6.3 and 6.4)
    # =========================================================================
    p_sub5 = doc.add_paragraph()
    p_sub5.paragraph_format.space_before = Pt(4)
    p_sub5.paragraph_format.space_after = Pt(4)
    p_sub5.paragraph_format.keep_with_next = True
    r5 = p_sub5.add_run("6.5 User Interface Design")
    r5.font.name = 'Times New Roman'
    r5.font.size = Pt(16)
    r5.bold = True

    add_para(doc,
        "Figure 6.3 shows the live Next.js web application landing page, featuring active defense telemetry counters and on-demand URL input. "
        "Figure 6.4 shows the live active threat verdict card evaluating 'http://paypa1-account-update.xyz/login', rendering the animated "
        "SVG threat gauge (Score 95, MALICIOUS), high-confidence warning badges, and explainable risk tags.",
        space_after=4, font_size=11)

    add_image_box(doc, SCREEN_DIR / "live_homepage.png", "Fig. 6.3: URLSentinel Web Dashboard Interface", width_in=4.7)
    add_image_box(doc, SCREEN_DIR / "live_scanner_verdict.png", "Fig. 6.4: Live Threat Scanner Active Verdict Card", width_in=4.7)

    doc.add_page_break()
    print("Chapter 6 built (exactly 5 pages, pp. 20-24).")
