r"""
generate_all_clean_diagrams.py
==============================
URLSentinel Publication-Grade Diagram Generator (Final Master Edition)

Generates all 10 architecture, UML, and pipeline diagrams with:
1. Generous canvas size (10.5 x 7.0 inches at 300 DPI) preventing any cramped text.
2. Clean structured cards with integrated header bars (NO floating badges colliding with titles).
3. Generous line heights (3.6 - 4.5 units per line) ensuring zero text spill or overflow.
4. Wide inter-box gaps (8.0 - 12.0 units) so arrows and labels NEVER touch or overlap boxes.
5. Pure orthogonal / straight arrow routing: ZERO crossing lines, ZERO messy diagonals.
6. High-contrast, publication-grade cybersecurity palette (Blue, Emerald, Purple, Rose, Amber).
7. Strict preservation: files placed exclusively in z:\URLSentinel\URLSentinel_PPD_Report\diagrams\
   without modifying the Word docx or pdf reports.
"""

import os
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches

OUT_DIR = Path(r"z:\URLSentinel\URLSentinel_PPD_Report\diagrams")
OUT_DIR.mkdir(parents=True, exist_ok=True)
FONT = 'DejaVu Sans'

# -----------------------------------------------------------------------------
# Core Primitives
# -----------------------------------------------------------------------------
def setup_canvas(width=10.5, height=7.0, dpi=300):
    fig, ax = plt.subplots(figsize=(width, height), dpi=dpi)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')
    fig.patch.set_facecolor('#ffffff')
    ax.set_facecolor('#ffffff')
    return fig, ax

def draw_shadow(ax, x, y, w, h, radius=1.6):
    s = patches.FancyBboxPatch(
        (x + 0.4, y - 0.5), w, h,
        boxstyle=f"round,pad=0.1,rounding_size={radius}",
        fc="#cbd5e1", ec="none", alpha=0.45, zorder=1
    )
    ax.add_patch(s)

def draw_header_card(ax, x, y, w, h, title, lines, theme_color, bg_color, border_color,
                     header_h=6.2, title_size=9.5, body_size=8.0, line_spacing=3.8, radius=1.6):
    """Draws a card with a solid colored header bar and spacious body text."""
    draw_shadow(ax, x, y, w, h, radius=radius)
    # Body Box
    body_box = patches.FancyBboxPatch(
        (x, y), w, h,
        boxstyle=f"round,pad=0.1,rounding_size={radius}",
        ec=border_color, fc=bg_color, lw=1.8, zorder=2
    )
    ax.add_patch(body_box)

    # Header Bar
    header_box = patches.FancyBboxPatch(
        (x, y + h - header_h), w, header_h,
        boxstyle=f"round,pad=0.1,rounding_size={radius}",
        ec=border_color, fc=theme_color, lw=1.8, zorder=3
    )
    ax.add_patch(header_box)

    # Title centered in header bar
    ax.text(x + w/2, y + h - header_h/2, title, ha='center', va='center',
            fontsize=title_size, fontweight='bold', color="#ffffff", family=FONT, zorder=4)

    # Body lines
    sy = y + h - header_h - 2.8
    for line in lines:
        ax.text(x + 2.0, sy, line, ha='left', va='center',
                fontsize=body_size, fontweight='bold', color="#1e293b", family=FONT, zorder=4)
        sy -= line_spacing

def draw_pill(ax, x, y, text, color="#0f172a", border="#94a3b8", bg="#ffffff", fontsize=7.6, zorder=8):
    """Draws a crisp white pill badge for arrow and connector labels."""
    ax.text(x, y, text, ha='center', va='center', fontsize=fontsize, fontweight='bold',
            color=color, family=FONT,
            bbox=dict(boxstyle="round,pad=0.28,rounding_size=0.8", fc=bg, ec=border, lw=1.1, alpha=0.98),
            zorder=zorder)

def draw_arrow(ax, p1, p2, color="#334155", lw=1.8, mutation_scale=13, zorder=5):
    """Draws a direct arrow between two points."""
    ax.annotate("", xy=p2, xytext=p1,
                arrowprops=dict(arrowstyle="-|>", color=color, lw=lw, mutation_scale=mutation_scale, shrinkA=0, shrinkB=0),
                zorder=zorder)

def draw_path_arrow(ax, points, color="#334155", lw=1.8, mutation_scale=13, zorder=5):
    """Draws an orthogonal multi-segment path with an arrowhead at the end."""
    xs = [p[0] for p in points]
    ys = [p[1] for p in points]
    ax.plot(xs, ys, color=color, lw=lw, zorder=zorder)
    ax.annotate("", xy=points[-1], xytext=points[-2],
                arrowprops=dict(arrowstyle="-|>", color=color, lw=lw, mutation_scale=mutation_scale, shrinkA=0, shrinkB=0),
                zorder=zorder)

def save_diagram(fig, filename):
    out_path = OUT_DIR / filename
    plt.subplots_adjust(left=0, right=1, top=1, bottom=0)
    plt.savefig(out_path, dpi=300, facecolor='#ffffff', edgecolor='none')
    plt.close()
    print(f"Generated: {filename}")


