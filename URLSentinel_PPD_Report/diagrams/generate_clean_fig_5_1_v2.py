"""
generate_clean_fig_5_1_v2.py
============================
Masterpiece Generator for Fig 5.1: Overall System Architecture Diagram
Designed for URLSentinel B.Tech Project for Product Development Report.

Aesthetic Guidelines:
  - 100% Orthogonal line routing (strictly horizontal & vertical, zero slanted/criss-crossing lines)
  - Symmetrical grid layout with mathematical precision
  - High-contrast, modern enterprise color palette (Navy, Emerald, Royal Violet, Rose, Amber)
  - Beautiful rounded container cards with subtle drop shadows
  - Pill badges with crisp contrast for all data-flow labels
  - Bus-based distribution and aggregation architecture
  - Ultra-high resolution 300 DPI vector-sharp rendering
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from pathlib import Path

DIAG_DIR = Path(r"z:\URLSentinel\URLSentinel_PPD_Report\diagrams")
OUT_FILE = DIAG_DIR / "Fig_5_1_System_Architecture.png"

def create_system_architecture_diagram():
    # Canvas: 11.2 x 7.6 inches at 300 DPI
    fig, ax = plt.subplots(figsize=(11.2, 7.6), dpi=300)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')

    fig.patch.set_facecolor('#ffffff')
    ax.set_facecolor('#ffffff')

    FONT_FAMILY = 'DejaVu Sans'

    # -------------------------------------------------------------------------
    # DRAWING PRIMITIVES
    # -------------------------------------------------------------------------
    def draw_drop_shadow(x, y, w, h, radius=2.0):
        shadow = patches.FancyBboxPatch(
            (x + 0.35, y - 0.45), w, h,
            boxstyle=f"round,pad=0.15,rounding_size={radius}",
            fc="#cbd5e1", ec="none", alpha=0.45, zorder=1
        )
        ax.add_patch(shadow)

    def draw_card(x, y, w, h, title, subtitle_lines, title_color, bg_color, border_color,
                  radius=2.0, lw=1.5, badge_text="", badge_color=""):
        draw_drop_shadow(x, y, w, h, radius)
        box = patches.FancyBboxPatch(
            (x, y), w, h,
            boxstyle=f"round,pad=0.15,rounding_size={radius}",
            ec=border_color, fc=bg_color, lw=lw, zorder=2
        )
        ax.add_patch(box)

        # Optional top badge (e.g., Latency or Tier)
        if badge_text:
            bx = x + w - 1.2
            by = y + h - 1.2
            ax.text(bx, by, badge_text, ha='right', va='top', fontsize=6.2, fontweight='bold',
                    color=badge_color, family=FONT_FAMILY,
                    bbox=dict(boxstyle="round,pad=0.18", fc="#ffffff", ec=border_color, lw=0.8, alpha=0.95),
                    zorder=4)

        # Title
        if subtitle_lines:
            ty = y + h - 3.6
            ax.text(x + w/2, ty, title, ha='center', va='center',
                    fontsize=9.4, fontweight='bold', color=title_color, zorder=3,
                    family=FONT_FAMILY)
            
            # Subtle accent divider inside card
            ax.plot([x + 3.0, x + w - 3.0], [ty - 2.0, ty - 2.0], color=border_color, lw=0.6, alpha=0.45, zorder=3)

            # Subtitle lines
            start_sy = ty - 4.4
            line_spacing = 2.5
            for idx, s in enumerate(subtitle_lines):
                sy = start_sy - idx * line_spacing
                ax.text(x + w/2, sy, s, ha='center', va='center',
                        fontsize=7.4, color="#334155", zorder=3,
                        family=FONT_FAMILY)
        else:
            ax.text(x + w/2, y + h/2, title, ha='center', va='center',
                    fontsize=9.6, fontweight='bold', color=title_color, zorder=3,
                    family=FONT_FAMILY)

    def draw_pill_label(x, y, text, color="#0f172a", border_color="#94a3b8", bg_color="#ffffff", fontsize=7.0):
        ax.text(x, y, text, ha='center', va='center', fontsize=fontsize, fontweight='bold',
                color=color, family=FONT_FAMILY,
                bbox=dict(boxstyle="round,pad=0.28,rounding_size=1.0", fc=bg_color, ec=border_color, lw=0.9, alpha=0.98),
                zorder=7)

    # -------------------------------------------------------------------------
    # MAIN HEADER & TITLE BANNER
    # -------------------------------------------------------------------------
    ax.text(50, 96.8, "URLSENTINEL OVERALL SYSTEM ARCHITECTURE",
            ha='center', va='center', fontsize=12.8, fontweight='bold',
            color="#0f172a", family=FONT_FAMILY, zorder=5)
    
    ax.text(50, 94.6, "Layered Defense-in-Depth Pipeline  •  Real-Time Endpoint Interception  •  Cryptographic Blockchain Provenance",
            ha='center', va='center', fontsize=7.2, fontweight='medium',
            color="#64748b", family=FONT_FAMILY, zorder=5)

    # Decorative header divider
    ax.plot([15, 85], [93.2, 93.2], color="#cbd5e1", lw=1.0, zorder=4)

    # -------------------------------------------------------------------------
    # TIER 1: PRESENTATION & CLIENT LAYER (Blue Palette)
    # -------------------------------------------------------------------------
    t1_y = 77.5
    t1_h = 13.5
    t1_w = 27.0
    gap1 = (92.0 - 3 * t1_w) / 2  # (92 - 81) / 2 = 5.5

    x1_1 = 4.0
    x1_2 = x1_1 + t1_w + gap1  # 36.5
    x1_3 = x1_2 + t1_w + gap1  # 69.0

    c1_1 = x1_1 + t1_w / 2  # 17.5
    c1_2 = x1_2 + t1_w / 2  # 50.0
    c1_3 = x1_3 + t1_w / 2  # 82.5

    draw_card(x1_1, t1_y, t1_w, t1_h, "Web Dashboard",
              ["Next.js 14 Frontend Application", "Tailwind CSS  •  Live Telemetry UI", "On-Demand URL Risk Inspection"],
              "#1e40af", "#eff6ff", "#3b82f6", badge_text="WEB UI", badge_color="#1e40af")

    draw_card(x1_2, t1_y, t1_w, t1_h, "Browser Extension",
              ["Chromium Manifest V3 Service Worker", "chrome.webNavigation Interceptor", "Pre-DOM Zero-Hour Blockade"],
              "#1e40af", "#eff6ff", "#3b82f6", badge_text="EXT MV3", badge_color="#1e40af")

    draw_card(x1_3, t1_y, t1_w, t1_h, "Enterprise REST API",
              ["FastAPI Asynchronous Gateway", "Pydantic v2 Schema Enforcement", "Sub-50ms Round-Trip Response"],
              "#1e40af", "#eff6ff", "#3b82f6", badge_text="REST API", badge_color="#1e40af")

    # -------------------------------------------------------------------------
    # TIER 2: SECURITY BOUNDARY & INGESTION PERIMETER (Emerald Palette)
    # -------------------------------------------------------------------------
    t2_y = 56.5
    t2_h = 12.0
    t2_x = 4.0
    t2_w = 92.0

    draw_card(t2_x, t2_y, t2_w, t2_h, "Security Boundary & Ingestion Perimeter",
              ["Nginx Reverse Proxy  •  Bearer Token Authentication  •  Token Bucket Rate Limiting (10 req/s)",
               "Strict SSRF Defense Boundary: Automated RFC 1918 / Loopback Egress Dropping via Docker Egress Rules"],
              "#065f46", "#ecfdf5", "#10b981", badge_text="GATEWAY PERIMETER", badge_color="#065f46")

    # Clean Vertical Arrows: Tier 1 -> Tier 2
    # Arrow 1: Web Dashboard -> Ingestion
    ax.annotate("", xy=(c1_1, t2_y + t2_h), xytext=(c1_1, t1_y),
                arrowprops=dict(arrowstyle="-|>", color="#2563eb", lw=1.6, mutation_scale=12, shrinkA=0, shrinkB=0),
                zorder=5)
    draw_pill_label(c1_1, (t1_y + t2_y + t2_h)/2, "HTTPS (TLS 1.3)", color="#1e40af", border_color="#93c5fd", bg_color="#ffffff")

    # Arrow 2: Browser Extension -> Ingestion
    ax.annotate("", xy=(c1_2, t2_y + t2_h), xytext=(c1_2, t1_y),
                arrowprops=dict(arrowstyle="-|>", color="#2563eb", lw=1.6, mutation_scale=12, shrinkA=0, shrinkB=0),
                zorder=5)
    draw_pill_label(c1_2, (t1_y + t2_y + t2_h)/2, "REST / WebNav", color="#1e40af", border_color="#93c5fd", bg_color="#ffffff")

    # Arrow 3: Enterprise REST API -> Ingestion
    ax.annotate("", xy=(c1_3, t2_y + t2_h), xytext=(c1_3, t1_y),
                arrowprops=dict(arrowstyle="-|>", color="#2563eb", lw=1.6, mutation_scale=12, shrinkA=0, shrinkB=0),
                zorder=5)
    draw_pill_label(c1_3, (t1_y + t2_y + t2_h)/2, "API Scan (JSON)", color="#1e40af", border_color="#93c5fd", bg_color="#ffffff")

    # -------------------------------------------------------------------------
    # TIER 3: MULTI-STAGE ANALYTICAL PIPELINE (Purple / Violet Palette)
    # -------------------------------------------------------------------------
    t3_y = 34.0
    t3_h = 13.5
    t3_w = 21.0
    gap3 = (92.0 - 4 * t3_w) / 3  # 2.667

    x3_1 = 4.0
    x3_2 = x3_1 + t3_w + gap3  # 27.667
    x3_3 = x3_2 + t3_w + gap3  # 51.333
    x3_4 = x3_3 + t3_w + gap3  # 75.0

    c3_1 = x3_1 + t3_w / 2  # 14.5
    c3_2 = x3_2 + t3_w / 2  # 38.167
    c3_3 = x3_3 + t3_w / 2  # 61.833
    c3_4 = x3_4 + t3_w / 2  # 85.5

    draw_card(x3_1, t3_y, t3_w, t3_h, "URL Normalizer",
              ["RFC 3986 Canonicalizer", "PSL Domain Parsing", "Punycode Decoder"],
              "#581c87", "#faf5ff", "#8b5cf6", badge_text="0.12 ms", badge_color="#581c87")

    draw_card(x3_2, t3_y, t3_w, t3_h, "Lexical & Entropy",
              ["Shannon Entropy H(S)", "25+ Syntactic Features", "Token Length & Ratios"],
              "#581c87", "#faf5ff", "#8b5cf6", badge_text="0.85 ms", badge_color="#581c87")

    draw_card(x3_3, t3_y, t3_w, t3_h, "ML Classifier v2.1",
              ["Calibrated Random Forest", "DGA Consonant Clustering", "100.0% Precision SSO"],
              "#581c87", "#faf5ff", "#8b5cf6", badge_text="0.28 ms", badge_color="#581c87")

    draw_card(x3_4, t3_y, t3_w, t3_h, "Threat Intelligence",
              ["URLhaus & OpenPhish", "PhishTank Active Feeds", "Redis Cache Sync (15m)"],
              "#581c87", "#faf5ff", "#8b5cf6", badge_text="0.09 ms", badge_color="#581c87")

    # -------------------------------------------------------------------------
    # ORTHOGONAL DISPATCH BUS: Tier 2 -> Tier 3
    # -------------------------------------------------------------------------
    # Dispatch bus bar at y = 51.0
    d_bus_y = 51.0
    d_bus_color = "#059669"
    d_bus_lw = 1.6

    # 1. Main vertical dispatch trunk from Ingestion Gateway center (x=50.0) down to bus
    ax.plot([50.0, 50.0], [t2_y, d_bus_y], color=d_bus_color, lw=d_bus_lw, zorder=4)

    # 2. Horizontal dispatch bus line spanning from c3_1 (14.5) to c3_4 (85.5)
    ax.plot([c3_1, c3_4], [d_bus_y, d_bus_y], color=d_bus_color, lw=d_bus_lw, zorder=4)

    # 3. Connection nodes on dispatch bus
    for cx in [c3_1, c3_2, 50.0, c3_3, c3_4]:
        ax.plot(cx, d_bus_y, marker='o', markersize=3.6, color=d_bus_color, zorder=5)

    # 4. Vertical drop arrows from dispatch bus into the 4 analytical engines
    for cx in [c3_1, c3_2, c3_3, c3_4]:
        ax.annotate("", xy=(cx, t3_y + t3_h), xytext=(cx, d_bus_y),
                    arrowprops=dict(arrowstyle="-|>", color=d_bus_color, lw=1.5, mutation_scale=11, shrinkA=0, shrinkB=0),
                    zorder=5)

    # Label on dispatch trunk
    draw_pill_label(50.0, (t2_y + d_bus_y)/2, "Parallel Dispatch: Canonical URL",
                    color="#065f46", border_color="#6ee7b7", bg_color="#ffffff", fontsize=6.8)

    # -------------------------------------------------------------------------
    # TIER 4: DECISION ENGINE & EVIDENCE PROVENANCE (Rose & Amber Palette)
    # -------------------------------------------------------------------------
    t4_y = 9.0
    t4_h = 14.0
    t4_w1 = 44.0
    t4_w2 = 42.0
    gap4 = 92.0 - (t4_w1 + t4_w2)  # 6.0

    x4_1 = 4.0
    x4_2 = x4_1 + t4_w1 + gap4  # 54.0

    c4_1 = x4_1 + t4_w1 / 2  # 26.0
    c4_2 = x4_2 + t4_w2 / 2  # 75.0

    draw_card(x4_1, t4_y, t4_w1, t4_h, "Multi-Signal Risk Engine",
              ["Bayesian Threat Synthesis & Dynamic Signal Weighting (0–100)",
               "Deterministic Verdicts: SAFE  •  ELEVATED  •  MALICIOUS",
               "Human-Actionable Explainability & Heuristic Factor Tags"],
              "#881337", "#fff1f2", "#f43f5e", badge_text="DECISION CORE", badge_color="#881337")

    draw_card(x4_2, t4_y, t4_w2, t4_h, "Blockchain & Cryptographic Signer",
              ["Canonical SHA-256 Forensic Evidence Digest Generator",
               "Sepolia EVM Smart Contract: ThreatRegistry.sol Anchoring",
               "Immutable Audit Ledger with Non-Repudiation Receipts"],
              "#7c2d12", "#fffbeb", "#f59e0b", badge_text="IMMUTABLE LEDGER", badge_color="#7c2d12")

    # -------------------------------------------------------------------------
    # ELEGANT CONVERGENCE AGGREGATION BUS: Tier 3 -> Multi-Signal Risk Engine
    # -------------------------------------------------------------------------
    # Aggregation bus bar at y = 28.5
    a_bus_y = 28.5
    a_bus_color = "#7c3aed"
    a_bus_lw = 1.6

    # 1. Four clean vertical drops from Tier 3 boxes down to aggregation bus
    ax.plot([c3_1, c3_1], [t3_y, a_bus_y], color=a_bus_color, lw=a_bus_lw, zorder=4)
    ax.plot([c3_2, c3_2], [t3_y, a_bus_y], color=a_bus_color, lw=a_bus_lw, zorder=4)
    ax.plot([c3_3, c3_3], [t3_y, a_bus_y], color=a_bus_color, lw=a_bus_lw, zorder=4)
    ax.plot([c3_4, c3_4], [t3_y, a_bus_y], color=a_bus_color, lw=a_bus_lw, zorder=4)

    # 2. Horizontal aggregation bus line spanning from c3_1 (14.5) to c3_4 (85.5)
    ax.plot([c3_1, c3_4], [a_bus_y, a_bus_y], color=a_bus_color, lw=a_bus_lw, zorder=4)

    # 3. Connection nodes on aggregation bus
    for cx in [c3_1, c3_2, c4_1, c3_3, c3_4]:
        ax.plot(cx, a_bus_y, marker='o', markersize=3.6, color=a_bus_color, zorder=5)

    # 4. Single prominent convergence arrow dropping from bus directly into Risk Engine center (x=26.0)
    ax.annotate("", xy=(c4_1, t4_y + t4_h), xytext=(c4_1, a_bus_y),
                arrowprops=dict(arrowstyle="-|>", color=a_bus_color, lw=1.8, mutation_scale=12, shrinkA=0, shrinkB=0),
                zorder=5)

    draw_pill_label(c4_1, (a_bus_y + t4_y + t4_h)/2, "Aggregated Threat Telemetry & Feature Vectors",
                    color="#581c87", border_color="#c4b5fd", bg_color="#ffffff", fontsize=6.8)

    # -------------------------------------------------------------------------
    # HORIZONTAL CONNECTION: Multi-Signal Risk Engine -> Blockchain Signer
    # -------------------------------------------------------------------------
    right_edge_t4_1 = x4_1 + t4_w1  # 48.0
    left_edge_t4_2 = x4_2           # 54.0
    mid_y_t4 = t4_y + t4_h / 2      # 16.0

    ax.annotate("", xy=(left_edge_t4_2, mid_y_t4), xytext=(right_edge_t4_1, mid_y_t4),
                arrowprops=dict(arrowstyle="-|>", color="#e11d48", lw=1.6, mutation_scale=12, shrinkA=0, shrinkB=0),
                zorder=5)

    draw_pill_label((right_edge_t4_1 + left_edge_t4_2)/2, mid_y_t4, "Evidence Digest\n(SHA-256)",
                    color="#881337", border_color="#fda4af", bg_color="#ffffff", fontsize=6.5)

    # -------------------------------------------------------------------------
    # FINAL EXPORT
    # -------------------------------------------------------------------------
    plt.subplots_adjust(left=0.01, right=0.99, top=0.99, bottom=0.01)
    plt.savefig(OUT_FILE, dpi=300, bbox_inches='tight', pad_inches=0.12)
    plt.close()
    print(f"SUCCESS: Publication-grade Fig 5.1 created at: {OUT_FILE}")

if __name__ == "__main__":
    create_system_architecture_diagram()
