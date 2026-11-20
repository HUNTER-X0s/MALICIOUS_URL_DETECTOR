import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from pathlib import Path

OUT_FILE = Path(r"z:\URLSentinel\URLSentinel_PPD_Report\diagrams\Fig_5_1_System_Architecture.png")

def generate_compact_architecture_diagram():
    # Width: 12.0 inches, Height: 6.4 inches (Aspect Ratio: 1.875)
    # At 300 DPI -> 3600 x 1920 px
    fig, ax = plt.subplots(figsize=(12.0, 6.4), dpi=300)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')

    fig.patch.set_facecolor('#ffffff')
    ax.set_facecolor('#ffffff')

    FONT_FAMILY = 'DejaVu Sans'

    def draw_drop_shadow(x, y, w, h, radius=1.6):
        shadow = patches.FancyBboxPatch(
            (x + 0.35, y - 0.45), w, h,
            boxstyle=f"round,pad=0.12,rounding_size={radius}",
            fc="#e2e8f0", ec="none", alpha=0.6, zorder=1
        )
        ax.add_patch(shadow)

    def draw_card(x, y, w, h, title, subtitle_lines, title_color, bg_color, border_color,
                  radius=1.6, lw=1.3, badge=""):
        draw_drop_shadow(x, y, w, h, radius)
        box = patches.FancyBboxPatch(
            (x, y), w, h,
            boxstyle=f"round,pad=0.12,rounding_size={radius}",
            ec=border_color, fc=bg_color, lw=lw, zorder=2
        )
        ax.add_patch(box)

        # Title
        if subtitle_lines:
            # Position title comfortably in top part of card
            ty = y + h - 3.2
            ax.text(x + w/2, ty, title, ha='center', va='center',
                    fontsize=9.2, fontweight='bold', color=title_color, zorder=3,
                    family=FONT_FAMILY)
            
            # Subtle accent divider
            ax.plot([x + 3.0, x + w - 3.0], [ty - 1.7, ty - 1.7], color=border_color, lw=0.6, alpha=0.5, zorder=3)

            # Subtitle lines
            start_sy = ty - 3.8
            line_spacing = 2.4
            for idx, s in enumerate(subtitle_lines):
                sy = start_sy - idx * line_spacing
                ax.text(x + w/2, sy, s, ha='center', va='center',
                        fontsize=7.4, color="#334155", zorder=3,
                        family=FONT_FAMILY)
        else:
            ax.text(x + w/2, y + h/2, title, ha='center', va='center',
                    fontsize=9.2, fontweight='bold', color=title_color, zorder=3,
                    family=FONT_FAMILY)

    def draw_pill_label(x, y, text, color="#0f172a", border_color="#94a3b8", bg_color="#ffffff", fontsize=6.8):
        ax.text(x, y, text, ha='center', va='center', fontsize=fontsize, fontweight='bold',
                color=color, family=FONT_FAMILY,
                bbox=dict(boxstyle="round,pad=0.22,rounding_size=0.8", fc=bg_color, ec=border_color, lw=0.8, alpha=0.98),
                zorder=7)

    # -------------------------------------------------------------------------
    # MAIN HEADER & TITLE (Single clean prominent line)
    # -------------------------------------------------------------------------
    ax.text(50, 96.5, "URLSENTINEL OVERALL SYSTEM ARCHITECTURE",
            ha='center', va='center', fontsize=12.5, fontweight='bold',
            color="#0f172a", family=FONT_FAMILY, zorder=5)

    # -------------------------------------------------------------------------
    # TIER 1: CLIENT & INGESTION TIER (3 Boxes, Blue Palette)
    # -------------------------------------------------------------------------
    t1_y = 78.5
    t1_h = 13.0
    t1_w = 27.5
    gap1 = (92.0 - 3 * t1_w) / 2  # 4.75

    x1_1 = 4.0
    x1_2 = x1_1 + t1_w + gap1  # 36.25
    x1_3 = x1_2 + t1_w + gap1  # 68.5

    c1_1 = x1_1 + t1_w / 2  # 17.75
    c1_2 = x1_2 + t1_w / 2  # 50.0
    c1_3 = x1_3 + t1_w / 2  # 82.25

    draw_card(x1_1, t1_y, t1_w, t1_h, "Web Dashboard",
              ["Next.js 14, Tailwind CSS, SVG Telemetry",
               "Real-Time Inspection & Risk Analysis UI"],
              "#1e3a8a", "#eff6ff", "#3b82f6")

    draw_card(x1_2, t1_y, t1_w, t1_h, "Browser Extension",
              ["Chromium MV3, WebNav Interceptor",
               "Pre-DOM Zero-Hour Blockade Engine"],
              "#1e3a8a", "#eff6ff", "#3b82f6")

    draw_card(x1_3, t1_y, t1_w, t1_h, "Enterprise REST API",
              ["FastAPI Gateway, Pydantic v2 Models",
               "Sub-50ms Synchronous Risk Evaluation"],
              "#1e3a8a", "#eff6ff", "#3b82f6")

    # -------------------------------------------------------------------------
    # TIER 2: SECURITY BOUNDARY & INGESTION PERIMETER (Emerald Green)
    # -------------------------------------------------------------------------
    t2_y = 57.5
    t2_h = 10.5
    t2_w = 92.0
    t2_x = 4.0

    draw_card(t2_x, t2_y, t2_w, t2_h, "Security Boundary & Ingestion Perimeter",
              ["Nginx Reverse Proxy  •  Token Authentication  •  Rate Limiting (10 req/s)  •  SSRF Defence (RFC 1918 Dropped)"],
              "#065f46", "#ecfdf5", "#10b981")

    # Connectors Tier 1 -> Tier 2
    for cx, lbl in [(c1_1, "HTTPS"), (c1_2, "REST / WebNav"), (c1_3, "API Scan")]:
        ax.annotate("", xy=(cx, t2_y + t2_h), xytext=(cx, t1_y),
                    arrowprops=dict(arrowstyle="-|>", color="#2563eb", lw=1.3, mutation_scale=10, shrinkA=0, shrinkB=0),
                    zorder=5)
        draw_pill_label(cx, (t1_y + t2_y + t2_h)/2, lbl, color="#1e40af", border_color="#93c5fd", fontsize=6.6)

    # -------------------------------------------------------------------------
    # TIER 3: PARALLEL DETECTION ENGINES (4 Boxes, Purple Palette)
    # -------------------------------------------------------------------------
    t3_y = 35.5
    t3_h = 12.5
    t3_w = 21.0
    gap3 = (92.0 - 4 * t3_w) / 3  # (92 - 84) / 3 = 2.666

    x3_1 = 4.0
    x3_2 = x3_1 + t3_w + gap3
    x3_3 = x3_2 + t3_w + gap3
    x3_4 = x3_3 + t3_w + gap3

    c3_1 = x3_1 + t3_w / 2
    c3_2 = x3_2 + t3_w / 2
    c3_3 = x3_3 + t3_w / 2
    c3_4 = x3_4 + t3_w / 2

    draw_card(x3_1, t3_y, t3_w, t3_h, "URL Normalizer",
              ["RFC 3986, PSL Cache", "Punycode Decoder (0.12ms)"],
              "#4c1d95", "#f5f3ff", "#8b5cf6")

    draw_card(x3_2, t3_y, t3_w, t3_h, "Lexical & Entropy",
              ["Shannon Entropy H(S)", "Token Length, Special Chars"],
              "#4c1d95", "#f5f3ff", "#8b5cf6")

    draw_card(x3_3, t3_y, t3_w, t3_h, "ML Classifier v2.1",
              ["Random Forest Ensemble", "DGA Consonants (0.28ms)"],
              "#4c1d95", "#f5f3ff", "#8b5cf6")

    draw_card(x3_4, t3_y, t3_w, t3_h, "Threat Intelligence",
              ["URLhaus, OpenPhish", "PhishTank Ingestion (0.09ms)"],
              "#4c1d95", "#f5f3ff", "#8b5cf6")

    # Connectors Tier 2 -> Tier 3 via Canonical URL Dispatch bus
    d_bus_y = 51.5
    d_bus_color = "#059669"
    d_bus_lw = 1.3

    # Trunk from perimeter center down to bus
    ax.plot([50.0, 50.0], [t2_y, d_bus_y], color=d_bus_color, lw=d_bus_lw, zorder=4)
    # Horizontal bus
    ax.plot([c3_1, c3_4], [d_bus_y, d_bus_y], color=d_bus_color, lw=d_bus_lw, zorder=4)
    for cx in [c3_1, c3_2, 50.0, c3_3, c3_4]:
        ax.plot(cx, d_bus_y, marker='o', markersize=3.2, color=d_bus_color, zorder=5)

    # Drops into Tier 3 boxes
    for cx in [c3_1, c3_2, c3_3, c3_4]:
        ax.annotate("", xy=(cx, t3_y + t3_h), xytext=(cx, d_bus_y),
                    arrowprops=dict(arrowstyle="-|>", color=d_bus_color, lw=1.3, mutation_scale=9, shrinkA=0, shrinkB=0),
                    zorder=5)

    draw_pill_label(50.0, (t2_y + d_bus_y)/2, "Canonical URL Dispatch",
                    color="#065f46", border_color="#6ee7b7", bg_color="#ffffff", fontsize=6.6)

    # -------------------------------------------------------------------------
    # TIER 4: DECISION ENGINE & EVIDENCE PROVENANCE (Rose & Amber Palette)
    # -------------------------------------------------------------------------
    t4_y = 8.0
    t4_h = 13.5
    t4_w1 = 43.5
    t4_w2 = 43.5
    gap4 = 92.0 - (t4_w1 + t4_w2)  # 5.0

    x4_1 = 4.0
    x4_2 = x4_1 + t4_w1 + gap4  # 52.5

    c4_1 = x4_1 + t4_w1 / 2  # 25.75
    c4_2 = x4_2 + t4_w2 / 2  # 74.25

    draw_card(x4_1, t4_y, t4_w1, t4_h, "Multi-Signal Risk Engine",
              ["Bayesian Signal Aggregator (0–100)",
               "Calibrated Verdict: SAFE  •  ELEVATED  •  MALICIOUS"],
              "#881337", "#fff1f2", "#f43f5e")

    draw_card(x4_2, t4_y, t4_w2, t4_h, "Blockchain & Cryptographic Signer",
              ["Canonical SHA-256 Forensic Evidence Digest Generator",
               "EVM ThreatRegistry.sol Anchoring for Permanent Auditability"],
              "#7c2d12", "#fffbeb", "#f59e0b")

    # Aggregation Bus: Tier 3 -> Multi-Signal Risk Engine
    a_bus_y = 28.0
    a_bus_color = "#7c3aed"
    a_bus_lw = 1.3

    # Drops from Tier 3 boxes
    for cx in [c3_1, c3_2, c3_3, c3_4]:
        ax.plot([cx, cx], [t3_y, a_bus_y], color=a_bus_color, lw=a_bus_lw, zorder=4)

    # Bus line
    ax.plot([c3_1, c3_4], [a_bus_y, a_bus_y], color=a_bus_color, lw=a_bus_lw, zorder=4)
    for cx in [c3_1, c3_2, c4_1, c3_3, c3_4]:
        ax.plot(cx, a_bus_y, marker='o', markersize=3.2, color=a_bus_color, zorder=5)

    # Drop into Risk Engine
    ax.annotate("", xy=(c4_1, t4_y + t4_h), xytext=(c4_1, a_bus_y),
                arrowprops=dict(arrowstyle="-|>", color=a_bus_color, lw=1.5, mutation_scale=10, shrinkA=0, shrinkB=0),
                zorder=5)

    draw_pill_label(c4_1, (a_bus_y + t4_y + t4_h)/2, "Aggregated Threat Telemetry",
                    color="#581c87", border_color="#c4b5fd", bg_color="#ffffff", fontsize=6.6)

    # Horizontal Connector: Risk Engine -> Blockchain Signer
    right_edge_t4_1 = x4_1 + t4_w1
    left_edge_t4_2 = x4_2
    mid_y_t4 = t4_y + t4_h / 2

    ax.annotate("", xy=(left_edge_t4_2, mid_y_t4), xytext=(right_edge_t4_1, mid_y_t4),
                arrowprops=dict(arrowstyle="-|>", color="#e11d48", lw=1.4, mutation_scale=10, shrinkA=0, shrinkB=0),
                zorder=5)

    draw_pill_label((right_edge_t4_1 + left_edge_t4_2)/2, mid_y_t4, "Evidence\nHash",
                    color="#881337", border_color="#fda4af", bg_color="#ffffff", fontsize=6.5)

    # Save
    plt.subplots_adjust(left=0.01, right=0.99, top=0.99, bottom=0.01)
    plt.savefig(OUT_FILE, dpi=300, bbox_inches='tight', pad_inches=0.1)
    plt.close()
    print(f"Generated compact Fig 5.1 at {OUT_FILE}")

if __name__ == '__main__':
    generate_compact_architecture_diagram()
