"""
final_sections/ch5_sys_design.py - 5. SYSTEM DESIGN (Target: 6 pages, pp. 14-19)
"""

from docx.shared import Inches, Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
from report_sections.common import (
    DIAG_DIR, add_para, add_image_box
)

def build_ch5(doc):
    # =========================================================================
    # PAGE 14: 5. SYSTEM DESIGN & 5.1 System Architecture
    # =========================================================================
    p_h = doc.add_paragraph()
    p_h.paragraph_format.space_before = Pt(0)
    p_h.paragraph_format.space_after = Pt(10)
    p_h.paragraph_format.keep_with_next = True
    r = p_h.add_run("5. SYSTEM DESIGN")
    r.font.name = 'Times New Roman'
    r.font.size = Pt(20)
    r.bold = True

    p_sub1 = doc.add_paragraph()
    p_sub1.paragraph_format.space_before = Pt(6)
    p_sub1.paragraph_format.space_after = Pt(4)
    p_sub1.paragraph_format.keep_with_next = True
    r1 = p_sub1.add_run("5.1 System Architecture")
    r1.font.name = 'Times New Roman'
    r1.font.size = Pt(16)
    r1.bold = True

    add_para(doc,
        "The architecture of URLSentinel is designed around principles of loose coupling, high concurrency, strict trust boundary "
        "enforcement, and verifiable data integrity. As illustrated in Figure 5.1, the platform is partitioned into three primary tiers: "
        "the Client and Ingestion Tier, the Analytical API and Detection Engine Tier, and the Storage and Blockchain Verification Tier.")

    add_para(doc,
        "The Client Tier comprises the Next.js web application and the Chromium Manifest V3 browser extension. Incoming requests traverse "
        "an Nginx reverse proxy enforcing SSL termination, rate limiting, and SSRF containment. The Core Analytical Tier houses the "
        "URL Normalizer, Lexical Analyzer, Random Forest ML Classifier, and Threat Intelligence Ingestion crons. These microservices execute "
        "in parallel: while lexical features are extracted, threat feeds are queried concurrently. The Risk Engine synthesizes all signals into "
        "a calibrated verdict. Finally, the Storage Tier maintains in-memory Redis caches and anchors cryptographic SHA-256 evidence digests "
        "into an EVM smart contract ledger for permanent auditability.")

    add_image_box(doc, DIAG_DIR / "Fig_5_1_System_Architecture.png", "Fig. 5.1: System Architecture Diagram", width_in=5.4)
    doc.add_page_break()

    # =========================================================================
    # PAGE 15: 5.2 Use Case Diagram & 5.3 Entity Relationship Diagram
    # =========================================================================
    p_sub2 = doc.add_paragraph()
    p_sub2.paragraph_format.space_before = Pt(4)
    p_sub2.paragraph_format.space_after = Pt(2)
    p_sub2.paragraph_format.keep_with_next = True
    r2 = p_sub2.add_run("5.2 Use Case Diagram")
    r2.font.name = 'Times New Roman'
    r2.font.size = Pt(15)
    r2.bold = True

    add_para(doc,
        "Figure 5.2 defines the operational interactions between End Users, Security Analysts, and Administrators. "
        "End users submit URLs and receive instant warnings, analysts verify cryptographic receipts, and administrators manage threat feeds.",
        space_after=4, font_size=11)

    add_image_box(doc, DIAG_DIR / "Fig_5_2_Use_Case_Diagram.png", "Fig. 5.2: Use-Case Diagram", width_in=4.6)

    p_sub3 = doc.add_paragraph()
    p_sub3.paragraph_format.space_before = Pt(6)
    p_sub3.paragraph_format.space_after = Pt(2)
    p_sub3.paragraph_format.keep_with_next = True
    r3 = p_sub3.add_run("5.3 Entity Relationship Diagram (ERD)")
    r3.font.name = 'Times New Roman'
    r3.font.size = Pt(15)
    r3.bold = True

    add_para(doc,
        "Figure 5.3 defines the relational schema separating operational telemetry from blockchain evidence across SCAN_REQUEST, "
        "VERDICT_RECORD, FEATURE_RECORD, THREAT_INTEL_FEED, and BLOCKCHAIN_EVIDENCE entities.",
        space_after=4, font_size=11)

    add_image_box(doc, DIAG_DIR / "Fig_5_3_Entity_Relationship_Diagram.png", "Fig. 5.3: Entity Relationship Diagram (ERD)", width_in=4.6)
    doc.add_page_break()

    # =========================================================================
    # PAGE 16: 5.4 Activity Diagram
    # =========================================================================
    p_sub4 = doc.add_paragraph()
    p_sub4.paragraph_format.space_before = Pt(4)
    p_sub4.paragraph_format.space_after = Pt(4)
    p_sub4.paragraph_format.keep_with_next = True
    r4 = p_sub4.add_run("5.4 Activity Diagram")
    r4.font.name = 'Times New Roman'
    r4.font.size = Pt(16)
    r4.bold = True

    add_para(doc,
        "Figure 5.4 models the procedural control flow of an end-to-end URL evaluation. The activity begins upon target URL submission. "
        "The system normalizes the string and checks the SSO whitelist and Redis cache. If uncached, the workflow branches into parallel "
        "feature extraction, ML classification, and threat intelligence querying. The Risk Engine synthesizes the signals. If the score exceeds 60, "
        "an interstitial warning is triggered; otherwise, the request is permitted. Finally, evidence digests are anchored to the blockchain.")

    add_image_box(doc, DIAG_DIR / "Fig_5_4_Activity_Diagram.png", "Fig. 5.4: Activity Diagram", width_in=5.4)
    doc.add_page_break()

    # =========================================================================
    # PAGE 17: 5.5 Class Diagram
    # =========================================================================
    p_sub5 = doc.add_paragraph()
    p_sub5.paragraph_format.space_before = Pt(4)
    p_sub5.paragraph_format.space_after = Pt(4)
    p_sub5.paragraph_format.keep_with_next = True
    r5 = p_sub5.add_run("5.5 Class Diagram")
    r5.font.name = 'Times New Roman'
    r5.font.size = Pt(16)
    r5.bold = True

    add_para(doc,
        "Figure 5.5 illustrates the object-oriented structure of the URLSentinel core analytics engine. The design follows SOLID principles: "
        "URLNormalizer handles canonicalization; FeatureExtractor encapsulates Shannon entropy and Levenshtein distance methods; MLClassifier "
        "wraps pre-trained ensemble models; RiskEngine synthesizes multi-source telemetry into validated ScanReports; and BlockchainVerifier "
        "interacts with the EVM smart contract via Web3.py.")

    add_image_box(doc, DIAG_DIR / "Fig_5_5_Class_Diagram.png", "Fig. 5.5: Class Diagram", width_in=5.4)
    doc.add_page_break()

    # =========================================================================
    # PAGE 18: 5.6 Sequence Diagram
    # =========================================================================
    p_sub6 = doc.add_paragraph()
    p_sub6.paragraph_format.space_before = Pt(4)
    p_sub6.paragraph_format.space_after = Pt(4)
    p_sub6.paragraph_format.keep_with_next = True
    r6 = p_sub6.add_run("5.6 Sequence Diagram")
    r6.font.name = 'Times New Roman'
    r6.font.size = Pt(16)
    r6.bold = True

    add_para(doc,
        "Figure 5.6 illustrates the chronological message exchange between system components. Asynchronous non-blocking calls allow "
        "feature extraction, ML prediction, and threat feed queries to execute in parallel, delivering sub-2ms core analytical execution. "
        "The sequence coordinates the browser client, API gateway, ML model inference pipeline, threat feed cache, and blockchain registrar.")

    add_image_box(doc, DIAG_DIR / "Fig_5_6_Sequence_Diagram.png", "Fig. 5.6: Sequence Diagram", width_in=5.4)
    doc.add_page_break()

    # =========================================================================
    # PAGE 19: 5.7 Data Flow Diagrams (Level 0 and Level 1)
    # =========================================================================
    p_sub7 = doc.add_paragraph()
    p_sub7.paragraph_format.space_before = Pt(4)
    p_sub7.paragraph_format.space_after = Pt(2)
    p_sub7.paragraph_format.keep_with_next = True
    r7 = p_sub7.add_run("5.7 Data Flow Diagram (DFD)")
    r7.font.name = 'Times New Roman'
    r7.font.size = Pt(16)
    r7.bold = True

    add_para(doc,
        "Figure 5.7 presents the Level 0 Context DFD showing external entities interacting with Process 0.0. "
        "Figure 5.8 presents the Level 1 DFD, decomposing the platform into five sub-processes interacting with data stores D1–D3.",
        space_after=4, font_size=11)

    add_image_box(doc, DIAG_DIR / "Fig_5_7_DFD_Level_0.png", "Fig. 5.7: Data Flow Diagram (Level 0)", width_in=4.6)
    add_image_box(doc, DIAG_DIR / "Fig_5_8_DFD_Level_1.png", "Fig. 5.8: Data Flow Diagram (Level 1)", width_in=4.6)

    doc.add_page_break()
    print("Chapter 5 built (exactly 6 pages, pp. 14-19).")