# -----------------------------------------------------------------------------
# 1. Fig 5.1: Overall System Architecture Diagram
# -----------------------------------------------------------------------------
def generate_fig_5_1():
    fig, ax = setup_canvas(width=10.5, height=7.0)

    # Title
    ax.text(50, 96.5, "URLSENTINEL OVERALL SYSTEM ARCHITECTURE",
            ha='center', va='center', fontsize=13.5, fontweight='bold', color="#0f172a", family=FONT)
    ax.plot([15, 85], [93.8, 93.8], color="#cbd5e1", lw=1.2)

    # TIER 1: Client / Presentation (Blue)
    t1_y, t1_h, t1_w, gap1 = 76.0, 15.0, 27.0, 5.5
    x1_1 = 4.0
    x1_2 = x1_1 + t1_w + gap1  # 36.5
    x1_3 = x1_2 + t1_w + gap1  # 69.0

    c1_1, c1_2, c1_3 = x1_1 + t1_w/2, x1_2 + t1_w/2, x1_3 + t1_w/2

    draw_header_card(ax, x1_1, t1_y, t1_w, t1_h, "Web Dashboard (Next.js 14)", [
        "• React 18, Tailwind CSS UI",
        "• Real-time SVG gauge animation",
        "• On-demand forensic submission"
    ], "#1e40af", "#eff6ff", "#3b82f6", header_h=5.2, title_size=9.2, body_size=7.8, line_spacing=3.0)

    draw_header_card(ax, x1_2, t1_y, t1_w, t1_h, "Browser Extension (MV3)", [
        "• Chromium Service Worker",
        "• Pre-DOM webNavigation intercept",
        "• Sub-millisecond zero-hour block"
    ], "#1e40af", "#eff6ff", "#3b82f6", header_h=5.2, title_size=9.2, body_size=7.8, line_spacing=3.0)

    draw_header_card(ax, x1_3, t1_y, t1_w, t1_h, "Enterprise REST API", [
        "• FastAPI asynchronous gateway",
        "• Pydantic v2 strict models",
        "• Rate-limited JSON endpoints"
    ], "#1e40af", "#eff6ff", "#3b82f6", header_h=5.2, title_size=9.2, body_size=7.8, line_spacing=3.0)

    # TIER 2: Security Perimeter (Emerald)
    t2_y, t2_h, t2_x, t2_w = 56.5, 12.5, 4.0, 92.0
    draw_header_card(ax, t2_x, t2_y, t2_w, t2_h, "Security Boundary & Ingestion Perimeter", [
        "• Nginx Reverse Proxy  •  Token Bucket Rate Limiting (10 req/s)  •  TLS 1.3 Termination",
        "• Zero-Trust SSRF Defense Boundary: Automated RFC 1918 / Loopback Egress Dropping"
    ], "#065f46", "#ecfdf5", "#10b981", header_h=5.0, title_size=9.5, body_size=8.0, line_spacing=3.2)

    # Arrows Tier 1 -> Tier 2
    for cx, label in [(c1_1, "HTTPS / TLS"), (c1_2, "REST / WebNav"), (c1_3, "API Key Scan")]:
        draw_arrow(ax, (cx, t1_y), (cx, t2_y + t2_h), color="#2563eb", lw=1.8)
        draw_pill(ax, cx, (t1_y + t2_y + t2_h)/2, label, color="#1e40af", border="#93c5fd", bg="#ffffff", fontsize=7.2)

    # TIER 3: Multi-Stage Analytical Pipeline (Purple)
    t3_y, t3_h, t3_w, gap3 = 34.0, 15.5, 21.2, 2.4
    x3_1 = 4.0
    x3_2 = x3_1 + t3_w + gap3  # 27.6
    x3_3 = x3_2 + t3_w + gap3  # 51.2
    x3_4 = x3_3 + t3_w + gap3  # 74.8

    c3_1, c3_2, c3_3, c3_4 = x3_1 + t3_w/2, x3_2 + t3_w/2, x3_3 + t3_w/2, x3_4 + t3_w/2

    draw_header_card(ax, x3_1, t3_y, t3_w, t3_h, "URL Normalizer", [
        "• RFC 3986 parser",
        "• PSL suffix cache",
        "• Punycode decoder",
        "• Latency: <0.12ms"
    ], "#581c87", "#faf5ff", "#8b5cf6", header_h=4.8, title_size=8.8, body_size=7.6, line_spacing=2.6)

    draw_header_card(ax, x3_2, t3_y, t3_w, t3_h, "Lexical & Entropy", [
        "• Shannon H(s) metric",
        "• 25+ syntactic stats",
        "• Subdomain depth",
        "• Latency: <0.85ms"
    ], "#581c87", "#faf5ff", "#8b5cf6", header_h=4.8, title_size=8.8, body_size=7.6, line_spacing=2.6)

    draw_header_card(ax, x3_3, t3_y, t3_w, t3_h, "ML Classifier v2.1", [
        "• Logistic model",
        "• DGA consonant run",
        "• 0% SSO false alarm",
        "• Latency: <0.28ms"
    ], "#581c87", "#faf5ff", "#8b5cf6", header_h=4.8, title_size=8.8, body_size=7.6, line_spacing=2.6)

    draw_header_card(ax, x3_4, t3_y, t3_w, t3_h, "Threat Intelligence", [
        "• URLhaus active feed",
        "• OpenPhish real-time",
        "• Redis cache lookup",
        "• Latency: <0.09ms"
    ], "#581c87", "#faf5ff", "#8b5cf6", header_h=4.8, title_size=8.8, body_size=7.6, line_spacing=2.6)

    # Dispatch Bus Tier 2 -> Tier 3
    d_bus_y = 52.0
    d_bus_color = "#059669"
    ax.plot([50.0, 50.0], [t2_y, d_bus_y], color=d_bus_color, lw=1.8, zorder=4)
    ax.plot([c3_1, c3_4], [d_bus_y, d_bus_y], color=d_bus_color, lw=1.8, zorder=4)
    for cx in [c3_1, c3_2, 50.0, c3_3, c3_4]:
        ax.plot(cx, d_bus_y, marker='o', markersize=4.0, color=d_bus_color, zorder=5)
    for cx in [c3_1, c3_2, c3_3, c3_4]:
        draw_arrow(ax, (cx, d_bus_y), (cx, t3_y + t3_h), color=d_bus_color, lw=1.8)
    draw_pill(ax, 50.0, (t2_y + d_bus_y)/2, "Canonical URL Dispatch", color="#065f46", border="#6ee7b7", bg="#ffffff", fontsize=7.2)

    # TIER 4: Decision & Persistence (Rose & Amber)
    t4_y, t4_h = 7.0, 17.5
    t4_w = 40.0
    gap4 = 12.0
    x4_1 = 4.0
    x4_2 = x4_1 + t4_w + gap4  # 56.0

    c4_1 = x4_1 + t4_w/2
    c4_2 = x4_2 + t4_w/2

    draw_header_card(ax, x4_1, t4_y, t4_w, t4_h, "Multi-Signal Risk Engine", [
        "• Bayesian Threat Synthesis & Dynamic Weighting (0-100)",
        "• Deterministic Verdicts: SAFE  •  ELEVATED  •  MALICIOUS",
        "• Human-Actionable Explainability & Risk Factor Attribution Tags"
    ], "#881337", "#fff1f2", "#f43f5e", header_h=5.2, title_size=9.2, body_size=7.8, line_spacing=3.4)

    draw_header_card(ax, x4_2, t4_y, t4_w, t4_h, "Blockchain & Cryptographic Signer", [
        "• Canonical SHA-256 Forensic Evidence Digest Generator",
        "• Sepolia EVM Contract: ThreatRegistry.sol Anchoring",
        "• Immutable Audit Ledger with Decentralized Non-Repudiation"
    ], "#7c2d12", "#fffbeb", "#f59e0b", header_h=5.2, title_size=9.2, body_size=7.8, line_spacing=3.4)

    # Aggregation Bus Tier 3 -> Tier 4
    a_bus_y = 28.5
    a_bus_color = "#7c3aed"
    for cx in [c3_1, c3_2, c3_3, c3_4]:
        ax.plot([cx, cx], [t3_y, a_bus_y], color=a_bus_color, lw=1.8, zorder=4)
    ax.plot([c3_1, c3_4], [a_bus_y, a_bus_y], color=a_bus_color, lw=1.8, zorder=4)
    for cx in [c3_1, c3_2, c4_1, c3_3, c3_4]:
        ax.plot(cx, a_bus_y, marker='o', markersize=4.0, color=a_bus_color, zorder=5)

    draw_arrow(ax, (c4_1, a_bus_y), (c4_1, t4_y + t4_h), color=a_bus_color, lw=2.0)
    draw_pill(ax, c4_1, (a_bus_y + t4_y + t4_h)/2, "Aggregated Threat Telemetry", color="#581c87", border="#c4b5fd", bg="#ffffff", fontsize=7.2)

    # Arrow Tier 4 Left -> Right (Digest Handoff)
    mid_y_t4 = t4_y + t4_h/2
    draw_arrow(ax, (x4_1 + t4_w, mid_y_t4), (x4_2, mid_y_t4), color="#e11d48", lw=2.0)
    draw_pill(ax, (x4_1 + t4_w + x4_2)/2, mid_y_t4, "Evidence Digest", color="#881337", border="#fda4af", bg="#ffffff", fontsize=7.2)

    save_diagram(fig, "Fig_5_1_System_Architecture.png")


# -----------------------------------------------------------------------------
# 2. Fig 5.2: Use Case Diagram
# -----------------------------------------------------------------------------
def generate_fig_5_2():
    fig, ax = setup_canvas(width=10.5, height=7.0)

    ax.text(50, 96.5, "USE CASE DIAGRAM: URLSENTINEL PLATFORM",
            ha='center', va='center', fontsize=13.5, fontweight='bold', color="#0f172a", family=FONT)
    ax.plot([15, 85], [93.8, 93.8], color="#cbd5e1", lw=1.2)

    # 3 Actors on Left (Generous cards)
    actor_w = 20.0
    actor_h = 13.0
    actor_x = 4.0

    draw_header_card(ax, actor_x, 74.0, actor_w, actor_h, "End User", [
        "• Desktop Browser",
        "• Mobile Web Client"
    ], "#1e40af", "#eff6ff", "#3b82f6", header_h=5.0, title_size=9.2, body_size=7.8, line_spacing=3.2)

    draw_header_card(ax, actor_x, 44.0, actor_w, actor_h, "Security Analyst", [
        "• SOC Investigator",
        "• Threat Auditor"
    ], "#065f46", "#ecfdf5", "#10b981", header_h=5.0, title_size=9.2, body_size=7.8, line_spacing=3.2)

    draw_header_card(ax, actor_x, 14.0, actor_w, actor_h, "Platform Admin", [
        "• DevOps Engineer",
        "• System Custodian"
    ], "#701a75", "#fdf4ff", "#c026d3", header_h=5.0, title_size=9.2, body_size=7.8, line_spacing=3.2)

    # System Boundary Box
    sb_x, sb_y, sb_w, sb_h = 30.0, 5.0, 66.0, 86.0
    sb = patches.FancyBboxPatch(
        (sb_x, sb_y), sb_w, sb_h,
        boxstyle="round,pad=0.2,rounding_size=2.0",
        ec="#64748b", fc="#ffffff", lw=1.6, linestyle="--", zorder=2
    )
    ax.add_patch(sb)
    ax.text(sb_x + sb_w/2, sb_y + sb_h - 2.8, "URLSentinel Security Platform (Boundary)",
            ha='center', va='center', fontsize=10.0, fontweight='bold', color="#334155", family=FONT, zorder=3)

    # Helper for Use Case Oval
    def draw_uc(cx, cy, w, h, text):
        draw_shadow(ax, cx, cy, w, h, radius=h/2)
        oval = patches.FancyBboxPatch(
            (cx, cy), w, h,
            boxstyle=f"round,pad=0.1,rounding_size={h/2}",
            ec="#3b82f6", fc="#f8fafc", lw=1.5, zorder=3
        )
        ax.add_patch(oval)
        ax.text(cx + w/2, cy + h/2, text, ha='center', va='center',
                fontsize=8.5, fontweight='bold', color="#0f172a", family=FONT, zorder=4)

    # Use Cases - Column 1 (X = 34.0, W = 28.0, H = 6.2)
    uc_w, uc_h = 28.0, 6.2
    c1_x = 34.0
    draw_uc(c1_x, 78.0, uc_w, uc_h, "Submit URL for Analysis")       # UC1
    draw_uc(c1_x, 69.0, uc_w, uc_h, "View Risk Gauge & Verdict")     # UC2
    draw_uc(c1_x, 60.0, uc_w, uc_h, "Live Navigation Hook")          # UC3

    # Analyst Section
    draw_uc(c1_x, 48.0, uc_w, uc_h, "Inspect Evidence Breakdown")   # UC4
    draw_uc(c1_x, 39.0, uc_w, uc_h, "Verify Blockchain Receipt")    # UC5
    draw_uc(c1_x, 30.0, uc_w, uc_h, "Report False Positive")        # UC6

    # Admin Section
    draw_uc(c1_x, 18.0, uc_w, uc_h, "Trigger Threat Feed Sync")     # UC7
    draw_uc(c1_x, 9.0,  uc_w, uc_h, "Review System Telemetry")      # UC8

    # Column 2 Use Cases (X = 66.0, W = 28.0, H = 6.2)
    c2_x = 66.0
    draw_uc(c2_x, 48.0, uc_w, uc_h, "Query Domain Intel API")       # UC9
    draw_uc(c2_x, 39.0, uc_w, uc_h, "Audit Cryptographic Proofs")   # UC10
    draw_uc(c2_x, 18.0, uc_w, uc_h, "Manage API Keys & Quotas")     # UC11

    # Connectors - Clean direct / orthogonal routing without intersecting other ovals
    u_right = actor_x + actor_w
    u_mid = 74.0 + actor_h/2
    for uc_y in [78.0 + uc_h/2, 69.0 + uc_h/2, 60.0 + uc_h/2]:
        draw_path_arrow(ax, [(u_right, u_mid), (28.0, u_mid), (28.0, uc_y), (c1_x, uc_y)], color="#2563eb", lw=1.6)

    # Analyst Connections
    a_mid = 44.0 + actor_h/2
    for uc_y in [48.0 + uc_h/2, 39.0 + uc_h/2, 30.0 + uc_h/2]:
        draw_path_arrow(ax, [(u_right, a_mid), (28.0, a_mid), (28.0, uc_y), (c1_x, uc_y)], color="#059669", lw=1.6)
    # Analyst to Col 2
    for uc_y in [48.0 + uc_h/2, 39.0 + uc_h/2]:
        draw_arrow(ax, (c1_x + uc_w, uc_y), (c2_x, uc_y), color="#059669", lw=1.6)

    # Admin Connections
    ad_mid = 14.0 + actor_h/2
    for uc_y in [18.0 + uc_h/2, 9.0 + uc_h/2]:
        draw_path_arrow(ax, [(u_right, ad_mid), (28.0, ad_mid), (28.0, uc_y), (c1_x, uc_y)], color="#9333ea", lw=1.6)
    # Admin to Col 2
    draw_arrow(ax, (c1_x + uc_w, 18.0 + uc_h/2), (c2_x, 18.0 + uc_h/2), color="#9333ea", lw=1.6)

    save_diagram(fig, "Fig_5_2_Use_Case_Diagram.png")


