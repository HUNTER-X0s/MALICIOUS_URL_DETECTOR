"""
generate_clean_fig_5_1.py
=========================
Generates a publication-grade, ultra-clean System Architecture Diagram (Fig 5.1).
Features:
  - Clean orthogonal and vertical arrows with zero criss-crossing or awkward slants
  - Subtle drop shadows for depth and visual elegance
  - Professional typography with balanced margins and padding
  - Distinct tier color palettes with crisp contrast
  - Elegant signal aggregation bus connecting pipeline engines to Risk Engine
  - Symmetrical spacing across all tiers
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from pathlib import Path

DIAG_DIR = Path(r"z:\URLSentinel\URLSentinel_PPD_Report\diagrams")
OUT_FILE = DIAG_DIR / "Fig_5_1_System_Architecture.png"

def create_diagram():
    # Canvas settings: 11 x 7.2 inches at 300 DPI for razor-sharp clarity
    fig, ax = plt.subplots(figsize=(11.0, 7.2), dpi=300)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')

    # Background canvas tint (pure white)
    fig.patch.set_facecolor('#ffffff')
    ax.set_facecolor('#ffffff')

    # Helper: draw drop shadow
    def draw_shadow(x, y, w, h, radius=1.8):
        shadow = patches.FancyBboxPatch(
            (x + 0.35, y - 0.45), w, h,
            boxstyle=f"round,pad=0.2,rounding_size={radius}",
            fc="#cbd5e1", ec="none", alpha=0.45, zorder=1
        )
        ax.add_patch(shadow)

    # Helper: draw styled rounded box with header and subtitle
    def draw_card(x, y, w, h, title, subtitle_lines, title_color, bg_color, border_color, radius=1.8, lw=1.5):
        draw_shadow(x, y, w, h, radius)
        box = patches.FancyBboxPatch(
            (x, y), w, h,
            boxstyle=f"round,pad=0.2,rounding_size={radius}",
            ec=border_color, fc=bg_color, lw=lw, zorder=2
        )
        ax.add_patch(box)

        # Title
        if subtitle_lines:
            ty = y + h - 3.8
            ax.text(x + w/2, ty, title, ha='center', va='center',
                    fontsize=9.2, fontweight='bold', color=title_color, zorder=3,
                    family='DejaVu Sans')
            # Subtitle lines
            n_sub = len(subtitle_lines)
            start_sy = ty - 2.8
            line_spacing = 2.4
            for idx, s in enumerate(subtitle_lines):
                sy = start_sy - idx * line_spacing
                ax.text(x + w/2, sy, s, ha='center', va='center',
                        fontsize=7.3, color="#334155", zorder=3,
                        family='DejaVu Sans')
        else:
            ax.text(x + w/2, y + h/2, title, ha='center', va='center',
                    fontsize=9.5, fontweight='bold', color=title_color, zorder=3,
                    family='DejaVu Sans')

    # Helper: draw clean orthogonal line / arrow
    def draw_arrow_straight(x1, y1, x2, y2, label="", color="#475569", lw=1.5, label_y_offset=0.0):
        ax.annotate(
            "", xy=(x2, y2), xytext=(x1, y1),
            arrowprops=dict(arrowstyle="-|>", color=color, lw=lw, mutation_scale=12,
                            shrinkA=0, shrinkB=0),
            zorder=5
        )
        if label:
            mx, my = (x1 + x2)/2, (y1 + y2)/2 + label_y_offset
            ax.text(mx, my, label, ha='center', va='center', fontsize=6.8, fontweight='semibold',
                    color="#1e293b", family='DejaVu Sans',
                    bbox=dict(boxstyle="round,pad=0.25", fc="#ffffff", ec="#cbd5e1", lw=0.8, alpha=0.95),
                    zorder=6)

    # -------------------------------------------------------------------------
    # MAIN HEADER
    # -------------------------------------------------------------------------
    ax.text(50, 96.5, "URLSENTINEL OVERALL SYSTEM ARCHITECTURE",
            ha='center', va='center', fontsize=12.5, fontweight='bold',
            color="#0f172a", family='DejaVu Sans', zorder=5)
    
    # Subtle decorative rule under title
    ax.plot([25, 75], [94.5, 94.5], color="#94a3b8", lw=0.8, zorder=4)

    # -------------------------------------------------------------------------
    # TIER 1: CLIENT PRESENTATION & INGESTION (Blue Palette)
    # -------------------------------------------------------------------------
    t1_y = 78.5
    t1_h = 13.0
    t1_w = 27.0
    gap1 = (92.0 - 3 * t1_w) / 2  # (92 - 81) / 2 = 5.5

    x1_1 = 4.0
    x1_2 = x1_1 + t1_w + gap1  # 4 + 27 + 5.5 = 36.5
    x1_3 = x1_2 + t1_w + gap1  # 36.5 + 27 + 5.5 = 69.0

    c1_1 = x1_1 + t1_w / 2  # 17.5
    c1_2 = x1_2 + t1_w / 2  # 50.0
    c1_3 = x1_3 + t1_w / 2  # 82.5

    draw_card(x1_1, t1_y, t1_w, t1_h, "Web Dashboard",
              ["Next.js 14 Web Application", "Tailwind CSS  |  SVG Telemetry"],
              "#1e40af", "#eff6ff", "#3b82f6")

    draw_card(x1_2, t1_y, t1_w, t1_h, "Browser Extension",
              ["Chromium Manifest V3", "WebNavigation Endpoint Interceptor"],
              "#1e40af", "#eff6ff", "#3b82f6")

    draw_card(x1_3, t1_y, t1_w, t1_h, "Enterprise REST API",
              ["FastAPI Analytical Gateway", "Pydantic v2 Contract Validation"],
              "#1e40af", "#eff6ff", "#3b82f6")

    # -------------------------------------------------------------------------
    # TIER 2: SECURITY BOUNDARY & INGESTION PERIMETER (Emerald / Green Palette)
    # -------------------------------------------------------------------------
    t2_y = 57.5
    t2_h = 11.5
    t2_x = 4.0
    t2_w = 92.0

    draw_card(t2_x, t2_y, t2_w, t2_h, "Security Boundary & Ingestion Perimeter",
              ["Nginx Reverse Proxy  •  Bearer Token Authentication  •  Token Bucket Rate Limiting (10 req/s)",
               "Zero-Trust SSRF Defense Layer: Automated RFC 1918 / Loopback Egress Dropping"],
              "#065f46", "#ecfdf5", "#10b981")

    # Arrows Tier 1 -> Tier 2 (Perfect Verticals!)
    draw_arrow_straight(c1_1, t1_y, c1_1, t2_y + t2_h, label="HTTPS (TLS 1.3)", color="#2563eb")
    draw_arrow_straight(c1_2, t1_y, c1_2, t2_y + t2_h, label="REST / WebNav", color="#2563eb")
    draw_arrow_straight(c1_3, t1_y, c1_3, t2_y + t2_h, label="API Scan (JSON)", color="#2563eb")

    # -------------------------------------------------------------------------
    # TIER 3: MULTI-STAGE ANALYTICAL PIPELINE (Purple / Violet Palette)
    # -------------------------------------------------------------------------
    t3_y = 35.0
    t3_h = 13.5
    t3_w = 21.0
    gap3 = (92.0 - 4 * t3_w) / 3  # (92 - 84) / 3 = 2.667

    x3_1 = 4.0
    x3_2 = x3_1 + t3_w + gap3  # 4 + 21 + 2.667 = 27.667
    x3_3 = x3_2 + t3_w + gap3  # 27.667 + 21 + 2.667 = 51.333
    x3_4 = x3_3 + t3_w + gap3  # 51.333 + 21 + 2.667 = 75.0

    c3_1 = x3_1 + t3_w / 2  # 14.5
    c3_2 = x3_2 + t3_w / 2  # 38.167
    c3_3 = x3_3 + t3_w / 2  # 61.833
    c3_4 = x3_4 + t3_w / 2  # 85.5

    draw_card(x3_1, t3_y, t3_w, t3_h, "URL Normalizer",
              ["RFC 3986 Syntax Canonicalizer", "PSL Cache  •  Punycode Decoder", "Execution Latency: 0.12 ms"],
              "#581c87", "#faf5ff", "#8b5cf6")

    draw_card(x3_2, t3_y, t3_w, t3_h, "Lexical & Entropy",
              ["Shannon Entropy H(S) Analysis", "Token Length  •  Special Chars", "Execution Latency: 0.85 ms"],
              "#581c87", "#faf5ff", "#8b5cf6")

    draw_card(x3_3, t3_y, t3_w, t3_h, "ML Classifier v2.1",
              ["Calibrated Random Forest", "DGA Consonant Clustering", "Execution Latency: 0.28 ms"],
              "#581c87", "#faf5ff", "#8b5cf6")

    draw_card(x3_4, t3_y, t3_w, t3_h, "Threat Intelligence",
              ["URLhaus, OpenPhish Feeds", "PhishTank Real-time Ingestion", "Execution Latency: 0.09 ms"],
              "#581c87", "#faf5ff", "#8b5cf6")

    # Arrows Tier 2 -> Tier 3 (Clean Verticals!)
    draw_arrow_straight(c3_1, t2_y, c3_1, t3_y + t3_h, color="#059669")
    draw_arrow_straight(c3_2, t2_y, c3_2, t3_y + t3_h, color="#059669")
    draw_arrow_straight(c3_3, t2_y, c3_3, t3_y + t3_h, color="#059669")
    draw_arrow_straight(c3_4, t2_y, c3_4, t3_y + t3_h, color="#059669")

    # Tier 2 Dispatcher Label
    ax.text(50, (t2_y + t3_y + t3_h)/2, "Parallel Analytical Dispatch (Normalized Candidate URL)",
            ha='center', va='center', fontsize=6.8, fontweight='semibold',
            color="#065f46", family='DejaVu Sans',
            bbox=dict(boxstyle="round,pad=0.25", fc="#ffffff", ec="#10b981", lw=0.8, alpha=0.95),
            zorder=6)

    # -------------------------------------------------------------------------
    # TIER 4: SYNTHESIS & PROVENANCE (Rose & Amber Palette)
    # -------------------------------------------------------------------------
    t4_y = 9.5
    t4_h = 13.5
    t4_w1 = 44.0
    t4_w2 = 42.0
    gap4 = 92.0 - (t4_w1 + t4_w2)  # 92 - 86 = 6.0

    x4_1 = 4.0
    x4_2 = x4_1 + t4_w1 + gap4  # 4 + 44 + 6 = 54.0

    c4_1 = x4_1 + t4_w1 / 2  # 26.0
    c4_2 = x4_2 + t4_w2 / 2  # 75.0

    draw_card(x4_1, t4_y, t4_w1, t4_h, "Multi-Signal Risk Engine",
              ["Bayesian Threat Synthesis & Dynamic Weighting (0–100)",
               "Deterministic Verdicts: SAFE  |  ELEVATED  |  MALICIOUS",
               "Human-Actionable Explainability & Heuristic Factor Tags"],
              "#881337", "#fff1f2", "#f43f5e")

    draw_card(x4_2, t4_y, t4_w2, t4_h, "Blockchain & Cryptographic Signer",
              ["Canonical SHA-256 Forensic Evidence Digest Generator",
               "Sepolia EVM Smart Contract: ThreatRegistry.sol",
               "Immutable Non-Repudiation Audit Ledger"],
              "#7c2d12", "#fffbeb", "#f59e0b")

    # -------------------------------------------------------------------------
    # ELEGANT CONVERGENCE BUS: Tier 3 -> Multi-Signal Risk Engine
    # -------------------------------------------------------------------------
    # Bus line at y = 28.5
    bus_y = 28.5
    bus_color = "#7c3aed"
    bus_lw = 1.6

    # 4 clean vertical drops from Tier 3 boxes to the bus
    ax.plot([c3_1, c3_1], [t3_y, bus_y], color=bus_color, lw=bus_lw, zorder=4)
    ax.plot([c3_2, c3_2], [t3_y, bus_y], color=bus_color, lw=bus_lw, zorder=4)
    ax.plot([c3_3, c3_3], [t3_y, bus_y], color=bus_color, lw=bus_lw, zorder=4)
    ax.plot([c3_4, c3_4], [t3_y, bus_y], color=bus_color, lw=bus_lw, zorder=4)

    # Horizontal bus bar spanning from c3_1 to c3_4
    ax.plot([c3_1, c3_4], [bus_y, bus_y], color=bus_color, lw=bus_lw, zorder=4)

    # Small circular nodes at intersections on the bus
    for cx in [c3_1, c3_2, c3_3, c3_4]:
        ax.plot(cx, bus_y, marker='o', markersize=3.8, color=bus_color, zorder=5)

    # Single clean, prominent arrow dropping from bus into Multi-Signal Risk Engine center
    draw_arrow_straight(c4_1, bus_y, c4_1, t4_y + t4_h,
                        label="Aggregated Threat Telemetry & Feature Vectors",
                        color=bus_color, lw=1.8)

    # -------------------------------------------------------------------------
    # HORIZONTAL ARROW: Risk Engine -> Blockchain Signer
    # -------------------------------------------------------------------------
    right_edge_t4_1 = x4_1 + t4_w1  # 48.0
    left_edge_t4_2 = x4_2           # 54.0
    mid_y_t4 = t4_y + t4_h / 2      # 9.5 + 6.75 = 16.25

    draw_arrow_straight(right_edge_t4_1, mid_y_t4, left_edge_t4_2, mid_y_t4,
                        label="Evidence\nDigest", color="#e11d48", lw=1.6)

    # -------------------------------------------------------------------------
    # SAVE FIGURE
    # -------------------------------------------------------------------------
    plt.subplots_adjust(left=0.01, right=0.99, top=0.99, bottom=0.01)
    plt.savefig(OUT_FILE, dpi=300, bbox_inches='tight', pad_inches=0.15)
    plt.close()
    print(f"Clean Fig 5.1 successfully generated and placed at: {OUT_FILE}")

if __name__ == "__main__":
    create_diagram()
