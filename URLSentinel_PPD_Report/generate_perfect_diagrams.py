"""
generate_perfect_diagrams.py - High-precision diagram generator for URLSentinel PPD Report
Generates publication-quality architectural, UML, DFD, and evaluation charts.
Zero overlapping lines, clean typography, consistent academic color palette.
"""

import os
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

DIAG_DIR = Path(r"z:\URLSentinel\URLSentinel_PPD_Report\diagrams")
CHART_DIR = Path(r"z:\URLSentinel\URLSentinel_PPD_Report\charts")
DIAG_DIR.mkdir(parents=True, exist_ok=True)
CHART_DIR.mkdir(parents=True, exist_ok=True)

# Common canvas helper
def create_canvas(width=9.5, height=5.8, dpi=300):
    fig, ax = plt.subplots(figsize=(width, height), dpi=dpi)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')
    return fig, ax

def draw_box(ax, x, y, w, h, title, subtitle="", color="#0f172a", bgcolor="#ffffff", edge_color="#334155", radius=1.5, lw=1.2):
    rect = patches.FancyBboxPatch(
        (x, y), w, h,
        boxstyle=f"round,pad=0.3,rounding_size={radius}",
        ec=edge_color, fc=bgcolor, lw=lw, zorder=2
    )
    ax.add_patch(rect)
    if subtitle:
        ax.text(x + w/2, y + h*0.62, title, ha='center', va='center', fontsize=8.5, fontweight='bold', color=color, zorder=3)
        ax.text(x + w/2, y + h*0.28, subtitle, ha='center', va='center', fontsize=7.2, color="#475569", zorder=3)
    else:
        ax.text(x + w/2, y + h/2, title, ha='center', va='center', fontsize=8.5, fontweight='bold', color=color, zorder=3)
    return rect

def draw_arrow(ax, x1, y1, x2, y2, label="", color="#334155", lw=1.2):
    ax.annotate(
        "", xy=(x2, y2), xytext=(x1, y1),
        arrowprops=dict(arrowstyle="-|>", color=color, lw=lw, mutation_scale=10),
        zorder=4
    )
    if label:
        mx, my = (x1 + x2)/2, (y1 + y2)/2
        ax.text(mx, my + 1.2, label, ha='center', va='bottom', fontsize=7, color="#1e293b",
                bbox=dict(boxstyle="round,pad=0.15", fc="white", ec="none", alpha=0.85), zorder=5)

# ===========================================================================
# 1. Fig 5.1: Overall System Architecture Diagram
# ===========================================================================
def build_fig_5_1():
    from generate_compact_fig_5_1 import generate_compact_architecture_diagram
    generate_compact_architecture_diagram()
    print("Regenerated Fig 5.1 (Compact Publication-Grade)")

# ===========================================================================
# 2. Fig 5.2: Use Case Diagram (Clean UML, No Line Crossings over text)
# ===========================================================================
def build_fig_5_2():
    fig, ax = create_canvas(9.5, 5.8)
    ax.text(50, 96, "USE CASE DIAGRAM: URLSENTINEL PLATFORM", ha='center', fontsize=11, fontweight='bold', color="#0f172a")

    # Boundary Box
    b_rect = patches.Rectangle((28, 6), 68, 86, fill=False, ec="#475569", lw=1.5, linestyle="--")
    ax.add_patch(b_rect)
    ax.text(62, 88.5, "URLSentinel Defense System Boundary", ha='center', fontsize=9.5, fontweight='bold', color="#334155")

    # Actors on the Left
    draw_box(ax, 2, 72, 22, 11, "End User", "Consumer / Employee", "#1e3a8a", "#eff6ff", "#3b82f6", radius=2)
    draw_box(ax, 2, 43, 22, 11, "Security Analyst", "SOC Incident Responder", "#065f46", "#ecfdf5", "#10b981", radius=2)
    draw_box(ax, 2, 14, 22, 11, "Administrator", "Platform Engineer", "#701a75", "#fdf4ff", "#c026d3", radius=2)

    # Use Cases inside Boundary (Ovals)
    def draw_oval(cx, cy, rx, ry, label):
        oval = patches.Ellipse((cx, cy), rx*2, ry*2, ec="#334155", fc="#f8fafc", lw=1.2, zorder=2)
        ax.add_patch(oval)
        ax.text(cx, cy, label, ha='center', va='center', fontsize=7.8, fontweight='bold', color="#0f172a", zorder=3)

    # User UCs
    draw_oval(46, 79, 13, 4.2, "Submit Target URL")
    draw_oval(46, 68, 13, 4.2, "View Live Verdict & Gauge")
    draw_oval(78, 74, 14, 4.2, "Browse with MV3 Protection")

    # Analyst UCs
    draw_oval(46, 54, 13, 4.2, "Inspect Entropy & DGA Data")
    draw_oval(46, 43, 13, 4.2, "Export Threat Report (JSON)")
    draw_oval(78, 48, 14, 4.2, "Verify Blockchain Evidence Hash")

    # Admin UCs
    draw_oval(46, 28, 13, 4.2, "Sync External Threat Feeds")
    draw_oval(46, 17, 13, 4.2, "Review Sandbox Health & Logs")
    draw_oval(78, 22, 14, 4.2, "Manage Rate Limits & API Keys")

    # Clean Actor Connector Lines (No intersecting actor boxes)
    # End User -> UCs
    ax.plot([24, 33], [77.5, 79], color="#1e3a8a", lw=1.2)
    ax.plot([24, 33], [77.5, 68], color="#1e3a8a", lw=1.2)
    ax.plot([24, 64], [77.5, 74], color="#1e3a8a", lw=1.2)

    # Analyst -> UCs
    ax.plot([24, 33], [48.5, 54], color="#065f46", lw=1.2)
    ax.plot([24, 33], [48.5, 43], color="#065f46", lw=1.2)
    ax.plot([24, 64], [48.5, 48], color="#065f46", lw=1.2)

    # Admin -> UCs
    ax.plot([24, 33], [19.5, 28], color="#701a75", lw=1.2)
    ax.plot([24, 33], [19.5, 17], color="#701a75", lw=1.2)
    ax.plot([24, 64], [19.5, 22], color="#701a75", lw=1.2)

    plt.tight_layout()
    p = DIAG_DIR / "Fig_5_2_Use_Case_Diagram.png"
    plt.savefig(p, dpi=300)
    plt.close()
    print("Regenerated Fig 5.2")