# -----------------------------------------------------------------------------
# 3. Fig 5.3: Entity Relationship Diagram (ERD)
# -----------------------------------------------------------------------------
def generate_fig_5_3():
    fig, ax = setup_canvas(width=10.5, height=7.0)

    ax.text(50, 96.5, "ENTITY RELATIONSHIP DIAGRAM (ERD)",
            ha='center', va='center', fontsize=13.5, fontweight='bold', color="#0f172a", family=FONT)
    ax.plot([15, 85], [93.8, 93.8], color="#cbd5e1", lw=1.2)

    def draw_entity_table(x, y, w, h, name, fields, header_color="#1e293b", border="#475569"):
        draw_shadow(ax, x, y, w, h)
        box = patches.FancyBboxPatch(
            (x, y), w, h,
            boxstyle="round,pad=0.1,rounding_size=1.5",
            ec=border, fc="#ffffff", lw=1.8, zorder=2
        )
        ax.add_patch(box)
        hh = 5.2
        header_box = patches.FancyBboxPatch(
            (x, y + h - hh), w, hh,
            boxstyle="round,pad=0.1,rounding_size=1.5",
            ec=border, fc=header_color, lw=1.8, zorder=3
        )
        ax.add_patch(header_box)
        ax.text(x + w/2, y + h - hh/2, name, ha='center', va='center',
                fontsize=10.0, fontweight='bold', color="#ffffff", family=FONT, zorder=4)

        fy = y + h - hh - 2.8
        for ftype, fname, ftype_desc in fields:
            prefix_color = "#dc2626" if ftype == "PK" else ("#2563eb" if ftype == "FK" else "#64748b")
            ax.text(x + 1.8, fy, ftype, ha='left', va='center',
                    fontsize=7.8, fontweight='bold', color=prefix_color, family=FONT, zorder=4)
            ax.text(x + 5.5, fy, fname, ha='left', va='center',
                    fontsize=8.2, fontweight='bold', color="#0f172a", family=FONT, zorder=4)
            ax.text(x + w - 1.8, fy, ftype_desc, ha='right', va='center',
                    fontsize=7.6, fontweight='bold', color="#475569", family=FONT, zorder=4)
            fy -= 3.6

    # Top Row: SCAN_REQUEST, VERDICT_RECORD, BLOCKCHAIN_ANCHOR
    t_y, t_h, w_top, gap_top = 54.0, 36.0, 27.5, 4.75
    x_sr = 4.0
    x_vr = x_sr + w_top + gap_top  # 36.25
    x_ba = x_vr + w_top + gap_top  # 68.5

    draw_entity_table(x_sr, t_y, w_top, t_h, "SCAN_REQUEST", [
        ("PK", "id", "UUID"),
        ("  ", "canonical_url", "TEXT"),
        ("  ", "url_hash", "VARCHAR(64)"),
        ("  ", "client_ip", "VARCHAR(45)"),
        ("  ", "status", "ENUM"),
        ("  ", "created_at", "TIMESTAMP"),
    ], header_color="#1e3a8a", border="#3b82f6")

    draw_entity_table(x_vr, t_y, w_top, t_h, "VERDICT_RECORD", [
        ("PK", "id", "UUID"),
        ("FK", "scan_id", "UUID"),
        ("  ", "verdict", "ENUM"),
        ("  ", "risk_score", "INT(0-100)"),
        ("  ", "signed_digest", "VARCHAR(64)"),
        ("  ", "confidence", "ENUM"),
    ], header_color="#881337", border="#f43f5e")

    draw_entity_table(x_ba, t_y, w_top, t_h, "BLOCKCHAIN_ANCHOR", [
        ("PK", "tx_hash", "VARCHAR(66)"),
        ("FK", "verdict_id", "UUID"),
        ("  ", "merkle_root", "VARCHAR(64)"),
        ("  ", "block_number", "BIGINT"),
        ("  ", "contract_addr", "VARCHAR(42)"),
        ("  ", "anchored_at", "TIMESTAMP"),
    ], header_color="#7c2d12", border="#f59e0b")

    # Bottom Row: EVIDENCE_SIGNAL, THREAT_INTEL_ENTRY
    b_y, b_h, w_bot, gap_bot = 8.0, 37.0, 43.5, 5.0
    x_es = 4.0
    x_ti = x_es + w_bot + gap_bot  # 52.5

    draw_entity_table(x_es, b_y, w_bot, b_h, "EVIDENCE_SIGNAL", [
        ("PK", "id", "UUID"),
        ("FK", "verdict_id", "UUID"),
        ("  ", "layer_source", "ENUM (LEX, ML, TI, DNS)"),
        ("  ", "signal_name", "VARCHAR(64)"),
        ("  ", "weight_contribution", "FLOAT"),
        ("  ", "human_explanation", "TEXT"),
        ("  ", "observed_at", "TIMESTAMP"),
    ], header_color="#581c87", border="#8b5cf6")

    draw_entity_table(x_ti, b_y, w_bot, b_h, "THREAT_INTEL_ENTRY", [
        ("PK", "id", "UUID"),
        ("  ", "indicator", "VARCHAR(255)"),
        ("  ", "source_feed", "ENUM (URLhaus, OpenPhish)"),
        ("  ", "threat_type", "ENUM (PHISH, MALWARE)"),
        ("  ", "confidence_level", "FLOAT"),
        ("  ", "is_active", "BOOLEAN"),
        ("  ", "last_synced_at", "TIMESTAMP"),
    ], header_color="#065f46", border="#10b981")

    # Relationships
    sr_mid_y = t_y + t_h/2
    draw_arrow(ax, (x_sr + w_top, sr_mid_y), (x_vr, sr_mid_y), color="#2563eb", lw=1.8)
    draw_pill(ax, (x_sr + w_top + x_vr)/2, sr_mid_y, "1 : 1\ngenerates", color="#1e40af", border="#93c5fd", bg="#ffffff", fontsize=7.2)

    draw_arrow(ax, (x_vr + w_top, sr_mid_y), (x_ba, sr_mid_y), color="#d97706", lw=1.8)
    draw_pill(ax, (x_vr + w_top + x_ba)/2, sr_mid_y, "1 : 1\nanchors", color="#7c2d12", border="#fcd34d", bg="#ffffff", fontsize=7.2)

    c_vr = x_vr + w_top/2
    c_es = x_es + w_bot/2
    draw_path_arrow(ax, [(c_vr - 6.0, t_y), (c_vr - 6.0, 48.0), (c_es, 48.0), (c_es, b_y + b_h)], color="#7c3aed", lw=1.8)
    draw_pill(ax, (c_es + c_vr - 6.0)/2, 48.0, "1 : N produces", color="#581c87", border="#c4b5fd", bg="#ffffff", fontsize=7.5)

    c_ti = x_ti + w_bot/2
    draw_path_arrow(ax, [(c_ti, b_y + b_h), (c_ti, 48.0), (c_vr + 6.0, 48.0), (c_vr + 6.0, t_y)], color="#059669", lw=1.8)
    draw_pill(ax, (c_ti + c_vr + 6.0)/2, 48.0, "M : N correlates", color="#065f46", border="#6ee7b7", bg="#ffffff", fontsize=7.5)

    save_diagram(fig, "Fig_5_3_Entity_Relationship_Diagram.png")


