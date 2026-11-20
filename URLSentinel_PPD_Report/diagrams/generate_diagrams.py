"""
URLSentinel Diagram Generator
Generates high-resolution publication-grade architecture, UML, and flow diagrams
for the B.Tech PPD Final Report, along with editable Mermaid and PlantUML sources.
"""
import os
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches

OUT_DIR = Path(r"z:\URLSentinel\URLSentinel_PPD_Report\diagrams")
SRC_DIR = Path(r"z:\URLSentinel\URLSentinel_PPD_Report\editable_diagram_sources")
OUT_DIR.mkdir(parents=True, exist_ok=True)
SRC_DIR.mkdir(parents=True, exist_ok=True)

# ---------------------------------------------------------------------------
# Helper functions for drawing professional diagrams with matplotlib
# ---------------------------------------------------------------------------

def create_canvas(width=10, height=7, dpi=300):
    fig, ax = plt.subplots(figsize=(width, height), dpi=dpi)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')
    return fig, ax

def draw_box(ax, x, y, w, h, title, subtitle="", color="#1e293b", bgcolor="#f8fafc", edge_color="#334155", radius=2):
    rect = patches.FancyBboxPatch(
        (x, y), w, h,
        boxstyle=f"round,pad=0.5,rounding_size={radius}",
        ec=edge_color, fc=bgcolor, lw=1.5, zorder=2
    )
    ax.add_patch(rect)
    
    if subtitle:
        ax.text(x + w/2, y + h*0.65, title, ha='center', va='center', fontsize=9.5, fontweight='bold', color=color, zorder=3)
        ax.text(x + w/2, y + h*0.32, subtitle, ha='center', va='center', fontsize=8, color="#475569", style='italic', zorder=3)
    else:
        ax.text(x + w/2, y + h/2, title, ha='center', va='center', fontsize=9, fontweight='bold', color=color, zorder=3)
    return rect

def draw_arrow(ax, x1, y1, x2, y2, label="", color="#475569"):
    ax.annotate(
        "", xy=(x2, y2), xytext=(x1, y1),
        arrowprops=dict(arrowstyle="-|>", color=color, lw=1.5, mutation_scale=12),
        zorder=4
    )
    if label:
        mx, my = (x1 + x2)/2, (y1 + y2)/2
        ax.text(mx, my + 1.5, label, ha='center', va='bottom', fontsize=7.5, color=color,
                bbox=dict(boxstyle="round,pad=0.2", fc="white", ec="none", alpha=0.8), zorder=5)