# ===========================================================================
# 3. Fig 5.3: Entity Relationship Diagram (ERD) - Clean relational layout
# ===========================================================================
def build_fig_5_3():
    fig, ax = create_canvas(9.5, 5.8)
    ax.text(50, 96, "ENTITY RELATIONSHIP DIAGRAM (DATABASE SCHEMA & BLOCKCHAIN)", ha='center', fontsize=11, fontweight='bold', color="#0f172a")

    # Table Box Helper
    def draw_erd_table(x, y, w, h, name, fields):
        # Header
        h_h = 4.5
        rect_h = patches.Rectangle((x, y + h - h_h), w, h_h, ec="#334155", fc="#1e293b", lw=1.2, zorder=2)
        ax.add_patch(rect_h)
        ax.text(x + w/2, y + h - h_h/2, name, ha='center', va='center', fontsize=8, fontweight='bold', color="white", zorder=3)
        # Body
        rect_b = patches.Rectangle((x, y), w, h - h_h, ec="#334155", fc="#f8fafc", lw=1.2, zorder=2)
        ax.add_patch(rect_b)
        # Fields
        for idx, (f_name, f_type, is_pk) in enumerate(fields):
            fy = y + h - h_h - (idx + 0.7) * 3.2
            prefix = "PK " if is_pk == "PK" else ("FK " if is_pk == "FK" else "   ")
            color = "#b91c1c" if is_pk == "PK" else ("#1d4ed8" if is_pk == "FK" else "#334155")
            ax.text(x + 1.5, fy, prefix + f_name, fontsize=7, fontweight='bold' if is_pk else 'normal', color=color, zorder=3)
            ax.text(x + w - 1.5, fy, f_type, ha='right', fontsize=6.8, color="#64748b", zorder=3)

    # 1. SCAN_REQUEST
    f_scan = [
        ("id", "UUID", "PK"),
        ("raw_url", "TEXT", ""),
        ("canonical_url", "TEXT", ""),
        ("url_hash", "VARCHAR(64)", ""),
        ("client_ip", "VARCHAR(45)", ""),
        ("created_at", "TIMESTAMP", ""),
    ]
    draw_erd_table(4, 52, 28, 25, "SCAN_REQUEST", f_scan)

    # 2. VERDICT_RECORD
    f_verdict = [
        ("id", "UUID", "PK"),
        ("scan_id", "UUID", "FK"),
        ("verdict", "VARCHAR(16)", ""),
        ("risk_score", "INTEGER", ""),
        ("confidence", "FLOAT", ""),
        ("evidence_hash", "VARCHAR(64)", ""),
    ]
    draw_erd_table(36, 52, 28, 25, "VERDICT_RECORD", f_verdict)

    # 3. FEATURE_RECORD
    f_feat = [
        ("id", "UUID", "PK"),
        ("scan_id", "UUID", "FK"),
        ("entropy", "FLOAT", ""),
        ("consonant_ratio", "FLOAT", ""),
        ("brand_distance", "INTEGER", ""),
        ("ml_probability", "FLOAT", ""),
    ]
    draw_erd_table(68, 52, 28, 25, "FEATURE_RECORD", f_feat)

    # 4. BLOCKCHAIN_EVIDENCE
    f_chain = [
        ("tx_hash", "VARCHAR(66)", "PK"),
        ("scan_id", "UUID", "FK"),
        ("block_number", "BIGINT", ""),
        ("evidence_digest", "VARCHAR(64)", ""),
        ("signer_address", "VARCHAR(42)", ""),
        ("anchored_at", "TIMESTAMP", ""),
    ]
    draw_erd_table(20, 10, 28, 25, "BLOCKCHAIN_EVIDENCE", f_chain)

    # 5. THREAT_INTEL_FEED
    f_intel = [
        ("id", "UUID", "PK"),
        ("domain", "VARCHAR(255)", ""),
        ("source_feed", "VARCHAR(32)", ""),
        ("is_malicious", "BOOLEAN", ""),
        ("confidence", "FLOAT", ""),
        ("last_updated", "TIMESTAMP", ""),
    ]
    draw_erd_table(54, 10, 28, 25, "THREAT_INTEL_FEED", f_intel)

    # Relationships (Connectors)
    # SCAN_REQUEST (1) -> (1) VERDICT_RECORD
    draw_arrow(ax, 32, 64.5, 36, 64.5, "1 : 1")
    # VERDICT_RECORD (1) -> (1) FEATURE_RECORD
    draw_arrow(ax, 64, 64.5, 68, 64.5, "1 : 1")
    # VERDICT_RECORD (1) -> (1) BLOCKCHAIN_EVIDENCE
    draw_arrow(ax, 40, 52, 34, 35, "1 : 1")
    # SCAN_REQUEST -> THREAT_INTEL_FEED lookup
    draw_arrow(ax, 50, 52, 58, 35, "1 : N")

    plt.tight_layout()
    p = DIAG_DIR / "Fig_5_3_Entity_Relationship_Diagram.png"
    plt.savefig(p, dpi=300)
    plt.close()
    print("Regenerated Fig 5.3")