# -----------------------------------------------------------------------------
# 4. Fig 5.4: Activity Diagram
# -----------------------------------------------------------------------------
def generate_fig_5_4():
    fig, ax = setup_canvas(width=10.5, height=7.0)

    ax.text(50, 96.5, "ACTIVITY DIAGRAM: URL DETECTION WORKFLOW",
            ha='center', va='center', fontsize=13.5, fontweight='bold', color="#0f172a", family=FONT)
    ax.plot([15, 85], [93.8, 93.8], color="#cbd5e1", lw=1.2)

    # Start Node
    ax.plot(30.0, 89.0, marker='o', markersize=14, color="#10b981", zorder=4)

    # Step 1: Ingest URL
    draw_header_card(ax, 14.0, 75.0, 32.0, 9.5, "1. Ingest Raw URL", [
        "• Client or extension navigation hook"
    ], "#1e40af", "#eff6ff", "#3b82f6", header_h=4.5, title_size=9.0, body_size=7.6, line_spacing=2.2)
    draw_arrow(ax, (30.0, 87.0), (30.0, 84.5), color="#334155")

    # Step 2: RFC 3986 Parsing
    draw_header_card(ax, 14.0, 61.5, 32.0, 9.5, "2. RFC 3986 Normalization", [
        "• Punycode & PSL suffix decomposition"
    ], "#581c87", "#faf5ff", "#8b5cf6", header_h=4.5, title_size=9.0, body_size=7.6, line_spacing=2.2)
    draw_arrow(ax, (30.0, 75.0), (30.0, 71.0), color="#334155")

    # Decision Diamond: SSRF Check
    d_x, d_y = 30.0, 48.5
    dw, dh = 11.0, 6.0
    diamond = patches.Polygon([
        (d_x, d_y + dh), (d_x + dw, d_y), (d_x, d_y - dh), (d_x - dw, d_y)
    ], closed=True, ec="#ef4444", fc="#fef2f2", lw=1.8, zorder=3)
    ax.add_patch(diamond)
    ax.text(d_x, d_y, "Private IP /\nSSRF Target?", ha='center', va='center',
            fontsize=8.2, fontweight='bold', color="#991b1b", family=FONT, zorder=4)

    draw_arrow(ax, (30.0, 61.5), (30.0, d_y + dh), color="#334155")

    # SSRF Branch [Yes] -> Right
    draw_header_card(ax, 62.0, 43.5, 32.0, 10.0, "Reject: SSRF Defense Blocked", [
        "• Drops RFC 1918 / IMDS egress target"
    ], "#991b1b", "#fee2e2", "#ef4444", header_h=4.5, title_size=9.0, body_size=7.6, line_spacing=2.2)

    draw_arrow(ax, (d_x + dw, d_y), (62.0, d_y), color="#dc2626", lw=1.8)
    draw_pill(ax, (d_x + dw + 62.0)/2, d_y + 2.5, "Yes [SSRF]", color="#dc2626", border="#fca5a5", bg="#ffffff", fontsize=7.2)

    # SSRF End Bullseye
    ax.plot(78.0, 31.0, marker='o', markersize=14, color="#ef4444", zorder=4)
    ax.plot(78.0, 31.0, marker='x', markersize=8, color="#ffffff", markeredgewidth=2.0, zorder=5)
    draw_arrow(ax, (78.0, 43.5), (78.0, 33.5), color="#dc2626")

    # SSRF Branch [No] -> Proceed Down
    # Step 3: Parallel Engines
    draw_header_card(ax, 14.0, 27.5, 32.0, 10.5, "3. Parallel Feature Engines", [
        "• Lexical • Homoglyph • ML • Feeds"
    ], "#065f46", "#ecfdf5", "#10b981", header_h=4.5, title_size=9.0, body_size=7.6, line_spacing=2.2)
    draw_arrow(ax, (30.0, d_y - dh), (30.0, 38.0), color="#059669", lw=1.8)
    draw_pill(ax, 30.0, (d_y - dh + 38.0)/2, "No [Public]", color="#059669", border="#6ee7b7", bg="#ffffff", fontsize=7.2)

    # Step 4: Multi-Signal Bayesian Verdict
    draw_header_card(ax, 14.0, 13.0, 32.0, 10.5, "4. Multi-Signal Synthesis", [
        "• Bayesian Score (0-100) & Provenance"
    ], "#881337", "#fff1f2", "#f43f5e", header_h=4.5, title_size=9.0, body_size=7.6, line_spacing=2.2)
    draw_arrow(ax, (30.0, 27.5), (30.0, 23.5), color="#334155")

    # Step 5: Render Response & Sign Hash
    draw_header_card(ax, 58.0, 13.0, 32.0, 10.5, "5. Render UI & Emit Verdict", [
        "• Display Risk Gauge & JWS Digest"
    ], "#1e3a8a", "#eff6ff", "#3b82f6", header_h=4.5, title_size=9.0, body_size=7.6, line_spacing=2.2)
    draw_arrow(ax, (46.0, 18.25), (58.0, 18.25), color="#334155")
    draw_pill(ax, 52.0, 18.25, "Score", color="#881337", border="#fda4af", bg="#ffffff", fontsize=7.2)

    # Final Complete Node
    ax.plot(94.0, 18.25, marker='o', markersize=16, color="#0f172a", fillstyle='none', markeredgewidth=2.0, zorder=4)
    ax.plot(94.0, 18.25, marker='o', markersize=9, color="#10b981", zorder=5)
    draw_arrow(ax, (90.0, 18.25), (92.5, 18.25), color="#059669")

    save_diagram(fig, "Fig_5_4_Activity_Diagram.png")