# ---------------------------------------------------------------------------
# 1. Fig 5.1: Overall System Architecture Diagram
# ---------------------------------------------------------------------------
def gen_fig5_1():
    fig, ax = create_canvas(11, 7.5)
    ax.text(50, 96, "URLSENTINEL: OVERALL SYSTEM ARCHITECTURE", ha='center', fontsize=14, fontweight='bold', color="#0f172a")
    
    # Layer 1: Client Layer
    ax.text(5, 87, "CLIENT / PRESENTATION LAYER", fontsize=10, fontweight='bold', color="#1e3a8a")
    draw_box(ax, 5, 75, 26, 9, "Web Dashboard", "Next.js 15, Tailwind CSS, SVG Gauge", "#1e3a8a", "#eff6ff", "#3b82f6")
    draw_box(ax, 37, 75, 26, 9, "Browser Extension", "Chromium Manifest V3, WebNav Hook", "#1e3a8a", "#eff6ff", "#3b82f6")
    draw_box(ax, 69, 75, 26, 9, "Developer REST API", "FastAPI, OpenAPI, JSON Schema", "#1e3a8a", "#eff6ff", "#3b82f6")
    
    # Layer 2: API Gateway & Security Perimeter
    draw_box(ax, 15, 59, 70, 8, "Reverse Proxy, Ingestion & Security Perimeter", "Nginx, SSL/TLS, Rate Limiter (10 r/s), SSRF Guard (RFC 1918 / Cloud IMDS Defense)", "#065f46", "#ecfdf5", "#10b981")
    
    draw_arrow(ax, 18, 75, 25, 67, "HTTPS / JSON")
    draw_arrow(ax, 50, 75, 50, 67, "REST / Auth")
    draw_arrow(ax, 82, 75, 75, 67, "API Key / Scan")
    
    # Layer 3: Multi-Layer Detection Engines
    ax.text(5, 52, "MULTI-LAYERED URL ANALYSIS ENGINES", fontsize=10, fontweight='bold', color="#4c1d95")
    draw_box(ax, 4, 38, 20, 11, "URL Normalizer", "RFC 3986, PSL Cache,\nHash Generation (3ms)", "#4c1d95", "#f5f3ff", "#8b5cf6")
    draw_box(ax, 28, 38, 20, 11, "Lexical & Homoglyph", "Shannon Entropy,\nLevenshtein Brand Proximity", "#4c1d95", "#f5f3ff", "#8b5cf6")
    draw_box(ax, 52, 38, 20, 11, "ML Classifier v2.1", "Statistical Logistic Model,\nDGA Consonants, Explanations", "#4c1d95", "#f5f3ff", "#8b5cf6")
    draw_box(ax, 76, 38, 20, 11, "Threat Intelligence", "URLhaus, OpenPhish Feeds,\n15-min APScheduler Cron", "#4c1d95", "#f5f3ff", "#8b5cf6")
    
    draw_arrow(ax, 30, 59, 14, 49)
    draw_arrow(ax, 45, 59, 38, 49)
    draw_arrow(ax, 55, 59, 62, 49)
    draw_arrow(ax, 70, 59, 86, 49)
    
    # Layer 4: Verdict Synthesis & Storage
    draw_box(ax, 8, 20, 38, 10, "Verdict Synthesis Engine", "Bayesian Signal Aggregator, Calibrated Risk (0-100),\nDetection Honesty Enforcer (Never false clean)", "#831843", "#fdf2f8", "#ec4899")
    draw_box(ax, 54, 20, 38, 10, "Cryptographic Signer & Hash Ledger", "RFC 7515 JWS Claims, SHA-256 Digest,\nOff-chain Redis + Blockchain On-chain Anchor", "#831843", "#fdf2f8", "#ec4899")
    
    draw_arrow(ax, 14, 38, 22, 30)
    draw_arrow(ax, 38, 38, 27, 30)
    draw_arrow(ax, 62, 38, 32, 30)
    draw_arrow(ax, 86, 38, 70, 30)
    draw_arrow(ax, 46, 25, 54, 25, "Digest Hash")
    
    # Layer 5: Data & Blockchain Persistence
    draw_box(ax, 12, 4, 32, 9, "Distributed Memory & Cache", "Redis 7.0 + In-Memory Fallback,\nScan Hash Cache (TTL 24h)", "#1e293b", "#f1f5f9", "#64748b")
    draw_box(ax, 56, 4, 32, 9, "Blockchain Registry", "EVM ThreatRegistry.sol,\nImmutable Audit Trail & IoC Hashes", "#1e293b", "#f1f5f9", "#64748b")
    
    draw_arrow(ax, 27, 20, 27, 13, "Store Result")
    draw_arrow(ax, 73, 20, 73, 13, "Anchor Digest")

    plt.tight_layout()
    p = OUT_DIR / "Fig_5_1_System_Architecture.png"
    plt.savefig(p, dpi=300)
    plt.close()
    print("Fig 5.1 created:", p)
    
    # Save editable Mermaid source
    with open(SRC_DIR / "Fig_5_1_System_Architecture.mmd", "w") as f:
        f.write("""graph TD
    subgraph Client Layer
        Web[Web Dashboard - Next.js 15]
        Ext[Browser Extension - Manifest V3]
        API[Public REST API - FastAPI]
    end

    subgraph Security Perimeter
        Nginx[Nginx Reverse Proxy & Rate Limiter]
        SSRF[SSRF Defense Boundary - RFC 1918 / IMDS]
    end

    subgraph Multi-Layer Detection Pipeline
        Norm[URL Normalizer - RFC 3986 / PSL Cache]
        Lex[Lexical Analyzer - Shannon Entropy]
        Homo[Homoglyph & Brand Engine - Levenshtein]
        ML[ML Classifier v2.1 - Statistical Logistic Model]
        TI[Threat Intel Ingestion - URLhaus / OpenPhish Cron]
    end

    subgraph Decision & Audit Layer
        Verdict[Verdict Engine - Multi-Signal Aggregation]
        Signer[Cryptographic Hash Digest Generator]
        Cache[Redis / Memory Cache]
        Chain[Blockchain Registry - ThreatRegistry.sol]
    end

    Web --> Nginx
    Ext --> Nginx
    API --> Nginx
    Nginx --> SSRF
    SSRF --> Norm
    Norm --> Lex
    Norm --> Homo
    Norm --> ML
    Norm --> TI
    Lex & Homo & ML & TI --> Verdict
    Verdict --> Signer
    Verdict --> Cache
    Signer --> Chain
""")