# ===========================================================================
# 4. Fig 5.4: Activity Diagram (UML compliant, start/decision/end)
# ===========================================================================
def build_fig_5_4():
    fig, ax = create_canvas(9.5, 5.8)
    ax.text(50, 96, "ACTIVITY DIAGRAM: END-TO-END URL EVALUATION WORKFLOW", ha='center', fontsize=11, fontweight='bold', color="#0f172a")

    # Start Node
    start = patches.Circle((50, 89), 2.2, ec="#0f172a", fc="#0f172a", zorder=3)
    ax.add_patch(start)
    ax.text(50, 92.5, "Start", ha='center', fontsize=7.5, color="#0f172a")

    # Step 1: Input & Normalization
    draw_box(ax, 34, 76, 32, 7, "Receive Candidate URL & Canonicalize", "RFC 3986 Normalization, Punycode Decode")
    draw_arrow(ax, 50, 86.8, 50, 83)

    # Decision 1: Whitelist Check
    def draw_diamond(cx, cy, rx, ry, text):
        poly = patches.Polygon([[cx, cy+ry], [cx+rx, cy], [cx, cy-ry], [cx-rx, cy]], ec="#334155", fc="#fef3c7", lw=1.2, zorder=2)
        ax.add_patch(poly)
        ax.text(cx, cy, text, ha='center', va='center', fontsize=7, fontweight='bold', color="#78350f", zorder=3)

    draw_diamond(50, 65, 12, 5, "In Trusted SSO\nWhitelist?")
    draw_arrow(ax, 50, 76, 50, 70)

    # Branch Yes: Whitelist SAFE
    draw_box(ax, 72, 61.5, 24, 7, "Issue SAFE Verdict", "Hard-clamped Score: 5")
    draw_arrow(ax, 62, 65, 72, 65, "[Yes]")

    # Branch No: Continue to Multi-Signal Mining
    draw_arrow(ax, 50, 60, 50, 52, "[No]")
    draw_box(ax, 28, 45, 44, 7, "Concurrent Feature Mining & Threat Feed Query", "Shannon Entropy | DGA Ratio | Levenshtein Brand | URLhaus")

    # Step 3: Bayesian Synthesis
    draw_box(ax, 30, 31, 40, 7, "Synthesize Multi-Signal Bayesian Risk Score", "Calculate Final Score (0 - 100) & Explanations")
    draw_arrow(ax, 50, 45, 50, 38)

    # Decision 2: Dangerous Target?
    draw_diamond(50, 19, 12, 5, "Risk Score\n>= 60?")
    draw_arrow(ax, 50, 31, 50, 24)

    # Branches from Decision 2
    draw_box(ax, 10, 6, 26, 7, "Block & Display Warning Screen", "Interstitial Red Warning")
    draw_box(ax, 64, 6, 26, 7, "Allow Navigation & Cache Result", "Return Clean Response")
    draw_arrow(ax, 38, 19, 23, 13, "[Yes]")
    draw_arrow(ax, 62, 19, 77, 13, "[No]")

    plt.tight_layout()
    p = DIAG_DIR / "Fig_5_4_Activity_Diagram.png"
    plt.savefig(p, dpi=300)
    plt.close()
    print("Regenerated Fig 5.4")