# -----------------------------------------------------------------------------
# 5. Fig 5.5: Class Diagram
# -----------------------------------------------------------------------------
def generate_fig_5_5():
    fig, ax = setup_canvas(width=10.5, height=7.0)

    ax.text(50, 96.5, "CLASS DIAGRAM: OBJECT-ORIENTED ENGINE MODEL",
            ha='center', va='center', fontsize=13.5, fontweight='bold', color="#0f172a", family=FONT)
    ax.plot([15, 85], [93.8, 93.8], color="#cbd5e1", lw=1.2)

    def draw_uml_class(x, y, w, h, name, attrs, methods, header_color="#1e3a8a", border="#3b82f6"):
        draw_shadow(ax, x, y, w, h)
        box = patches.FancyBboxPatch(
            (x, y), w, h, boxstyle="round,pad=0.1,rounding_size=1.5",
            ec=border, fc="#ffffff", lw=1.8, zorder=2
        )
        ax.add_patch(box)
        hh = 5.2
        hb = patches.FancyBboxPatch(
            (x, y + h - hh), w, hh, boxstyle="round,pad=0.1,rounding_size=1.5",
            ec=border, fc=header_color, lw=1.8, zorder=3
        )
        ax.add_patch(hb)
        ax.text(x + w/2, y + h - hh/2, name, ha='center', va='center',
                fontsize=9.8, fontweight='bold', color="#ffffff", family=FONT, zorder=4)

        cur_y = y + h - hh - 2.6
        for a in attrs:
            ax.text(x + 1.8, cur_y, a, ha='left', va='center',
                    fontsize=8.0, fontweight='bold', color="#334155", family=FONT, zorder=4)
            cur_y -= 3.2

        cur_y -= 0.6
        ax.plot([x + 1.0, x + w - 1.0], [cur_y, cur_y], color=border, lw=1.0, alpha=0.5, zorder=3)
        cur_y -= 2.6

        for m in methods:
            ax.text(x + 1.8, cur_y, m, ha='left', va='center',
                    fontsize=8.0, fontweight='bold', color="#0f172a", family=FONT, zorder=4)
            cur_y -= 3.2

    # Top Row Classes: URLNormalizer, MLClassifier, HomoglyphDetector
    top_y, top_h, top_w, gap_t = 50.0, 40.0, 28.0, 4.0
    x_un = 4.0
    x_ml = x_un + top_w + gap_t  # 36.0
    x_hd = x_ml + top_w + gap_t  # 68.0

    draw_uml_class(x_un, top_y, top_w, top_h, "URLNormalizer",
                   ["- raw_url: str", "- canonical_url: str", "- host_etld: str", "- psl_cache: Cache"],
                   ["+ normalize(url: str): str", "+ parse_components(): Dict", "+ compute_sha256(): str", "+ is_ip_destination(): bool"],
                   header_color="#1e3a8a", border="#3b82f6")

    draw_uml_class(x_ml, top_y, top_w, top_h, "MLClassifier",
                   ["- INTERCEPT: float = -3.80", "- WEIGHTS: Dict[str, float]", "- SENSITIVITY: float", "- MODEL_VERSION: str"],
                   ["+ extract_features(url): Dict", "+ predict_proba(feats): float", "+ get_attributions(): List", "+ calculate_entropy(): float"],
                   header_color="#581c87", border="#8b5cf6")

    draw_uml_class(x_hd, top_y, top_w, top_h, "HomoglyphDetector",
                   ["- BRAND_TARGETS: List[str]", "- CONFUSABLE_MAP: Dict", "- MAX_DISTANCE: int = 2", "- PUNYCODE_PREFIX: str"],
                   ["+ detect_spoof(host): Dict", "+ levenshtein_distance(): int", "+ normalize_punycode(): str", "+ check_subdomain_brand(): bool"],
                   header_color="#065f46", border="#10b981")

    # Bottom Row Classes: VerdictEngine, ThreatRegistryClient
    bot_y, bot_h, bot_w, gap_b = 6.0, 36.0, 43.0, 6.0
    x_ve = 4.0
    x_tr = x_ve + bot_w + gap_b  # 53.0

    draw_uml_class(x_ve, bot_y, bot_w, bot_h, "VerdictEngine",
                   ["- RISK_THRESHOLD_HIGH: float = 65.0", "- HONESTY_POLICY_ACTIVE: bool = True", "- evidence_ledger: List[Dict]"],
                   ["+ synthesize_verdict(signals: Dict): VerdictResponse", "+ enforce_truthful_guarantee(): void", "+ generate_tamper_digest(): str", "+ format_forensic_breakdown(): List"],
                   header_color="#881337", border="#f43f5e")

    draw_uml_class(x_tr, bot_y, bot_w, bot_h, "ThreatRegistryClient",
                   ["- rpc_endpoint: str", "- contract_address: str", "- chain_id: int = 11155111", "- gas_limit: int = 150000"],
                   ["+ anchor_evidence_digest(tx_payload: Dict): str", "+ query_evidence_receipt(url_hash: str): Dict", "+ verify_receipt_cryptographically(): bool"],
                   header_color="#7c2d12", border="#f59e0b")

    # Connectors
    c_un = x_un + top_w/2
    c_ml = x_ml + top_w/2
    c_hd = x_hd + top_w/2
    c_ve = x_ve + bot_w/2

    draw_path_arrow(ax, [(c_un, top_y), (c_un, 45.0), (c_ve - 10.0, 45.0), (c_ve - 10.0, bot_y + bot_h)], color="#2563eb")
    draw_path_arrow(ax, [(c_ml, top_y), (c_ml, 45.0), (c_ve, 45.0), (c_ve, bot_y + bot_h)], color="#7c3aed")
    draw_path_arrow(ax, [(c_hd, top_y), (c_hd, 45.0), (c_ve + 10.0, 45.0), (c_ve + 10.0, bot_y + bot_h)], color="#059669")

    ve_mid_y = bot_y + bot_h/2
    draw_arrow(ax, (x_ve + bot_w, ve_mid_y), (x_tr, ve_mid_y), color="#e11d48", lw=2.0)
    draw_pill(ax, (x_ve + bot_w + x_tr)/2, ve_mid_y, "Signed Evidence\nDigest", color="#881337", border="#fda4af", bg="#ffffff", fontsize=7.2)

    save_diagram(fig, "Fig_5_5_Class_Diagram.png")


# -----------------------------------------------------------------------------
# 6. Fig 5.6: Sequence Diagram
# -----------------------------------------------------------------------------
def generate_fig_5_6():
    fig, ax = setup_canvas(width=10.5, height=7.0)

    ax.text(50, 96.5, "SEQUENCE DIAGRAM: END-TO-END SCAN EXECUTION",
            ha='center', va='center', fontsize=13.5, fontweight='bold', color="#0f172a", family=FONT)
    ax.plot([15, 85], [93.8, 93.8], color="#cbd5e1", lw=1.2)

    # 5 Lifelines
    entities = [
        (10.0, "Client / Ext", "#1e40af", "#eff6ff", "#3b82f6"),
        (30.0, "API Gateway", "#065f46", "#ecfdf5", "#10b981"),
        (50.0, "SSRF Guard", "#991b1b", "#fef2f2", "#ef4444"),
        (70.0, "Engines / ML", "#581c87", "#faf5ff", "#8b5cf6"),
        (90.0, "Verdict & Chain", "#881337", "#fff1f2", "#f43f5e")
    ]

    header_w = 15.0
    header_h = 6.0
    header_y = 86.0

    for lx, name, tc, bg, bc in entities:
        draw_header_card(ax, lx - header_w/2, header_y, header_w, header_h, name, [],
                         theme_color=tc, bg_color=bg, border_color=bc, header_h=header_h, title_size=8.8)
        ax.plot([lx, lx], [header_y, 5.0], color="#cbd5e1", linestyle="--", lw=1.2, zorder=1)

    messages = [
        (79.0, 10.0, 30.0, "1: POST /api/v1/scan {url}", "#2563eb", False),
        (70.0, 30.0, 50.0, "2: validate_destination_ip(host)", "#059669", False),
        (61.0, 50.0, 30.0, "3: IP Verified (Public Origin: PASS)", "#16a34a", True),
        (52.0, 30.0, 70.0, "4: run_feature_pipeline_async()", "#7c3aed", False),
        (43.0, 70.0, 90.0, "5: return feature_vectors & risk_prior", "#7c3aed", False),
        (34.0, 90.0, 90.0, "6: synthesize_bayesian_verdict()", "#881337", "self"),
        (24.0, 90.0, 90.0, "7: anchor_sha256_digest_onchain()", "#d97706", "self"),
        (14.0, 90.0, 10.0, "8: HTTP 200: VerdictResponse (Risk, Gauge, Digest)", "#1e40af", True),
    ]

    for y, x1, x2, text, color, is_ret in messages:
        if is_ret == "self":
            # Self-loop cleanly drawn pointing LEFT into gap between 70 and 90
            ax.plot([x1, x1 - 5.0, x1 - 5.0, x1], [y, y, y - 3.8, y - 3.8], color=color, lw=1.8, zorder=4)
            ax.annotate("", xy=(x1, y - 3.8), xytext=(x1 - 5.0, y - 3.8),
                        arrowprops=dict(arrowstyle="-|>", color=color, lw=1.8, mutation_scale=11, shrinkA=0, shrinkB=0),
                        zorder=5)
            draw_pill(ax, x1 - 15.0, y - 1.9, text, color=color, border="#cbd5e1", bg="#ffffff", fontsize=7.4)
        else:
            style = "--" if is_ret else "-"
            ax.plot([x1, x2], [y, y], color=color, linestyle=style, lw=1.6, zorder=4)
            ax.annotate("", xy=(x2, y), xytext=(x1, y),
                        arrowprops=dict(arrowstyle="-|>", color=color, lw=1.6, mutation_scale=12, shrinkA=0, shrinkB=0),
                        zorder=5)
            draw_pill(ax, (x1 + x2)/2, y + 2.5, text, color=color, border="#cbd5e1", bg="#ffffff", fontsize=7.6)

    save_diagram(fig, "Fig_5_6_Sequence_Diagram.png")