# ---------------------------------------------------------------------------
# 2. Fig 5.2: Use Case Diagram
# ---------------------------------------------------------------------------
def gen_fig5_2():
    fig, ax = create_canvas(10, 7.5)
    ax.text(50, 96, "USE CASE DIAGRAM: URLSENTINEL PLATFORM", ha='center', fontsize=13, fontweight='bold', color="#0f172a")
    
    # Actors
    ax.text(12, 78, "Actor: End User", fontsize=10.5, fontweight='bold', color="#1e40af")
    ax.text(12, 45, "Actor: Security Analyst", fontsize=10.5, fontweight='bold', color="#065f46")
    ax.text(12, 16, "Actor: Administrator", fontsize=10.5, fontweight='bold', color="#701a75")
    
    # System boundary
    rect = patches.Rectangle((30, 5), 65, 86, fill=False, ec="#334155", lw=1.5, linestyle="--")
    ax.add_patch(rect)
    ax.text(62, 88, "URLSentinel Security System Boundary", ha='center', fontsize=10, fontweight='bold', color="#334155")
    
    # Use cases
    draw_box(ax, 35, 75, 26, 7, "Submit URL for Analysis", "", "#1e293b", "#f8fafc", "#cbd5e1", radius=3.5)
    draw_box(ax, 35, 64, 26, 7, "View Risk Gauge & Verdict", "", "#1e293b", "#f8fafc", "#cbd5e1", radius=3.5)
    draw_box(ax, 35, 53, 26, 7, "Browse with Live Protection", "", "#1e293b", "#f8fafc", "#cbd5e1", radius=3.5)
    draw_box(ax, 35, 42, 26, 7, "Inspect Evidence Breakdown", "", "#1e293b", "#f8fafc", "#cbd5e1", radius=3.5)
    draw_box(ax, 66, 42, 26, 7, "Verify Blockchain Receipt", "", "#1e293b", "#f8fafc", "#cbd5e1", radius=3.5)
    draw_box(ax, 35, 31, 26, 7, "Report False Positive", "", "#1e293b", "#f8fafc", "#cbd5e1", radius=3.5)
    draw_box(ax, 66, 31, 26, 7, "Query Domain Intel API", "", "#1e293b", "#f8fafc", "#cbd5e1", radius=3.5)
    draw_box(ax, 35, 20, 26, 7, "Trigger Threat Feed Sync", "", "#1e293b", "#f8fafc", "#cbd5e1", radius=3.5)
    draw_box(ax, 66, 20, 26, 7, "Review System Telemetry", "", "#1e293b", "#f8fafc", "#cbd5e1", radius=3.5)
    draw_box(ax, 50, 9, 28, 7, "Manage API Keys & Quotas", "", "#1e293b", "#f8fafc", "#cbd5e1", radius=3.5)
    
    # Connect Actor lines
    # End user lines
    ax.plot([18, 35], [78, 78.5], color="#1e40af", lw=1.2)
    ax.plot([18, 35], [78, 67.5], color="#1e40af", lw=1.2)
    ax.plot([18, 35], [78, 56.5], color="#1e40af", lw=1.2)
    
    # Analyst lines
    ax.plot([18, 35], [45, 45.5], color="#065f46", lw=1.2)
    ax.plot([18, 66], [45, 45.5], color="#065f46", lw=1.2)
    ax.plot([18, 35], [45, 34.5], color="#065f46", lw=1.2)
    ax.plot([18, 66], [45, 34.5], color="#065f46", lw=1.2)
    
    # Admin lines
    ax.plot([18, 35], [16, 23.5], color="#701a75", lw=1.2)
    ax.plot([18, 66], [16, 23.5], color="#701a75", lw=1.2)
    ax.plot([18, 50], [16, 12.5], color="#701a75", lw=1.2)

    plt.tight_layout()
    p = OUT_DIR / "Fig_5_2_Use_Case_Diagram.png"
    plt.savefig(p, dpi=300)
    plt.close()
    print("Fig 5.2 created:", p)
    
    with open(SRC_DIR / "Fig_5_2_Use_Case_Diagram.puml", "w") as f:
        f.write("""@startuml
left to right direction
skinparam packageStyle rectangle
actor "End User" as User
actor "Security Analyst" as Analyst
actor "System Admin" as Admin

rectangle "URLSentinel Platform" {
  usecase "Submit URL for Analysis" as UC1
  usecase "View Risk Gauge & Verdict" as UC2
  usecase "Browse with Real-Time Extension" as UC3
  usecase "Inspect Evidence Ledger" as UC4
  usecase "Verify Blockchain Receipt" as UC5
  usecase "Report False Positive" as UC6
  usecase "Query Domain Intel API" as UC7
  usecase "Trigger Threat Feed Sync" as UC8
  usecase "Review System Telemetry" as UC9
  usecase "Manage API Keys & Quotas" as UC10
}

User --> UC1
User --> UC2
User --> UC3

Analyst --> UC4
Analyst --> UC5
Analyst --> UC6
Analyst --> UC7

Admin --> UC8
Admin --> UC9
Admin --> UC10
@enduml
""")

# ---------------------------------------------------------------------------
# 3. Fig 5.3: Entity Relationship Diagram (ERD)
# ---------------------------------------------------------------------------
def gen_fig5_3():
    fig, ax = create_canvas(10, 7)
    ax.text(50, 96, "ENTITY RELATIONSHIP DIAGRAM (ERD)", ha='center', fontsize=13, fontweight='bold', color="#0f172a")
    
    draw_box(ax, 5, 62, 26, 26, "SCAN_REQUEST", "PK id (UUID)\ncanonical_url (TEXT)\nurl_hash (VARCHAR 64)\nclient_ip (VARCHAR 45)\nrequested_at (TIMESTAMP)\nstatus (ENUM)", "#0f172a", "#f8fafc", "#475569")
    draw_box(ax, 40, 62, 26, 26, "VERDICT_RECORD", "PK id (UUID)\nFK scan_id (UUID)\nverdict (ENUM: SAFE/MAL)\nrisk_score (INT: 0-100)\nconfidence (ENUM)\nsummary (TEXT)\nsigned_digest (VARCHAR 64)", "#0f172a", "#f8fafc", "#475569")
    draw_box(ax, 72, 62, 24, 26, "BLOCKCHAIN_ANCHOR", "PK tx_hash (VARCHAR 66)\nFK verdict_id (UUID)\nmerkle_root (VARCHAR 64)\nblock_number (BIGINT)\nanchored_at (TIMESTAMP)\ncontract_addr (VARCHAR 42)", "#0f172a", "#f8fafc", "#475569")
    
    draw_box(ax, 5, 12, 26, 32, "EVIDENCE_SIGNAL", "PK id (UUID)\nFK verdict_id (UUID)\nlayer (ENUM: ML/DNS/LEX)\nsignal_name (VARCHAR 50)\ncontribution (ENUM)\ndescription (TEXT)\nobserved_at (TIMESTAMP)\ntechnical_metadata (JSONB)", "#0f172a", "#f8fafc", "#475569")
    draw_box(ax, 40, 12, 26, 32, "THREAT_INTEL_ENTRY", "PK id (UUID)\nindicator (TEXT)\nindicator_type (ENUM)\nsource_feed (URLHAUS/OPENPHISH)\nthreat_type (MALWARE/PHISH)\nfirst_seen (TIMESTAMP)\nlast_active (TIMESTAMP)\nis_active (BOOLEAN)", "#0f172a", "#f8fafc", "#475569")
    draw_box(ax, 72, 12, 24, 32, "USER_AUDIT_LOG", "PK id (UUID)\napi_key (VARCHAR 64)\naction (VARCHAR 50)\nresource (TEXT)\nstatus_code (INT)\nlatency_ms (FLOAT)\ntimestamp (TIMESTAMP)", "#0f172a", "#f8fafc", "#475569")
    
    # Relationships
    draw_arrow(ax, 31, 75, 40, 75, "1 : 1 generates")
    draw_arrow(ax, 66, 75, 72, 75, "1 : 1 anchors")
    draw_arrow(ax, 53, 62, 20, 44, "1 : N produces")
    draw_arrow(ax, 53, 44, 53, 62, "M : N correlates")

    plt.tight_layout()
    p = OUT_DIR / "Fig_5_3_Entity_Relationship_Diagram.png"
    plt.savefig(p, dpi=300)
    plt.close()
    print("Fig 5.3 created:", p)
    
    with open(SRC_DIR / "Fig_5_3_Entity_Relationship_Diagram.puml", "w") as f:
        f.write("""@startuml
entity "SCAN_REQUEST" as req {
  * id : UUID <<PK>>
  --
  canonical_url : TEXT
  url_hash : VARCHAR(64)
  client_ip : VARCHAR(45)
  requested_at : TIMESTAMP
  status : ENUM
}

entity "VERDICT_RECORD" as verd {
  * id : UUID <<PK>>
  --
  scan_id : UUID <<FK>>
  verdict : ENUM
  risk_score : INT
  confidence : ENUM
  summary : TEXT
  signed_digest : VARCHAR(64)
}

entity "BLOCKCHAIN_ANCHOR" as bchain {
  * tx_hash : VARCHAR(66) <<PK>>
  --
  verdict_id : UUID <<FK>>
  merkle_root : VARCHAR(64)
  block_number : BIGINT
  anchored_at : TIMESTAMP
  contract_addr : VARCHAR(42)
}

entity "EVIDENCE_SIGNAL" as evid {
  * id : UUID <<PK>>
  --
  verdict_id : UUID <<FK>>
  layer : ENUM
  signal_name : VARCHAR(50)
  contribution : ENUM
  description : TEXT
  observed_at : TIMESTAMP
  technical_metadata : JSONB
}

entity "THREAT_INTEL_ENTRY" as intel {
  * id : UUID <<PK>>
  --
  indicator : TEXT
  indicator_type : ENUM
  source_feed : ENUM
  threat_type : ENUM
  is_active : BOOLEAN
}

req ||--|| verd : "generates"
verd ||--o| bchain : "anchors"
verd ||--|{ evid : "contains"
intel }|--|{ verd : "correlates"
@enduml
""")