# ===========================================================================
# 5. Fig 5.5: Class Diagram (Clean 3-compartment UML)
# ===========================================================================
def build_fig_5_5():
    fig, ax = create_canvas(9.5, 5.8)
    ax.text(50, 96, "CORE OBJECT-ORIENTED CLASS DIAGRAM", ha='center', fontsize=11, fontweight='bold', color="#0f172a")

    def draw_class_box(x, y, w, h, name, attrs, methods):
        # Header
        h_top = 4.2
        rect_h = patches.Rectangle((x, y + h - h_top), w, h_top, ec="#334155", fc="#1e293b", lw=1.2, zorder=2)
        ax.add_patch(rect_h)
        ax.text(x + w/2, y + h - h_top/2, name, ha='center', va='center', fontsize=7.8, fontweight='bold', color="white", zorder=3)
        # Body
        rect_b = patches.Rectangle((x, y), w, h - h_top, ec="#334155", fc="#f8fafc", lw=1.2, zorder=2)
        ax.add_patch(rect_b)
        # Separator line
        sep_y = y + h - h_top - (len(attrs) * 2.8 + 1.5)
        ax.plot([x, x + w], [sep_y, sep_y], color="#94a3b8", lw=0.8, zorder=3)
        # Attributes
        for i, a in enumerate(attrs):
            ax.text(x + 1.2, y + h - h_top - (i + 0.8) * 2.8, a, fontsize=6.8, color="#334155", zorder=3)
        # Methods
        for j, m in enumerate(methods):
            ax.text(x + 1.2, sep_y - (j + 0.8) * 2.8, m, fontsize=6.8, color="#0f172a", zorder=3)

    # Class 1: URLNormalizer
    c1_attrs = ["- raw_url: str", "- punycode: str"]
    c1_meth = ["+ normalize(): str", "+ decode_punycode(): str"]
    draw_class_box(4, 55, 27, 23, "URLNormalizer", c1_attrs, c1_meth)

    # Class 2: FeatureExtractor
    c2_attrs = ["- psl_trie: Trie", "- brands: List[str]"]
    c2_meth = ["+ extract(url): FeatureVector", "+ calc_entropy(s): float", "+ levenshtein(a, b): int"]
    draw_class_box(36, 52, 28, 26, "FeatureExtractor", c2_attrs, c2_meth)

    # Class 3: MLClassifier
    c3_attrs = ["- model: RandomForest", "- calibrated_scaler: any"]
    c3_meth = ["+ predict_proba(fv): float", "+ evaluate_dga(host): float"]
    draw_class_box(69, 52, 27, 26, "MLClassifier", c3_attrs, c3_meth)

    # Class 4: RiskEngine
    c4_attrs = ["- weights: Dict[str, float]", "- thresholds: Dict[str, int]"]
    c4_meth = ["+ synthesize(fv, ml_p): ScanReport", "+ compile_factors(): List[str]"]
    draw_class_box(20, 10, 30, 26, "RiskEngine", c4_attrs, c4_meth)

    # Class 5: BlockchainVerifier
    c5_attrs = ["- web3: Web3", "- contract_addr: str"]
    c5_meth = ["+ generate_digest(): str", "+ anchor_on_chain(): str", "+ verify_receipt(): bool"]
    draw_class_box(56, 10, 30, 26, "BlockchainVerifier", c5_attrs, c5_meth)

    # Dependencies / Associations
    draw_arrow(ax, 31, 65, 36, 65, "uses")
    draw_arrow(ax, 64, 65, 69, 65, "supplies")
    draw_arrow(ax, 50, 52, 35, 36, "inputs")
    draw_arrow(ax, 75, 52, 45, 36, "predicts")
    draw_arrow(ax, 50, 23, 56, 23, "attests")

    plt.tight_layout()
    p = DIAG_DIR / "Fig_5_5_Class_Diagram.png"
    plt.savefig(p, dpi=300)
    plt.close()
    print("Regenerated Fig 5.5")