# -----------------------------------------------------------------------------
# 7. Fig 5.7: Data Flow Diagram Level 0 (Context Level)
# -----------------------------------------------------------------------------
def generate_fig_5_7():
    fig, ax = setup_canvas(width=10.5, height=7.0)

    ax.text(50, 96.5, "DATA FLOW DIAGRAM (DFD) LEVEL 0: CONTEXT DIAGRAM",
            ha='center', va='center', fontsize=13.5, fontweight='bold', color="#0f172a", family=FONT)
    ax.plot([15, 85], [93.8, 93.8], color="#cbd5e1", lw=1.2)

    # 4 External Entities in Corners (Generous dimensions)
    ent_w, ent_h = 25.0, 15.0

    # Top-Left: Client
    tl_x, tl_y = 4.0, 74.0
    draw_header_card(ax, tl_x, tl_y, ent_w, ent_h, "Web User / Client", [
        "• Submits unverified URL",
        "• Receives Risk Gauge UI",
        "• Real-time browser blockade"
    ], "#1e40af", "#eff6ff", "#3b82f6", header_h=5.0, title_size=9.2, body_size=7.8, line_spacing=3.0)

    # Bottom-Left: Threat Feeds
    bl_x, bl_y = 4.0, 10.0
    draw_header_card(ax, bl_x, bl_y, ent_w, ent_h, "Threat Intel Feeds", [
        "• URLhaus active malware feed",
        "• OpenPhish phishing feed",
        "• 15-min scheduled ingestion"
    ], "#065f46", "#ecfdf5", "#10b981", header_h=5.0, title_size=9.2, body_size=7.8, line_spacing=3.0)

    # Top-Right: Auditor
    tr_x, tr_y = 71.0, 74.0
    draw_header_card(ax, tr_x, tr_y, ent_w, ent_h, "Security Auditor", [
        "• Queries forensic receipts",
        "• Inspects evidence ledger",
        "• Validates non-tampering"
    ], "#581c87", "#faf5ff", "#8b5cf6", header_h=5.0, title_size=9.2, body_size=7.8, line_spacing=3.0)

    # Bottom-Right: Blockchain
    br_x, br_y = 71.0, 10.0
    draw_header_card(ax, br_x, br_y, ent_w, ent_h, "EVM Blockchain Ledger", [
        "• ThreatRegistry.sol contract",
        "• Immutable SHA-256 digests",
        "• Sepolia testnet anchoring"
    ], "#7c2d12", "#fffbeb", "#f59e0b", header_h=5.0, title_size=9.2, body_size=7.8, line_spacing=3.0)

    # Central Process Circle 0.0
    cp_x, cp_y = 50.0, 48.0
    cp_r = 14.5

    draw_shadow(ax, cp_x - cp_r, cp_y - cp_r, 2*cp_r, 2*cp_r, radius=cp_r)
    circ = patches.Circle((cp_x, cp_y), cp_r, ec="#065f46", fc="#ecfdf5", lw=2.2, zorder=3)
    ax.add_patch(circ)
    circ_inner = patches.Circle((cp_x, cp_y), cp_r - 1.2, ec="#10b981", fc="#ffffff", lw=1.2, linestyle="--", zorder=3)
    ax.add_patch(circ_inner)

    ax.text(cp_x, cp_y + 5.0, "0.0", ha='center', va='center',
            fontsize=12.0, fontweight='bold', color="#065f46", family=FONT, zorder=4)
    ax.text(cp_x, cp_y + 1.0, "URLSENTINEL", ha='center', va='center',
            fontsize=10.5, fontweight='bold', color="#0f172a", family=FONT, zorder=4)
    ax.text(cp_x, cp_y - 3.2, "PLATFORM", ha='center', va='center',
            fontsize=9.5, fontweight='bold', color="#0f172a", family=FONT, zorder=4)
    ax.text(cp_x, cp_y - 7.2, "Threat Detection Engine", ha='center', va='center',
            fontsize=7.8, fontweight='bold', color="#059669", family=FONT, zorder=4)

    # Clean Flows between Entities and Center
    # 1. User -> System
    draw_path_arrow(ax, [(tl_x + ent_w, tl_y + 10.0), (38.0, tl_y + 10.0), (38.0, cp_y + 11.0)], color="#2563eb", lw=1.8)
    draw_pill(ax, 38.0, tl_y + 12.5, "1. Unverified Target URL", color="#1e40af", border="#93c5fd", bg="#ffffff", fontsize=7.4)

    # 2. System -> User
    draw_path_arrow(ax, [(36.0, cp_y + 2.0), (32.0, cp_y + 2.0), (32.0, tl_y + 4.0), (tl_x + ent_w, tl_y + 4.0)], color="#16a34a", lw=1.8)
    draw_pill(ax, 32.0, 68.0, "2. Risk Gauge & Verdict", color="#15803d", border="#86efac", bg="#ffffff", fontsize=7.4)

    # 3. Feeds -> System
    draw_path_arrow(ax, [(bl_x + ent_w, bl_y + 9.0), (40.0, bl_y + 9.0), (40.0, cp_y - 11.0)], color="#059669", lw=1.8)
    draw_pill(ax, 38.0, bl_y + 11.5, "3. Threat Feed Signatures", color="#065f46", border="#6ee7b7", bg="#ffffff", fontsize=7.4)

    # 4. System -> Blockchain
    draw_path_arrow(ax, [(60.0, cp_y - 11.0), (60.0, br_y + 9.0), (br_x, br_y + 9.0)], color="#d97706", lw=1.8)
    draw_pill(ax, 62.0, br_y + 11.5, "4. SHA-256 Digest Anchor", color="#7c2d12", border="#fcd34d", bg="#ffffff", fontsize=7.4)

    # 5. Auditor -> System
    draw_path_arrow(ax, [(tr_x, tr_y + 4.0), (68.0, tr_y + 4.0), (68.0, cp_y + 2.0), (64.0, cp_y + 2.0)], color="#7c3aed", lw=1.8)
    draw_pill(ax, 68.0, 68.0, "5. Query Verification Hash", color="#581c87", border="#c4b5fd", bg="#ffffff", fontsize=7.4)

    # 6. System -> Auditor
    draw_path_arrow(ax, [(62.0, cp_y + 11.0), (62.0, tr_y + 10.0), (tr_x, tr_y + 10.0)], color="#0284c7", lw=1.8)
    draw_pill(ax, 62.0, tr_y + 12.5, "6. Signed Provenance Receipt", color="#0369a1", border="#7dd3fc", bg="#ffffff", fontsize=7.4)

    save_diagram(fig, "Fig_5_7_DFD_Level_0.png")