# ---------------------------------------------------------------------------
# 4. Fig 5.4: Activity Diagram
# ---------------------------------------------------------------------------
def gen_fig5_4():
    fig, ax = create_canvas(8, 9)
    ax.text(50, 97, "ACTIVITY DIAGRAM: URL DETECTION WORKFLOW", ha='center', fontsize=12, fontweight='bold', color="#0f172a")
    
    # Steps from top to bottom
    y = 90
    draw_box(ax, 35, y, 30, 5, "Start: User Inputs URL", "", "#1e40af", "#eff6ff", "#3b82f6", radius=2.5)
    
    y -= 10
    draw_arrow(ax, 50, y+10, 50, y+5)
    draw_box(ax, 28, y, 44, 5, "URL Normalization & RFC 3986 Parsing", "", "#334155", "#f8fafc", "#64748b")
    
    y -= 10
    draw_arrow(ax, 50, y+10, 50, y+5)
    draw_box(ax, 24, y, 52, 6, "Decision: Check SSRF Boundary", "Host IP in RFC 1918 or IMDS (169.254.169.254)?", "#991b1b", "#fef2f2", "#ef4444")
    
    # SSRF Branch
    draw_arrow(ax, 76, y+3, 85, y+3)
    draw_box(ax, 78, y-8, 20, 6, "Reject Request\n(SSRF Blocked)", "", "#991b1b", "#fee2e2", "#b91c1c")
    ax.text(80, y+4.5, "Yes", fontsize=8, color="#dc2626", fontweight='bold')
    
    y -= 11
    draw_arrow(ax, 50, y+11, 50, y+6, "No (Public Origin)")
    draw_box(ax, 25, y, 50, 6, "Parallel Engine Execution (Async Workers)", "Lexical + Homoglyph + ML Classifier + Threat Feeds", "#4c1d95", "#f5f3ff", "#8b5cf6")
    
    y -= 11
    draw_arrow(ax, 50, y+11, 50, y+6)
    draw_box(ax, 28, y, 44, 6, "Multi-Signal Bayesian Verdict Engine", "Calculates Risk Score (0-100) & Assigns Band", "#831843", "#fdf2f8", "#ec4899")
    
    y -= 10
    draw_arrow(ax, 50, y+10, 50, y+5)
    draw_box(ax, 30, y, 40, 5, "Generate SHA-256 Evidence Digest", "Sign Verdict Hash for Auditability", "#0f172a", "#f8fafc", "#475569")
    
    y -= 10
    draw_arrow(ax, 50, y+10, 50, y+5)
    draw_box(ax, 25, y, 50, 6, "Store in Cache & Trigger UI Rendering", "Display SVG Gauge, Warning Screen or Pass", "#065f46", "#ecfdf5", "#10b981")
    
    y -= 8
    draw_arrow(ax, 50, y+8, 50, y+4)
    draw_box(ax, 40, y, 20, 4, "End: Complete", "", "#1e40af", "#eff6ff", "#3b82f6", radius=2)

    plt.tight_layout()
    p = OUT_DIR / "Fig_5_4_Activity_Diagram.png"
    plt.savefig(p, dpi=300)
    plt.close()
    print("Fig 5.4 created:", p)
    
    with open(SRC_DIR / "Fig_5_4_Activity_Diagram.mmd", "w") as f:
        f.write("""stateDiagram-v2
    [*] --> URL_Input: User Enters URL / Navigation Trigger
    URL_Input --> Normalization: Canonicalize RFC 3986 & Strip Obfuscation
    Normalization --> SSRF_Check: Evaluate Host IP & Rebinding
    
    state SSRF_Check <<choice>>
    SSRF_Check --> SSRF_Reject: Private Subnet / IMDS Detected (Yes)
    SSRF_Check --> Parallel_Analysis: Valid Public IP (No)
    
    state Parallel_Analysis {
        [*] --> Lexical_Entropy
        [*] --> Homoglyph_Levenshtein
        [*] --> ML_Statistical_Model
        [*] --> Threat_Feed_Lookup
    }
    
    Parallel_Analysis --> Verdict_Engine: Aggregate Signal Evidence
    Verdict_Engine --> Digest_Signing: Compute Tamper-Evident SHA-256 Digest
    Digest_Signing --> Client_Response: Return Risk Gauge, Ledger & Warning
    Client_Response --> [*]
    SSRF_Reject --> [*]
""")