# ===========================================================================
# 6. Fig 5.6: Sequence Diagram (Clean horizontal lifelines & messages)
# ===========================================================================
def build_fig_5_6():
    fig, ax = create_canvas(9.5, 5.8)
    ax.text(50, 96, "SYSTEM SEQUENCE DIAGRAM: CONCURRENT URL EVALUATION", ha='center', fontsize=11, fontweight='bold', color="#0f172a")

    lifelines = [
        ("Client / Browser", 10),
        ("FastAPI Gateway", 30),
        ("Feature Engine", 50),
        ("ML & Intel Tier", 70),
        ("Blockchain Ledger", 90),
    ]

    # Draw header boxes & lifelines
    for name, x in lifelines:
        draw_box(ax, x - 8, 84, 16, 7, name, "", "#1e293b", "#e2e8f0", "#475569", radius=1)
        ax.plot([x, x], [12, 84], color="#94a3b8", lw=1.2, linestyle="--", zorder=1)

    # Sequence Messages
    def draw_msg(y, x1, x2, text, is_reply=False):
        style = "-|>" if not is_reply else "->"
        ls = "-" if not is_reply else "--"
        color = "#1e3a8a" if not is_reply else "#059669"
        ax.annotate(
            "", xy=(x2, y), xytext=(x1, y),
            arrowprops=dict(arrowstyle=style, color=color, lw=1.2, linestyle=ls),
            zorder=4
        )
        mx = (x1 + x2)/2
        ax.text(mx, y + 1.2, text, ha='center', va='bottom', fontsize=6.8, color="#0f172a",
                bbox=dict(boxstyle="round,pad=0.1", fc="white", ec="none", alpha=0.9), zorder=5)

    draw_msg(78, 10, 30, "1. POST /api/v1/scan (target URL)")
    draw_msg(71, 30, 50, "2. extract_features(canonical_url)")
    draw_msg(64, 50, 30, "3. FeatureVector (25 dimensions)", is_reply=True)
    draw_msg(57, 30, 70, "4. Async evaluate(FV, feeds)")
    draw_msg(50, 70, 30, "5. ML Prob (0.95) & Intel Hit", is_reply=True)
    draw_msg(43, 30, 90, "6. Anchor SHA-256 Digest on-chain")
    draw_msg(36, 90, 30, "7. TxReceipt (0x8f2a...)", is_reply=True)
    draw_msg(28, 30, 10, "8. HTTP 200 JSON Verdict (MALICIOUS)", is_reply=True)

    plt.tight_layout()
    p = DIAG_DIR / "Fig_5_6_Sequence_Diagram.png"
    plt.savefig(p, dpi=300)
    plt.close()
    print("Regenerated Fig 5.6")

# ===========================================================================
# 7. Fig 5.7: DFD Level 0 (Context Level Diagram)
# ===========================================================================
def build_fig_5_7():
    fig, ax = create_canvas(9.5, 5.8)
    ax.text(50, 96, "DATA FLOW DIAGRAM LEVEL 0 (CONTEXT LEVEL)", ha='center', fontsize=11, fontweight='bold', color="#0f172a")

    # Central System Process (Circle)
    circ = patches.Circle((50, 50), 16, ec="#1e40af", fc="#eff6ff", lw=1.5, zorder=2)
    ax.add_patch(circ)
    ax.text(50, 52, "0.0\nURLSentinel Platform", ha='center', va='center', fontsize=9.5, fontweight='bold', color="#1e40af", zorder=3)
    ax.text(50, 42, "Central Defense System", ha='center', va='center', fontsize=7.2, color="#475569", zorder=3)

    # External Entities (Rectangles)
    draw_box(ax, 3, 68, 22, 12, "End User / Extension", "Endpoint Web Client", "#0f172a", "#f8fafc", "#475569")
    draw_box(ax, 75, 68, 22, 12, "Security Analyst", "SOC Forensics Console", "#0f172a", "#f8fafc", "#475569")
    draw_box(ax, 3, 18, 22, 12, "External Threat Feeds", "URLhaus / OpenPhish", "#0f172a", "#f8fafc", "#475569")
    draw_box(ax, 75, 18, 22, 12, "Blockchain Ledger", "EVM Threat Registry", "#0f172a", "#f8fafc", "#475569")

    # Data flows with clear routing (no arrows crossing text)
    draw_arrow(ax, 25, 76, 38, 62, "Candidate URL")
    draw_arrow(ax, 38, 56, 25, 70, "Threat Verdict / Warning")

    draw_arrow(ax, 75, 76, 62, 62, "Audit Query")
    draw_arrow(ax, 62, 56, 75, 70, "Forensic Telemetry")

    draw_arrow(ax, 25, 26, 38, 42, "Feed IOC Signatures")
    draw_arrow(ax, 62, 42, 75, 26, "Evidence Digest Hash")

    plt.tight_layout()
    p = DIAG_DIR / "Fig_5_7_DFD_Level_0.png"
    plt.savefig(p, dpi=300)
    plt.close()
    print("Regenerated Fig 5.7")