# -----------------------------------------------------------------------------
# 8. Fig 5.8: Data Flow Diagram Level 1 (Decomposition)
# -----------------------------------------------------------------------------
def generate_fig_5_8():
    fig, ax = setup_canvas(width=10.5, height=7.0)

    ax.text(50, 96.5, "DATA FLOW DIAGRAM (DFD) LEVEL 1: SUB-PROCESS DECOMPOSITION",
            ha='center', va='center', fontsize=13.0, fontweight='bold', color="#0f172a", family=FONT)
    ax.plot([15, 85], [93.8, 93.8], color="#cbd5e1", lw=1.2)

    # 2 Rows of Processes + 1 Bottom Row of Data Stores
    # Row 1: 1.0 (left), 2.0 (center), 3.0 (right)
    top_y = 65.0
    p_h = 18.0
    p_w = 26.5
    gap_p = 7.0
    x_p1 = 4.0
    x_p2 = x_p1 + p_w + gap_p  # 37.5
    x_p3 = x_p2 + p_w + gap_p  # 71.0

    draw_header_card(ax, x_p1, top_y, p_w, p_h, "1.0 Ingestion & Parsing", [
        "• RFC 3986 normalization",
        "• Public Suffix List cache",
        "• Punycode decoding"
    ], "#1e40af", "#eff6ff", "#3b82f6", header_h=5.0, title_size=9.2, body_size=7.8, line_spacing=3.2)

    draw_header_card(ax, x_p2, top_y, p_w, p_h, "2.0 SSRF & Ingress Gate", [
        "• DNS resolution of host",
        "• Drop RFC 1918 / IMDS",
        "• Loopback egress block"
    ], "#991b1b", "#fef2f2", "#ef4444", header_h=5.0, title_size=9.2, body_size=7.8, line_spacing=3.2)

    draw_header_card(ax, x_p3, top_y, p_w, p_h, "3.0 Feature Extraction", [
        "• Shannon Entropy H(s)",
        "• Levenshtein brand check",
        "• 25+ syntactic features"
    ], "#581c87", "#faf5ff", "#8b5cf6", header_h=5.0, title_size=9.2, body_size=7.8, line_spacing=3.2)

    # Row 2: 4.0 (right), 5.0 (center)
    mid_y = 35.0
    x_p4 = 71.0
    x_p5 = 37.5

    draw_header_card(ax, x_p4, mid_y, p_w, p_h, "4.0 ML Inference", [
        "• Calibrated model v2.1",
        "• Sigmoid risk probability",
        "• Factor attribution vector"
    ], "#065f46", "#ecfdf5", "#10b981", header_h=5.0, title_size=9.2, body_size=7.8, line_spacing=3.2)

    draw_header_card(ax, x_p5, mid_y, p_w, p_h, "5.0 Verdict Synthesis", [
        "• Multi-signal Bayesian mix",
        "• Dynamic score (0-100)",
        "• Tamper-evident digest"
    ], "#881337", "#fff1f2", "#f43f5e", header_h=5.0, title_size=9.2, body_size=7.8, line_spacing=3.2)

    # Output Card (Left of 5.0)
    x_out = 4.0
    draw_header_card(ax, x_out, mid_y, p_w, p_h, "6.0 Ledger & UI Emit", [
        "• Sepolia EVM on-chain TX",
        "• SVG gauge visualization",
        "• Signed forensic receipt"
    ], "#7c2d12", "#fffbeb", "#f59e0b", header_h=5.0, title_size=9.2, body_size=7.8, line_spacing=3.2)

    # Row 3: Data Stores (D1, D2)
    bot_y = 7.0
    ds_h = 16.0
    ds_w = 42.0
    x_d1 = 4.0
    x_d2 = 55.0

    def draw_datastore(x, y, w, h, ds_id, ds_name, desc):
        draw_shadow(ax, x, y, w, h)
        p = patches.FancyBboxPatch(
            (x, y), w, h, boxstyle="square,pad=0",
            ec="#475569", fc="#f8fafc", lw=1.6, zorder=2
        )
        ax.add_patch(p)
        ax.plot([x + 10.0, x + 10.0], [y, y + h], color="#475569", lw=1.6, zorder=3)
        ax.text(x + 5.0, y + h/2, ds_id, ha='center', va='center',
                fontsize=11.0, fontweight='bold', color="#1e3a8a", family=FONT, zorder=4)
        ax.text(x + 13.0, y + h*0.65, ds_name, ha='left', va='center',
                fontsize=9.5, fontweight='bold', color="#0f172a", family=FONT, zorder=4)
        ax.text(x + 13.0, y + h*0.30, desc, ha='left', va='center',
                fontsize=8.0, fontweight='bold', color="#475569", family=FONT, zorder=4)

    draw_datastore(x_d1, bot_y, ds_w, ds_h, "D1", "Threat Intel Cache DB", "URLhaus & OpenPhish Ingested IoC Signatures")
    draw_datastore(x_d2, bot_y, ds_w, ds_h, "D2", "Redis Scan Store & Ledger", "TTL Hash Registry & Blockchain Proof Receipts")

    # Connectors
    # 1.0 -> 2.0
    r1_mid = top_y + p_h/2
    draw_arrow(ax, (x_p1 + p_w, r1_mid), (x_p2, r1_mid), color="#2563eb", lw=1.8)
    draw_pill(ax, (x_p1 + p_w + x_p2)/2, r1_mid, "Canonical URL", color="#1e40af", border="#93c5fd", bg="#ffffff", fontsize=7.2)

    # 2.0 -> 3.0
    draw_arrow(ax, (x_p2 + p_w, r1_mid), (x_p3, r1_mid), color="#059669", lw=1.8)
    draw_pill(ax, (x_p2 + p_w + x_p3)/2, r1_mid, "Public Target", color="#065f46", border="#6ee7b7", bg="#ffffff", fontsize=7.2)

    # 3.0 -> 4.0 (Downward)
    c3 = x_p3 + p_w/2
    draw_arrow(ax, (c3, top_y), (c3, mid_y + p_h), color="#7c3aed", lw=1.8)
    draw_pill(ax, c3, (top_y + mid_y + p_h)/2, "Feature Vector", color="#581c87", border="#c4b5fd", bg="#ffffff", fontsize=7.2)

    # 4.0 -> 5.0 (Leftward)
    r2_mid = mid_y + p_h/2
    draw_arrow(ax, (x_p4, r2_mid), (x_p5 + p_w, r2_mid), color="#059669", lw=1.8)
    draw_pill(ax, (x_p4 + x_p5 + p_w)/2, r2_mid, "ML Risk Score", color="#065f46", border="#6ee7b7", bg="#ffffff", fontsize=7.2)

    # 5.0 -> 6.0 (Leftward)
    draw_arrow(ax, (x_p5, r2_mid), (x_out + p_w, r2_mid), color="#881337", lw=1.8)
    draw_pill(ax, (x_p5 + x_out + p_w)/2, r2_mid, "Verdict Record", color="#881337", border="#fda4af", bg="#ffffff", fontsize=7.2)

    # D1 -> 5.0 (Threat feeds into Verdict)
    draw_path_arrow(ax, [(x_d1 + ds_w - 6.0, bot_y + ds_h), (x_d1 + ds_w - 6.0, 28.0), (x_p5 + 6.0, 28.0), (x_p5 + 6.0, mid_y)], color="#0284c7")
    draw_pill(ax, (x_d1 + ds_w - 6.0 + x_p5 + 6.0)/2, 28.0, "Feed Match", color="#0369a1", border="#7dd3fc", bg="#ffffff", fontsize=7.2)

    # 5.0 -> D2 (Persist scan to cache)
    draw_path_arrow(ax, [(x_p5 + p_w - 6.0, mid_y), (x_p5 + p_w - 6.0, 28.0), (x_d2 + 10.0, 28.0), (x_d2 + 10.0, bot_y + ds_h)], color="#e11d48")
    draw_pill(ax, (x_p5 + p_w - 6.0 + x_d2 + 10.0)/2, 28.0, "Persist Record", color="#881337", border="#fda4af", bg="#ffffff", fontsize=7.2)

    save_diagram(fig, "Fig_5_8_DFD_Level_1.png")


# -----------------------------------------------------------------------------
# 9. Fig 6.1: Feature Extraction Pipeline Architecture
# -----------------------------------------------------------------------------
def generate_fig_6_1():
    fig, ax = setup_canvas(width=10.5, height=7.0)

    ax.text(50, 96.5, "FEATURE EXTRACTION & STATISTICAL HEURISTIC PIPELINE",
            ha='center', va='center', fontsize=13.0, fontweight='bold', color="#0f172a", family=FONT)
    ax.plot([15, 85], [93.5, 93.5], color="#cbd5e1", lw=1.2)

    # Top: Stage 1 Ingestion (Generous width)
    draw_header_card(ax, 10.0, 77.0, 80.0, 14.5, "Stage 1: Syntactic Ingestion & Normalization (RFC 3986)", [
        "• Decomposes URL into Scheme, FQDN Netloc, Path, Query Parameters, and Fragment",
        "• Canonicalizes Punycode encodings and isolates Public Suffix List (PSL) registered domain"
    ], "#1e40af", "#eff6ff", "#3b82f6", header_h=5.2, title_size=9.5, body_size=8.0, line_spacing=3.2)

    # Middle: 3 Parallel Extraction Engines (Spacious height = 35.0 units!)
    h_mid = 35.0
    y_mid = 32.0
    w_mid = 27.5
    gap_mid = 4.75
    x_m1 = 4.0
    x_m2 = x_m1 + w_mid + gap_mid  # 36.25
    x_m3 = x_m2 + w_mid + gap_mid  # 68.5

    draw_header_card(ax, x_m1, y_mid, w_mid, h_mid, "Structural & Entropy", [
        "• Shannon Entropy H(s) on Host",
        "• Shannon Entropy H(s) on Path",
        "• Digit-to-Letter Ratio",
        "• Special Symbol Frequency",
        "• Subdomain Depth Metric",
        "• Path Segment Count & Length",
        "• Total URL Character Length"
    ], "#581c87", "#faf5ff", "#8b5cf6", header_h=5.0, title_size=9.0, body_size=7.6, line_spacing=3.4)

    draw_header_card(ax, x_m2, y_mid, w_mid, h_mid, "Brand Spoof & Homoglyphs", [
        "• Levenshtein Distance to 40+ Brands",
        "• Brand in Foreign Subdomain",
        "• Unicode Homoglyph Confusable Map",
        "• Punycode Obfuscation Filter",
        "• DGA Consonant-Run Ratio",
        "• Vowel-to-Consonant Anomaly",
        "• Known URL Shortener Detection"
    ], "#065f46", "#ecfdf5", "#10b981", header_h=5.0, title_size=9.0, body_size=7.6, line_spacing=3.4)

    draw_header_card(ax, x_m3, y_mid, w_mid, h_mid, "Enterprise SSO Whitelist", [
        "• Verified Domain Whitelist Guard",
        "• Google, Microsoft, AWS, Okta SSO",
        "• Legitimate OAuth2 Redirect Filter",
        "• Active False Positive Suppression",
        "• Zero-Penalty for Trusted Identities",
        "• Preserves 0% SSO False Alarm Rate",
        "• Emits Clean Authorization Signal"
    ], "#7c2d12", "#fffbeb", "#f59e0b", header_h=5.0, title_size=9.0, body_size=7.6, line_spacing=3.4)

    # Bottom: Stage 3 Scoring & Output
    draw_header_card(ax, 10.0, 6.0, 80.0, 16.5, "Stage 3: Calibrated Logistic Scoring & Explainability Engine", [
        "• Dot Product Vector Computation:  z = -3.80 + Sum(w_i * f_i)  |  Sigmoid Probability:  P = 1 / (1 + e^-z)",
        "• Deterministic Severity Categorization:  SAFE (P < 0.30)  •  ELEVATED (0.30 <= P <= 0.65)  •  MALICIOUS (P > 0.65)",
        "• Emits Fine-Grained Factor Attribution Tags and SHA-256 Forensic Evidence Vector"
    ], "#881337", "#fff1f2", "#f43f5e", header_h=5.2, title_size=9.5, body_size=8.0, line_spacing=3.4)

    # Dispatch Bus Top -> Middle
    c_m1 = x_m1 + w_mid/2
    c_m2 = x_m2 + w_mid/2
    c_m3 = x_m3 + w_mid/2
    top_bus_y = 72.0

    ax.plot([50.0, 50.0], [77.0, top_bus_y], color="#2563eb", lw=1.8, zorder=4)
    ax.plot([c_m1, c_m3], [top_bus_y, top_bus_y], color="#2563eb", lw=1.8, zorder=4)
    for cx in [c_m1, c_m2, 50.0, c_m3]:
        ax.plot(cx, top_bus_y, marker='o', markersize=3.8, color="#2563eb", zorder=5)
    for cx in [c_m1, c_m2, c_m3]:
        draw_arrow(ax, (cx, top_bus_y), (cx, y_mid + h_mid), color="#2563eb", lw=1.8)
    draw_pill(ax, 50.0, (77.0 + top_bus_y)/2, "Canonical URL Tokens", color="#1e40af", border="#93c5fd", bg="#ffffff", fontsize=7.2)

    # Aggregation Bus Middle -> Bottom
    bot_bus_y = 27.0
    for cx in [c_m1, c_m2, c_m3]:
        ax.plot([cx, cx], [y_mid, bot_bus_y], color="#7c3aed", lw=1.8, zorder=4)
    ax.plot([c_m1, c_m3], [bot_bus_y, bot_bus_y], color="#7c3aed", lw=1.8, zorder=4)
    for cx in [c_m1, c_m2, 50.0, c_m3]:
        ax.plot(cx, bot_bus_y, marker='o', markersize=3.8, color="#7c3aed", zorder=5)
    draw_arrow(ax, (50.0, bot_bus_y), (50.0, 22.5), color="#7c3aed", lw=1.8)
    draw_pill(ax, 50.0, (bot_bus_y + 22.5)/2, "Feature Attributions & Weights", color="#581c87", border="#c4b5fd", bg="#ffffff", fontsize=7.2)

    save_diagram(fig, "Fig_6_1_Feature_Extraction_Pipeline.png")