# ---------------------------------------------------------------------------
# 5. Fig 5.5: Class Diagram
# ---------------------------------------------------------------------------
def gen_fig5_5():
    fig, ax = create_canvas(10, 7.5)
    ax.text(50, 96, "CLASS DIAGRAM: OBJECT-ORIENTED ENGINE MODEL", ha='center', fontsize=13, fontweight='bold', color="#0f172a")
    
    draw_box(ax, 4, 52, 28, 38, "URLNormalizer", "string canonical_url\nstring host\nstring path\nstring query\n--\n+ normalize(url: str): str\n+ parse_psl(): tuple\n+ compute_hash(): str\n+ is_valid_scheme(): bool", "#0f172a", "#f8fafc", "#334155")
    draw_box(ax, 36, 52, 28, 38, "MLClassifier", "float INTERCEPT = -3.80\ndict FEATURE_WEIGHTS\nset HIGH_ABUSE_TLDS\nset TRUSTED_DOMAINS\n--\n+ extract_features(url): dict\n+ predict(url): dict\n+ calculate_entropy(str): float\n+ brand_proximity(host): float", "#0f172a", "#f8fafc", "#334155")
    draw_box(ax, 68, 52, 28, 38, "HomoglyphDetector", "dict CONFUSABLE_MAP\nlist TARGET_BRANDS\n--\n+ detect_lookalike(host): dict\n+ normalize_unicode(str): str\n+ calculate_levenshtein(): int\n+ is_punycode(host): bool", "#0f172a", "#f8fafc", "#334155")
    
    draw_box(ax, 18, 8, 30, 36, "VerdictEngine", "float risk_threshold = 0.5\n--\n+ synthesize_verdict(signals): Verdict\n+ compute_confidence(): str\n+ enforce_honesty_invariants(): void\n+ generate_digest(): str\n+ format_evidence_ledger(): list", "#0f172a", "#f8fafc", "#334155")
    draw_box(ax, 54, 8, 30, 36, "ThreatFeedManager", "list feeds = [URLhaus, OpenPhish]\nAPScheduler scheduler\n--\n+ sync_feeds_async(): void\n+ match_hash(url_hash): bool\n+ get_last_sync_timestamp(): datetime\n+ purge_stale_iocs(): void", "#0f172a", "#f8fafc", "#334155")
    
    draw_arrow(ax, 18, 52, 30, 44)
    draw_arrow(ax, 50, 52, 38, 44)
    draw_arrow(ax, 82, 52, 45, 44)
    draw_arrow(ax, 69, 44, 48, 25)

    plt.tight_layout()
    p = OUT_DIR / "Fig_5_5_Class_Diagram.png"
    plt.savefig(p, dpi=300)
    plt.close()
    print("Fig 5.5 created:", p)
    
    with open(SRC_DIR / "Fig_5_5_Class_Diagram.puml", "w") as f:
        f.write("""@startuml
skinparam classAttributeIconSize 0

class URLNormalizer {
  - canonical_url: String
  - host: String
  - psl_cache: PublicSuffixList
  + normalize(url: String): String
  + decompose_psl(host: String): Tuple
  + compute_sha256(canonical: String): String
}

class MLClassifier {
  - INTERCEPT: Float = -3.80
  - FEATURE_WEIGHTS: Map
  + extract_features(url: String): Map
  + predict(url: String): PredictionResult
  + shannon_entropy(s: String): Float
  + brand_proximity_score(host: String): Float
}

class HomoglyphDetector {
  - CONFUSABLE_MAP: Map
  - TARGET_BRANDS: List
  + detect_spoof(host: String): SpoofResult
  + levenshtein(s1: String, s2: String): Int
}

class ThreatFeedManager {
  - scheduler: APScheduler
  - cached_hashes: Set<String>
  + sync_feeds_async(): Void
  + query_indicator(hash: String): ThreatMatch
}

class VerdictEngine {
  + synthesize(signals: List<Signal>): VerdictRecord
  + compute_confidence(): ConfidenceLevel
  + enforce_honesty(): Void
  + sign_digest(verdict: VerdictRecord): String
}

URLNormalizer --> VerdictEngine
MLClassifier --> VerdictEngine
HomoglyphDetector --> VerdictEngine
ThreatFeedManager --> VerdictEngine
@enduml
""")