# ===========================================================================
# 8. Fig 5.8: DFD Level 1 (Functional Decomposition)
# ===========================================================================
def build_fig_5_8():
    fig, ax = create_canvas(9.5, 5.8)
    ax.text(50, 96, "DATA FLOW DIAGRAM LEVEL 1 (DECOMPOSITION)", ha='center', fontsize=11, fontweight='bold', color="#0f172a")

    # Processes
    def draw_proc(x, y, w, h, p_num, name):
        draw_box(ax, x, y, w, h, f"{p_num} {name}", "", "#1e3a8a", "#eff6ff", "#3b82f6", radius=2)

    # Data Store helper (open ended rectangle)
    def draw_store(x, y, w, h, ds_id, name):
        ax.plot([x, x+w], [y+h, y+h], color="#0f172a", lw=1.2)
        ax.plot([x, x+w], [y, y], color="#0f172a", lw=1.2)
        ax.plot([x, x], [y, y+h], color="#0f172a", lw=1.2)
        rect = patches.Rectangle((x, y), w, h, ec="none", fc="#f1f5f9", zorder=1)
        ax.add_patch(rect)
        ax.text(x + w/2, y + h/2, f"{ds_id} {name}", ha='center', va='center', fontsize=7.2, fontweight='bold', color="#0f172a", zorder=2)

    draw_proc(4, 68, 26, 10, "1.0", "URL Normalization")
    draw_proc(37, 68, 26, 10, "2.0", "Feature Extraction")
    draw_proc(70, 68, 26, 10, "3.0", "ML Classification")

    draw_store(4, 46, 26, 7, "D1", "Redis Verdict Cache")
    draw_store(70, 46, 26, 7, "D2", "Threat Feed Store")

    draw_proc(20, 24, 28, 10, "4.0", "Risk Synthesis Engine")
    draw_proc(60, 24, 28, 10, "5.0", "Blockchain Attestation")

    draw_store(40, 8, 28, 7, "D3", "On-Chain Threat Ledger")

    # Clean Flows
    draw_arrow(ax, 30, 73, 37, 73, "Canonical URL")
    draw_arrow(ax, 63, 73, 70, 73, "Feature Vector")
    draw_arrow(ax, 17, 68, 17, 53, "Check Cache")
    draw_arrow(ax, 83, 68, 83, 53, "Query Feeds")

    draw_arrow(ax, 50, 68, 34, 34, "Features")
    draw_arrow(ax, 83, 46, 48, 29, "Threat Match")
    draw_arrow(ax, 48, 29, 60, 29, "Evidence Digest")
    draw_arrow(ax, 74, 24, 54, 15, "Anchor Tx")

    plt.tight_layout()
    p = DIAG_DIR / "Fig_5_8_DFD_Level_1.png"
    plt.savefig(p, dpi=300)
    plt.close()
    print("Regenerated Fig 5.8")

# ===========================================================================
# 9. Fig 6.1: Feature Extraction Pipeline
# ===========================================================================
def build_fig_6_1():
    fig, ax = create_canvas(9.5, 5.2)
    ax.text(50, 96, "URLSENTINEL FEATURE EXTRACTION PIPELINE", ha='center', fontsize=11, fontweight='bold', color="#0f172a")

    stages = [
        ("Raw Input URL", "RFC 3986 Sanity Check", 4),
        ("Punycode & Normalization", "IDN Decode, Lowercase Host", 23),
        ("Structural Tokenization", "Subdomains, Path, Params", 42),
        ("Mathematical Analysis", "Shannon Entropy H(S) & DGA", 61),
        ("Feature Vector Assembly", "25D Numerical Array", 80),
    ]

    for title, sub, x in stages:
        draw_box(ax, x, 40, 16, 26, title, sub, "#1e3a8a", "#eff6ff", "#3b82f6")

    draw_arrow(ax, 20, 53, 23, 53)
    draw_arrow(ax, 39, 53, 42, 53)
    draw_arrow(ax, 58, 53, 61, 53)
    draw_arrow(ax, 77, 53, 80, 53)

    # Sub-features listed below
    ax.text(50, 24, "Extracted Indicators: URL Length, Subdomain Count, Entropy, Consonant Ratio, Brand Levenshtein Distance",
            ha='center', fontsize=8, color="#334155", bbox=dict(boxstyle="round,pad=0.3", fc="#f8fafc", ec="#cbd5e1"))

    plt.tight_layout()
    p = DIAG_DIR / "Fig_6_1_Feature_Extraction_Pipeline.png"
    plt.savefig(p, dpi=300)
    plt.close()
    print("Regenerated Fig 6.1")