# -----------------------------------------------------------------------------
# 10. Fig 6.2: Blockchain Verification Workflow
# -----------------------------------------------------------------------------
def generate_fig_6_2():
    fig, ax = setup_canvas(width=10.5, height=7.0)

    ax.text(50, 96.5, "BLOCKCHAIN-BACKED THREAT INTELLIGENCE & VERIFICATION",
            ha='center', va='center', fontsize=13.0, fontweight='bold', color="#0f172a", family=FONT)
    ax.plot([15, 85], [93.8, 93.8], color="#cbd5e1", lw=1.2)

    # 2 Rows of 3 Cards:
    # Row 1 (Anchoring): Step 1 -> Step 2 -> Step 3
    # Row 2 (Verification): Step 6 <- Step 5 <- Step 4
    card_w = 26.0
    card_h = 32.0
    gap = 8.5
    x1 = 4.0
    x2 = x1 + card_w + gap  # 38.5
    x3 = x2 + card_w + gap  # 73.0

    row1_y = 54.0
    row2_y = 10.0

    # Step 1: Verdict Generation
    draw_header_card(ax, x1, row1_y, card_w, card_h, "STEP 1: Verdict Synthesis", [
        "• URLSentinel multi-signal core",
        "• Aggregates lexical & ML scores",
        "• Calculates Bayesian risk band",
        "• Compiles forensic evidence JSON",
        "• Emits deterministic verdict"
    ], "#1e40af", "#eff6ff", "#3b82f6", header_h=5.5, title_size=9.2, body_size=7.6, line_spacing=3.4)

    # Step 2: Cryptographic Digest
    draw_header_card(ax, x2, row1_y, card_w, card_h, "STEP 2: Evidence Digest", [
        "• Canonical JSON serialization",
        "• Computes SHA-256 hash:",
        "    H = SHA256(url + verdict +",
        "    score + timestamp + evidence)",
        "• Generates root digest string",
        "• Signs payload with RFC 7515 JWS"
    ], "#581c87", "#faf5ff", "#8b5cf6", header_h=5.5, title_size=9.2, body_size=7.6, line_spacing=3.4)

    # Step 3: Smart Contract Anchor
    draw_header_card(ax, x3, row1_y, card_w, card_h, "STEP 3: Contract Anchor", [
        "• Dispatches Sepolia EVM tx",
        "• Calls ThreatRegistry.sol",
        "• registerThreat(urlHash, digest)",
        "• Anchors IoC to block header",
        "• Emits ThreatRegistered event"
    ], "#065f46", "#ecfdf5", "#10b981", header_h=5.5, title_size=9.2, body_size=7.6, line_spacing=3.4)

    # Step 4: Immutable Ledger
    draw_header_card(ax, x3, row2_y, card_w, card_h, "STEP 4: Immutable Ledger", [
        "• Permanent decentralized block",
        "• Indexed by block number & TX",
        "• Guarantees non-repudiation",
        "• Zero single point of failure",
        "• Publicly auditable state"
    ], "#7c2d12", "#fffbeb", "#f59e0b", header_h=5.5, title_size=9.2, body_size=7.6, line_spacing=3.4)

    # Step 5: Public Audit Query
    draw_header_card(ax, x2, row2_y, card_w, card_h, "STEP 5: Public Audit Query", [
        "• Client or external auditor",
        "• Queries getThreatProof(urlHash)",
        "• Fetches on-chain anchored hash",
        "• Retrieves block timestamp",
        "• Zero-trust verification"
    ], "#0f172a", "#f8fafc", "#475569", header_h=5.5, title_size=9.2, body_size=7.6, line_spacing=3.4)

    # Step 6: Proof of Non-Tampering
    draw_header_card(ax, x1, row2_y, card_w, card_h, "STEP 6: Proof of Integrity", [
        "• Recomputes SHA-256 locally",
        "• Local Digest == On-Chain Digest",
        "• 100% Cryptographic Match",
        "• Proves zero log tampering",
        "• Legally admissible forensic record"
    ], "#15803d", "#f0fdf4", "#22c55e", header_h=5.5, title_size=9.2, body_size=7.6, line_spacing=3.4)

    # Connectors with Wide 8.5-unit gaps - ZERO collision!
    # 1 -> 2
    r1_mid_y = row1_y + card_h/2
    draw_arrow(ax, (x1 + card_w, r1_mid_y), (x2, r1_mid_y), color="#2563eb", lw=1.8)
    draw_pill(ax, (x1 + card_w + x2)/2, r1_mid_y, "JSON Data", color="#1e40af", border="#93c5fd", bg="#ffffff", fontsize=7.2)

    # 2 -> 3
    draw_arrow(ax, (x2 + card_w, r1_mid_y), (x3, r1_mid_y), color="#7c3aed", lw=1.8)
    draw_pill(ax, (x2 + card_w + x3)/2, r1_mid_y, "SHA-256", color="#581c87", border="#c4b5fd", bg="#ffffff", fontsize=7.2)

    # 3 -> 4 (Downward on Right)
    c3 = x3 + card_w/2
    draw_arrow(ax, (c3, row1_y), (c3, row2_y + card_h), color="#059669", lw=1.8)
    draw_pill(ax, c3, (row1_y + row2_y + card_h)/2, "Mined On-Chain", color="#065f46", border="#6ee7b7", bg="#ffffff", fontsize=7.2)

    # 4 -> 5 (Leftward)
    r2_mid_y = row2_y + card_h/2
    draw_arrow(ax, (x3, r2_mid_y), (x2 + card_w, r2_mid_y), color="#d97706", lw=1.8)
    draw_pill(ax, (x3 + x2 + card_w)/2, r2_mid_y, "Query TX", color="#7c2d12", border="#fcd34d", bg="#ffffff", fontsize=7.2)

    # 5 -> 6 (Leftward)
    draw_arrow(ax, (x2, r2_mid_y), (x1 + card_w, r2_mid_y), color="#334155", lw=1.8)
    draw_pill(ax, (x2 + x1 + card_w)/2, r2_mid_y, "Compare", color="#0f172a", border="#cbd5e1", bg="#ffffff", fontsize=7.2)

    # Bottom Verification Guarantee Banner
    ax.text(50.0, 4.0, "Cryptographic Guarantee: Any post-hoc database tampering invalidates equality H(local) != H(blockchain)",
            ha='center', va='center', fontsize=8.2, fontweight='bold', color="#15803d", family=FONT)

    save_diagram(fig, "Fig_6_2_Blockchain_Verification_Workflow.png")


# -----------------------------------------------------------------------------
# Main Execution
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    print("Beginning generation of all 10 publication-grade diagrams...")
    generate_fig_5_1()
    generate_fig_5_2()
    generate_fig_5_3()
    generate_fig_5_4()
    generate_fig_5_5()
    generate_fig_5_6()
    generate_fig_5_7()
    generate_fig_5_8()
    generate_fig_6_1()
    generate_fig_6_2()
    print("SUCCESS: All 10 diagrams successfully generated in diagrams folder!")