# ---------------------------------------------------------------------------
# 6. Fig 5.6: Sequence Diagram
# ---------------------------------------------------------------------------
def gen_fig5_6():
    fig, ax = create_canvas(10, 8)
    ax.text(50, 97, "SEQUENCE DIAGRAM: END-TO-END SCAN EXECUTION", ha='center', fontsize=12, fontweight='bold', color="#0f172a")
    
    # Actors and Lifelines
    entities = [
        (10, "Client / Ext"),
        (28, "API Gateway"),
        (46, "SSRF Guard"),
        (64, "Detection Engines"),
        (82, "Verdict / Signer"),
        (94, "Blockchain")
    ]
    
    for x, name in entities:
        draw_box(ax, x-7, 88, 14, 5, name, "", "#1e293b", "#f1f5f9", "#94a3b8", radius=1)
        ax.plot([x, x], [88, 5], color="#cbd5e1", linestyle="--", lw=1)
        
    y = 82
    draw_arrow(ax, 10, y, 28, y, "1: POST /api/v1/scan {url}")
    y -= 10
    draw_arrow(ax, 28, y, 46, y, "2: validate_ip_destination(url)")
    y -= 10
    draw_arrow(ax, 46, y, 28, y, "3: SSRF Pass: Public IP OK", color="#16a34a")
    y -= 10
    draw_arrow(ax, 28, y, 64, y, "4: run_engines_parallel()")
    y -= 10
    draw_arrow(ax, 64, y, 64, y-4, "5: Lexical + ML + Homoglyph")
    y -= 8
    draw_arrow(ax, 64, y, 82, y, "6: aggregate_signals(evidence)")
    y -= 10
    draw_arrow(ax, 82, y, 82, y-4, "7: compute_sha256_digest()")
    y -= 8
    draw_arrow(ax, 82, y, 94, y, "8: anchor_hash(optional)")
    y -= 8
    draw_arrow(ax, 82, y, 10, y, "9: return VerdictResponse (Risk, Gauge, Evidence)", color="#2563eb")

    plt.tight_layout()
    p = OUT_DIR / "Fig_5_6_Sequence_Diagram.png"
    plt.savefig(p, dpi=300)
    plt.close()
    print("Fig 5.6 created:", p)
    
    with open(SRC_DIR / "Fig_5_6_Sequence_Diagram.mmd", "w") as f:
        f.write("""sequenceDiagram
    autonumber
    actor User as Client / Browser Extension
    participant API as API Gateway (Nginx/FastAPI)
    participant SSRF as SSRF Defense Boundary
    participant Core as Detection & ML Engines
    participant Verdict as Verdict Engine & Signer
    participant Ledger as Blockchain Registry

    User->>API: POST /api/v1/scan (target URL)
    API->>SSRF: Inspect IP address & Rebinding Guard
    SSRF-->>API: Verified Public Target (Pass)
    API->>Core: Dispatch parallel lexical, ML, homoglyph, and threat feed jobs
    Core-->>Verdict: Return individual layer evidence vectors
    Verdict->>Verdict: Compute Bayesian score (0-100) and enforce honesty policy
    Verdict->>Verdict: Generate signed SHA-256 evidence digest
    Verdict->>Ledger: Anchor cryptographic digest on-chain
    Verdict-->>User: Return VerdictResponse (Score, Risk Band, Gauge, Evidence Ledger)
""")

# ---------------------------------------------------------------------------
# 7. Fig 5.7: Data Flow Diagram Level 0 (Context Diagram)
# ---------------------------------------------------------------------------
def gen_fig5_7():
    fig, ax = create_canvas(9, 6.5)
    ax.text(50, 95, "DATA FLOW DIAGRAM (DFD) LEVEL 0: CONTEXT DIAGRAM", ha='center', fontsize=12, fontweight='bold', color="#0f172a")
    
    # External entities
    draw_box(ax, 5, 58, 22, 14, "Web Browser / User", "Submits unverified URL,\nReceives Risk Gauge & Warning", "#1e40af", "#eff6ff", "#3b82f6")
    draw_box(ax, 5, 18, 22, 14, "Threat Feeds\n(URLhaus/OpenPhish)", "Provides daily phishing\nand malware IoC updates", "#1e40af", "#eff6ff", "#3b82f6")
    draw_box(ax, 73, 58, 22, 14, "Security Analyst /\nAuditor", "Queries tamper-evident\nverdict verification receipts", "#1e40af", "#eff6ff", "#3b82f6")
    draw_box(ax, 73, 18, 22, 14, "Blockchain Network\n(EVM Ledger)", "Stores immutable digest\nhashes for proof of detection", "#1e40af", "#eff6ff", "#3b82f6")
    
    # Central Process
    circ = patches.Circle((50, 45), 18, ec="#10b981", fc="#ecfdf5", lw=2, zorder=2)
    ax.add_patch(circ)
    ax.text(50, 48, "0.0\nURLSENTINEL\nPLATFORM", ha='center', va='center', fontsize=10, fontweight='bold', color="#065f46", zorder=3)
    ax.text(50, 36, "AI Phishing &\nThreat Detection", ha='center', va='center', fontsize=8, color="#047857", zorder=3)
    
    # Data flows
    draw_arrow(ax, 27, 68, 40, 56, "Unverified URL String")
    draw_arrow(ax, 38, 48, 27, 60, "Verdict & Risk Score")
    draw_arrow(ax, 27, 28, 38, 36, "Malicious Feeds Data")
    draw_arrow(ax, 60, 52, 73, 64, "Signed Audit Receipt")
    draw_arrow(ax, 60, 38, 73, 26, "Evidence Digest Hash")

    plt.tight_layout()
    p = OUT_DIR / "Fig_5_7_DFD_Level_0.png"
    plt.savefig(p, dpi=300)
    plt.close()
    print("Fig 5.7 created:", p)
    
    with open(SRC_DIR / "Fig_5_7_DFD_Level_0.mmd", "w") as f:
        f.write("""graph LR
    User[Web User / Browser Extension] -->|1. Unverified Target URL| P0((0.0 URLSentinel Threat Platform))
    P0 -->|2. Risk Score, Gauge & Warning| User
    Feeds[External Threat Feeds URLhaus/OpenPhish] -->|3. Phishing/Malware IoC Feeds| P0
    P0 -->|4. Signed Cryptographic Digest| Chain[Blockchain Threat Registry]
    Analyst[Security Auditor / Analyst] -->|5. Query Verification Hash| P0
    P0 -->|6. Cryptographic Provenance Receipt| Analyst
""")