# ===========================================================================
# 10. Fig 6.2: Blockchain Verification Workflow
# ===========================================================================
def build_fig_6_2():
    fig, ax = create_canvas(9.5, 5.2)
    ax.text(50, 96, "CRYPTOGRAPHIC EVIDENCE PROVENANCE & BLOCKCHAIN WORKFLOW", ha='center', fontsize=11, fontweight='bold', color="#0f172a")

    steps = [
        ("Evaluation Verdict", "Tuple: URL, Score, Verdict", 4),
        ("Canonical JSON Digest", "Deterministic Serialization", 23),
        ("SHA-256 Hashing", "64-char Hex Evidence Hash", 42),
        ("Smart Contract TX", "ThreatRegistry.sol Invocation", 61),
        ("On-Chain Verification", "Public Auditability", 80),
    ]

    for title, sub, x in steps:
        draw_box(ax, x, 40, 16, 26, title, sub, "#065f46", "#ecfdf5", "#10b981")

    draw_arrow(ax, 20, 53, 23, 53)
    draw_arrow(ax, 39, 53, 42, 53)
    draw_arrow(ax, 58, 53, 61, 53)
    draw_arrow(ax, 77, 53, 80, 53)

    ax.text(50, 24, "Immutable Provenance: Any third party can independently re-hash the scan payload and match the on-chain receipt",
            ha='center', fontsize=8, color="#334155", bbox=dict(boxstyle="round,pad=0.3", fc="#f8fafc", ec="#cbd5e1"))

    plt.tight_layout()
    p = DIAG_DIR / "Fig_6_2_Blockchain_Verification_Workflow.png"
    plt.savefig(p, dpi=300)
    plt.close()
    print("Regenerated Fig 6.2")

# ===========================================================================
# 11. Charts: Figs 7.1, 9.1, 9.2, 9.3 (Redesigned with no clipped text)
# ===========================================================================
def build_charts():
    # Fig 7.1: Latency Pipeline Breakdown
    plt.figure(figsize=(8, 4.2), dpi=300)
    stages = [
        "1. Normalization & Sanity Check",
        "2. Feature Extraction & Entropy",
        "3. ML Classifier Inference",
        "4. Threat Feed Hash Query",
        "5. Risk Synthesis & Response"
    ]
    latencies = [0.12, 0.85, 0.28, 0.09, 0.05]
    colors = ["#3b82f6", "#8b5cf6", "#10b981", "#f59e0b", "#ec4899"]

    bars = plt.barh(stages[::-1], latencies[::-1], color=colors[::-1], height=0.55)
    plt.xlabel("Execution Latency (milliseconds)", fontsize=9.5, fontweight='bold', color="#0f172a")
    plt.title("URLSentinel Evaluation Latency Pipeline Breakdown (Total: 1.39 ms)", fontsize=10.5, fontweight='bold', color="#0f172a", pad=12)
    plt.xlim(0, 1.1)
    plt.grid(axis='x', linestyle='--', alpha=0.5)

    for bar in bars:
        w = bar.get_width()
        plt.text(w + 0.02, bar.get_y() + bar.get_height()/2, f"{w:.2f} ms", va='center', fontsize=8.5, fontweight='bold', color="#1e293b")

    plt.tight_layout()
    plt.savefig(CHART_DIR / "Fig_7_1_Latency_Pipeline_Breakdown.png")
    plt.savefig(CHART_DIR / "latency_pipeline_breakdown.png")
    plt.close()
    print("Regenerated Fig 7.1 Latency Chart")

    # Fig 9.1: Overall Accuracy Comparison
    plt.figure(figsize=(8, 4.5), dpi=300)
    models = ["Static Blacklists\n(DNSBL/Feeds)", "Naive TF-IDF\nClassifier", "Random Forest\n(Baseline)", "URLSentinel v2.1\n(Multi-Layer)"]
    accuracies = [68.95, 78.40, 88.60, 97.15]
    bar_colors = ["#94a3b8", "#64748b", "#3b82f6", "#10b981"]

    b = plt.bar(models, accuracies, color=bar_colors, width=0.52)
    plt.ylabel("Overall Accuracy (%)", fontsize=9.5, fontweight='bold', color="#0f172a")
    plt.title("Detection Accuracy Comparison Across Paradigms (2,000 URLs)", fontsize=10.5, fontweight='bold', color="#0f172a", pad=12)
    plt.ylim(50, 105)
    plt.grid(axis='y', linestyle='--', alpha=0.5)

    for bar in b:
        h = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2, h + 1.2, f"{h:.2f}%", ha='center', fontsize=9, fontweight='bold', color="#0f172a")

    plt.tight_layout()
    plt.savefig(CHART_DIR / "Fig_9_1_Overall_Accuracy_Comparison.png")
    plt.savefig(CHART_DIR / "overall_accuracy_comparison.png")
    plt.close()
    print("Regenerated Fig 9.1 Accuracy Comparison")

    # Fig 9.2: Eight-Dimensional Capability Comparison (Clean, clearly labelled)
    categories = ["Typosquatting", "DGA Detection", "Subdomain Depth", "Latency (<2ms)", "Enterprise SSO", "Obfuscation", "Zero-Hour", "Explainability"]
    N = len(categories)
    angles = [n / float(N) * 2 * np.pi for n in range(N)]
    angles += angles[:1]

    # Scores out of 10
    v_black = [3, 2, 4, 9, 3, 2, 2, 2]
    v_ml = [6, 7, 7, 8, 4, 7, 7, 4]
    v_sentinel = [10, 9, 9, 10, 10, 9, 9, 10]

    v_black += v_black[:1]
    v_ml += v_ml[:1]
    v_sentinel += v_sentinel[:1]

    plt.figure(figsize=(7, 5), dpi=300)
    ax_rad = plt.subplot(111, polar=True)
    plt.xticks(angles[:-1], categories, color='#0f172a', size=8, fontweight='bold')
    ax_rad.set_rlabel_position(0)
    plt.yticks([2, 4, 6, 8, 10], ["2", "4", "6", "8", "10"], color="#64748b", size=7)
    plt.ylim(0, 11)

    ax_rad.plot(angles, v_black, linewidth=1.2, linestyle='solid', label="Static Blacklists", color="#94a3b8")
    ax_rad.fill(angles, v_black, '#94a3b8', alpha=0.1)

    ax_rad.plot(angles, v_ml, linewidth=1.2, linestyle='solid', label="Standard ML Classifier", color="#3b82f6")
    ax_rad.fill(angles, v_ml, '#3b82f6', alpha=0.15)

    ax_rad.plot(angles, v_sentinel, linewidth=2, linestyle='solid', label="URLSentinel v2.1", color="#10b981")
    ax_rad.fill(angles, v_sentinel, '#10b981', alpha=0.25)

    plt.title("Eight-Dimensional Cybersecurity Capability Comparison", size=10, fontweight='bold', color="#0f172a", y=1.08)
    plt.legend(loc='upper right', bbox_to_anchor=(0.1, 0.1), fontsize=7.5)
    plt.tight_layout()
    plt.savefig(CHART_DIR / "Fig_9_2_Feature_Wise_Radar_Analysis.png")
    plt.savefig(CHART_DIR / "feature_wise_radar_analysis.png")
    plt.close()
    print("Regenerated Fig 9.2 Radar Analysis")

    # Fig 9.3: Confusion Matrix Heatmap
    plt.figure(figsize=(5.5, 4.5), dpi=300)
    cm = np.array([[943, 57], [0, 1000]])
    im = plt.imshow(cm, interpolation='nearest', cmap=plt.cm.Blues)
    plt.title("Confusion Matrix: URLSentinel v2.1 (2,000 URLs)", fontsize=10, fontweight='bold', color="#0f172a", pad=12)
    plt.colorbar(im, fraction=0.046, pad=0.04)
    tick_marks = np.arange(2)
    plt.xticks(tick_marks, ["Malicious", "Benign"], fontsize=8.5, fontweight='bold')
    plt.yticks(tick_marks, ["Malicious", "Benign"], fontsize=8.5, fontweight='bold')
    plt.ylabel("Actual Label", fontsize=9, fontweight='bold')
    plt.xlabel("Predicted Label", fontsize=9, fontweight='bold')

    thresh = cm.max() / 2.
    labels = [["TP: 943\n(47.15%)", "FN: 57\n(2.85%)"], ["FP: 0\n(0.00%)", "TN: 1000\n(50.00%)"]]
    for i in range(2):
        for j in range(2):
            plt.text(j, i, labels[i][j], ha="center", va="center", fontsize=8.5, fontweight='bold',
                     color="white" if cm[i, j] > thresh else "black")

    plt.tight_layout()
    plt.savefig(CHART_DIR / "Fig_9_3_Confusion_Matrix_Heatmap.png")
    plt.savefig(CHART_DIR / "confusion_matrix_heatmap.png")
    plt.close()
    print("Regenerated Fig 9.3 Confusion Matrix Heatmap")

if __name__ == "__main__":
    print("Generating redesigned publication-grade diagrams and charts...")
    build_fig_5_1()
    build_fig_5_2()
    build_fig_5_3()
    build_fig_5_4()
    build_fig_5_5()
    build_fig_5_6()
    build_fig_5_7()
    build_fig_5_8()
    build_fig_6_1()
    build_fig_6_2()
    build_charts()
    print("All diagrams and charts regenerated successfully!")