# ---------------------------------------------------------------------------
# 8. Fig 5.8: Data Flow Diagram Level 1
# ---------------------------------------------------------------------------
def gen_fig5_8():
    fig, ax = create_canvas(10, 7.5)
    ax.text(50, 96, "DATA FLOW DIAGRAM (DFD) LEVEL 1: SUB-PROCESS DECOMPOSITION", ha='center', fontsize=12, fontweight='bold', color="#0f172a")
    
    draw_box(ax, 4, 76, 18, 10, "1.0 Ingestion &\nNormalization", "", "#1e293b", "#f8fafc", "#475569", radius=3)
    draw_box(ax, 32, 76, 18, 10, "2.0 SSRF &\nSecurity Gate", "", "#991b1b", "#fef2f2", "#ef4444", radius=3)
    draw_box(ax, 60, 76, 18, 10, "3.0 Parallel Feature\nExtraction", "", "#1e293b", "#f8fafc", "#475569", radius=3)
    draw_box(ax, 60, 42, 18, 10, "4.0 ML Classifier\nInference", "", "#4c1d95", "#f5f3ff", "#8b5cf6", radius=3)
    draw_box(ax, 32, 42, 18, 10, "5.0 Verdict Engine\nSynthesis", "", "#065f46", "#ecfdf5", "#10b981", radius=3)
    draw_box(ax, 4, 42, 18, 10, "6.0 Digest Signing\n& Anchoring", "", "#831843", "#fdf2f8", "#ec4899", radius=3)
    
    # Data stores
    draw_box(ax, 20, 14, 25, 8, "D1: Threat Intelligence Feed DB", "URLhaus, OpenPhish Active IoCs", "#1e3a8a", "#eff6ff", "#3b82f6")
    draw_box(ax, 58, 14, 25, 8, "D2: Distributed Cache & Log", "Redis Hashes / Scan Records", "#1e3a8a", "#eff6ff", "#3b82f6")
    
    draw_arrow(ax, 22, 81, 32, 81, "Canonical URL")
    draw_arrow(ax, 50, 81, 60, 81, "Public Host")
    draw_arrow(ax, 69, 76, 69, 52, "Features")
    draw_arrow(ax, 60, 47, 50, 47, "ML Risk Score")
    draw_arrow(ax, 32, 47, 22, 47, "Verdict")
    
    # Data store flows
    draw_arrow(ax, 32, 22, 40, 42, "Feed Match")
    draw_arrow(ax, 41, 42, 65, 22, "Write Result")

    plt.tight_layout()
    p = OUT_DIR / "Fig_5_8_DFD_Level_1.png"
    plt.savefig(p, dpi=300)
    plt.close()
    print("Fig 5.8 created:", p)
    
    with open(SRC_DIR / "Fig_5_8_DFD_Level_1.mmd", "w") as f:
        f.write("""graph TD
    In[User URL] --> P1[1.0 Canonicalization & Normalization]
    P1 -->|Clean URL| P2[2.0 SSRF & Destination IP Gate]
    P2 -->|Public Origin| P3[3.0 Parallel Feature Extraction]
    P3 -->|Entropy, Tokens, Brand Proximity| P4[4.0 ML Classifier v2.1]
    P4 -->|Prediction & Attributions| P5[5.0 Multi-Signal Verdict Engine]
    D1[(D1: Threat Feed Cache)] -->|Known Signatures| P5
    P5 -->|Final Verdict| P6[6.0 Cryptographic Digest & Blockchain Anchoring]
    P5 -->|Cache Result| D2[(D2: Redis Scan Store)]
    P6 --> Out[Signed Risk Receipt & User UI]
""")

# ---------------------------------------------------------------------------
# 9. Fig 6.1: Feature Extraction Flowchart
# ---------------------------------------------------------------------------
def gen_fig6_1():
    fig, ax = create_canvas(9, 8)
    ax.text(50, 97, "FEATURE EXTRACTION & STATISTICAL HEURISTIC PIPELINE", ha='center', fontsize=12, fontweight='bold', color="#0f172a")
    
    y = 90
    draw_box(ax, 30, y, 40, 5, "Normalized Canonical URL", "", "#1e293b", "#f8fafc", "#475569")
    
    y -= 10
    draw_arrow(ax, 50, y+10, 50, y+5)
    draw_box(ax, 20, y, 60, 6, "1. Syntactic Parsing (urllib.parse)", "Decompose Scheme, Netloc, Path, Query Parameters", "#1e40af", "#eff6ff", "#3b82f6")
    
    y -= 11
    draw_arrow(ax, 50, y+11, 50, y+6)
    draw_box(ax, 10, y, 80, 7, "2. Structural & Statistical Feature Computation", "Shannon Entropy H(s), Digit Ratio, Symbol Ratio, Subdomain Depth, Path Depth", "#4c1d95", "#f5f3ff", "#8b5cf6")
    
    y -= 12
    draw_arrow(ax, 50, y+12, 50, y+7)
    draw_box(ax, 10, y, 80, 8, "3. Domain Proximity & Deceptive Brand Analysis", "Levenshtein Edit Distance to 40+ Brands, Brand in Subdomain of Foreign TLD,\nConsonant-Run Ratio (DGA Detection), Known URL Shortener Detection", "#065f46", "#ecfdf5", "#10b981")
    
    y -= 11
    draw_arrow(ax, 50, y+11, 50, y+6)
    draw_box(ax, 20, y, 60, 6, "4. Trusted Enterprise Override Filter", "If verified cloud / SSO provider (Google, Microsoft, AWS) -> Neutralize False Alarms", "#0f172a", "#f1f5f9", "#64748b")
    
    y -= 11
    draw_arrow(ax, 50, y+11, 50, y+6)
    draw_box(ax, 15, y, 70, 6, "5. Sigmoid Probability Computation: P = 1 / (1 + e^-z)", "z = -3.80 + Sum(w_i * f_i) | Calibrated Thresholds: 0.80 Crit, 0.55 High, 0.30 Elev", "#831843", "#fdf2f8", "#ec4899")
    
    y -= 9
    draw_arrow(ax, 50, y+9, 50, y+4)
    draw_box(ax, 25, y, 50, 5, "Output: Score, Risk Band & Attribution Vectors", "", "#1e293b", "#f8fafc", "#475569")

    plt.tight_layout()
    p = OUT_DIR / "Fig_6_1_Feature_Extraction_Pipeline.png"
    plt.savefig(p, dpi=300)
    plt.close()
    print("Fig 6.1 created:", p)
    
    with open(SRC_DIR / "Fig_6_1_Feature_Extraction_Pipeline.mmd", "w") as f:
        f.write("""flowchart TD
    In[Canonical URL String] --> Parse[Decompose into Host, Path, Query]
    Parse --> Entropy[Calculate Shannon Entropy on Host]
    Parse --> Subdomain[Compute Subdomain Depth Anomaly]
    Parse --> Proximity[Compute Levenshtein Brand Proximity]
    Parse --> DGA[Evaluate Consonant & Vowel Ratios]
    Parse --> Shortener[Check Known Shortener Services]
    Entropy & Subdomain & Proximity & DGA & Shortener --> Trusted{Is Trusted SSO Domain?}
    Trusted -->|Yes| Override[Zero Out False Positive Penalty]
    Trusted -->|No| Matrix[Dot Product with Calibrated Weights]
    Override --> Matrix
    Matrix --> Sigmoid[Sigmoid Function P = 1 / 1 + exp -z]
    Sigmoid --> Output[Emit Calibrated Score & Explanations]
""")

# ---------------------------------------------------------------------------
# 10. Fig 6.2: Blockchain Verification Workflow
# ---------------------------------------------------------------------------
def gen_fig6_2():
    fig, ax = create_canvas(10, 7)
    ax.text(50, 96, "BLOCKCHAIN-BACKED THREAT INTELLIGENCE & VERIFICATION", ha='center', fontsize=12, fontweight='bold', color="#0f172a")
    
    draw_box(ax, 5, 68, 25, 16, "1. Verdict Generation", "URLSentinel core analyzes\nURL and compiles evidence\nledger into JSON structure", "#1e3a8a", "#eff6ff", "#3b82f6")
    draw_box(ax, 38, 68, 25, 16, "2. Cryptographic Digest", "SHA-256 hash computed:\nH(url_hash + verdict +\nscore + timestamp + evidence)", "#4c1d95", "#f5f3ff", "#8b5cf6")
    draw_box(ax, 71, 68, 25, 16, "3. Smart Contract Anchor", "Transaction sent to\nThreatRegistry.sol with digest\nand threat severity category", "#065f46", "#ecfdf5", "#10b981")
    
    draw_arrow(ax, 30, 76, 38, 76, "Evidence")
    draw_arrow(ax, 63, 76, 71, 76, "Digest")
    
    # Bottom verification loop
    draw_box(ax, 71, 14, 25, 16, "4. Immutable Log", "Event ThreatRegistered emitted,\nstored permanently on-chain\nwith block height & timestamp", "#831843", "#fdf2f8", "#ec4899")
    draw_box(ax, 38, 14, 25, 16, "5. Public Verification", "Third-party auditor or client\nqueries contract using verdict ID\nto retrieve on-chain digest", "#0f172a", "#f8fafc", "#475569")
    draw_box(ax, 5, 14, 25, 16, "6. Proof of Non-Tampering", "Local hash recomputation\nmatches on-chain digest exactly:\nGuarantees zero log tampering", "#16a34a", "#f0fdf4", "#22c55e")
    
    draw_arrow(ax, 83, 68, 83, 30, "On-chain tx")
    draw_arrow(ax, 71, 22, 63, 22, "Query")
    draw_arrow(ax, 38, 22, 30, 22, "Match: 100%")

    plt.tight_layout()
    p = OUT_DIR / "Fig_6_2_Blockchain_Verification_Workflow.png"
    plt.savefig(p, dpi=300)
    plt.close()
    print("Fig 6.2 created:", p)
    
    with open(SRC_DIR / "Fig_6_2_Blockchain_Verification_Workflow.mmd", "w") as f:
        f.write("""sequenceDiagram
    autonumber
    participant Engine as URLSentinel Verdict Engine
    participant Hash as Cryptographic Signer (SHA-256)
    participant Contract as ThreatRegistry.sol (EVM)
    participant Auditor as External Security Auditor

    Engine->>Hash: Pass normalized URL, risk score, evidence IDs
    Hash->>Hash: Generate SHA-256 digest: H(payload)
    Hash->>Contract: registerThreat(urlHash, riskScore, evidenceDigest)
    Contract->>Contract: Emit ThreatRegistered event on immutable block
    Auditor->>Contract: getThreatProof(urlHash)
    Contract-->>Auditor: Return on-chain anchored digest & block timestamp
    Auditor->>Auditor: Recompute SHA-256 locally & compare
    Note over Auditor: Exact Match Proves Non-Tampering & Auditability
""")

# Execute all generators
gen_fig5_1()
gen_fig5_2()
gen_fig5_3()
gen_fig5_4()
gen_fig5_5()
gen_fig5_6()
gen_fig5_7()
gen_fig5_8()
gen_fig6_1()
gen_fig6_2()

print("ALL 10 DIAGRAMS AND EDITABLE SOURCES CREATED SUCCESSFULLY!")
