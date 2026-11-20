"""
report_sections/chapter5_sys_design.py - Chapter 5: SYSTEM DESIGN for URLSentinel PPD Report
"""

from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from report_sections.common import (
    DIAGRAMS_DIR, add_para, add_heading_1, add_heading_2, add_heading_3,
    add_image_box
)

def build_chapter_5(doc):
    p_ch = doc.add_paragraph()
    p_ch.paragraph_format.space_before = Pt(12)
    p_ch.paragraph_format.space_after = Pt(12)
    r_ch = p_ch.add_run("CHAPTER 5\nSYSTEM DESIGN")
    r_ch.font.name = 'Times New Roman'
    r_ch.font.size = Pt(16)
    r_ch.bold = True
    p_ch.alignment = WD_ALIGN_PARAGRAPH.CENTER

    # 5.1 System Architecture
    add_heading_2(doc, "5.1 System Architecture")
    add_para(doc,
        "The system architecture of URLSentinel is designed around principles of loose coupling, high concurrency, strict trust boundary "
        "enforcement, and verifiable data integrity. As illustrated in Figure 5.1, the platform is partitioned into three operational tiers: "
        "the Client and Ingestion Tier, the Analytical API and Detection Engine Tier, and the Storage and Blockchain Verification Tier.")

    add_para(doc,
        "1. Client and Ingestion Tier: Acts as the primary interface for users and automated systems. Web clients interact via the Next.js 14 "
        "FORTRESS dashboard, which renders responsive telemetry, real-time risk scores, and explainable threat factors. The Chromium Manifest V3 "
        "browser extension operates directly at the endpoint, monitoring web navigation events and querying local cache tables to intercept "
        "malicious targets before DOM execution. External systems connect through secure RESTful API endpoints governed by token authentication.")

    add_para(doc,
        "2. Analytical API and Detection Core Tier: Serves as the central evaluation engine. Built on Python 3.12 and FastAPI, this tier houses "
        "the URL Normalizer, Feature Extraction Pipeline, Random Forest ML Classifier, and Multi-Signal Risk Engine. These microservices execute "
        "in parallel: while the lexical engine extracts syntactic and information-theoretic features, the threat intelligence service queries "
        "in-memory feeds. For active crawling, an isolated Sandbox Scanner spins up disposable container workers operating behind strict egress "
        "firewalls to prevent Server-Side Request Forgery (SSRF).")

    add_para(doc,
        "3. Storage and Blockchain Verification Tier: Manages persistent data and cryptographic provenance. High-speed Redis instances provide "
        "sub-millisecond caching of recent URL verdicts. Historical scan telemetry is stored in relational PostgreSQL databases. For tamper-evident "
        "auditability, the Blockchain Verification layer calculates SHA-256 evidence digests and anchors authoritative verdicts to a decentralized "
        "smart contract registry, guaranteeing that threat evidence cannot be forged or altered retroactively.")

    add_image_box(doc, DIAGRAMS_DIR / "Fig_5_1_System_Architecture.png",
                  "Figure 5.1: URLSentinel Overall System Architecture Diagram", width_in=5.8)

    # 5.2 Use Case Diagram
    add_heading_2(doc, "5.2 Use Case Diagram")
    add_para(doc,
        "The Use Case Diagram depicted in Figure 5.2 formally models the interactions between human/machine actors and the functional "
        "capabilities provided by URLSentinel. Four distinct actors interact with the system across defined operational boundaries:")

    add_para(doc,
        "• End User: Initiates on-demand URL scans through the web interface; navigates the web under the active protection of the browser "
        "extension; receives real-time red-screen interstitial warning screens upon intercepting dangerous links; inspects human-readable "
        "risk explanations; and manages personal allowlists.\n"
        "• Security Analyst: Accesses deep forensic telemetry (entropy scores, token depths, Levenshtein brand distances); exports structured "
        "JSON/PDF threat reports; queries historical threat campaign trends; and verifies cryptographic transaction hashes on the blockchain ledger.\n"
        "• System Administrator: Manages automated threat intelligence feed synchronization; triggers model retraining pipelines; configures API "
        "rate limits; monitors isolated container health; and oversees blockchain smart contract deployment.\n"
        "• Enterprise API Client: Submits automated high-throughput URL batches for policy evaluation; consumes structured machine-readable "
        "JSON risk scores; and integrates detection verdicts into perimeter email gateways and enterprise SIEM pipelines.")

    add_image_box(doc, DIAGRAMS_DIR / "Fig_5_2_Use_Case_Diagram.png",
                  "Figure 5.2: System Use Case Diagram with User Roles and Operational Boundaries", width_in=5.8)

    # 5.3 Entity Relationship Diagram
    add_heading_2(doc, "5.3 Entity Relationship Diagram")
    add_para(doc,
        "The Entity Relationship Diagram (ERD) illustrated in Figure 5.3 captures the conceptual and physical database schema governing URLSentinel. "
        "The design enforces a strict separation between high-volume operational telemetry (stored off-chain in relational PostgreSQL tables) and "
        "immutable cryptographic evidence (anchored on-chain in smart contract state).")

    add_para(doc,
        "The primary entities and their relational constraints include:\n"
        "• Scans: Represents the central audit entity. Contains `scan_id` (Primary Key, UUID), `raw_url`, `canonical_url`, `verdict` (SAFE, "
        "ELEVATED, SUSPICIOUS, MALICIOUS), `risk_score` (Integer 0–100), `confidence` (Float 0.0–1.0), `evidence_hash` (VARCHAR 64 SHA-256), "
        "and `created_at` timestamp.\n"
        "• Features: Stores extracted analytical metrics associated with a scan. Contains `feature_id` (PK), `scan_id` (Foreign Key referencing Scans), "
        "`url_length`, `domain_depth`, `subdomain_count`, `path_depth`, `entropy`, `consonant_ratio`, `brand_distance`, and `ml_probability`. "
        "Maintains a strict 1-to-1 relationship with `Scans`.\n"
        "• ThreatIntel: Represents synchronized threat intelligence indicators. Contains `intel_id` (PK), `domain`, `feed_source` (URLhaus, "
        "PhishTank, OpenPhish), `is_malicious` (Boolean), `confidence_rating`, and `last_synced` timestamp.\n"
        "• BlockchainEvidence: Models on-chain cryptographic anchoring. Contains `tx_hash` (PK, VARCHAR 66), `scan_id` (FK referencing Scans), "
        "`block_number`, `evidence_hash`, `canonical_url`, `recorded_verdict`, and `signer_address`. Maintains a 1-to-1 relationship with `Scans`.")

    add_image_box(doc, DIAGRAMS_DIR / "Fig_5_3_Entity_Relationship_Diagram.png",
                  "Figure 5.3: Database Entity Relationship Diagram (Off-Chain Schema & Blockchain Anchors)", width_in=5.8)

    # 5.4 Activity Diagram
    add_heading_2(doc, "5.4 Activity Diagram")
    add_para(doc,
        "The Activity Diagram shown in Figure 5.4 illustrates the end-to-end procedural control flow and decision logic executed during a URL "
        "evaluation cycle. The workflow begins upon target URL submission and progresses through sequential processing nodes:")

    add_para(doc,
        "1. Input Normalization: The raw string is stripped of whitespace, percent-encoded octets are decoded, and IDN hostnames are converted from Punycode.\n"
        "2. Cache Decision Node: The canonical URL is checked against the high-speed Redis cache. If a fresh record exists, the cached verdict is returned immediately.\n"
        "3. Whitelist Decision Node: The domain is matched against the verified SSO whitelist. If verified, the system issues an immediate SAFE verdict.\n"
        "4. Concurrent Processing: If uncached, the URL branches into parallel execution paths: (a) lexical feature mining and Shannon entropy calculation, "
        "(b) ML ensemble probability inference, and (c) threat intelligence feed lookup.\n"
        "5. Risk Synthesis Decision Node: The Risk Engine aggregates all signals. If risk score >= 60 or threat feed match is positive, a warning is generated.\n"
        "6. Cryptographic Anchoring: The SHA-256 evidence digest is computed and anchored to the blockchain registry.\n"
        "7. Terminal Dispatch: The structured verdict is returned to the client application and cached locally.")

    add_image_box(doc, DIAGRAMS_DIR / "Fig_5_4_Activity_Diagram.png",
                  "Figure 5.4: URL Sentinel Activity Diagram (End-to-End Evaluation Workflow)", width_in=5.8)

    # 5.5 Class Diagram
    add_heading_2(doc, "5.5 Class Diagram")
    add_para(doc,
        "Figure 5.5 details the object-oriented architectural model implemented within the URLSentinel Python backend. The system adheres "
        "to SOLID object-oriented design principles, utilizing decoupled class abstractions, strict type annotations, and dependency injection.")

    add_para(doc,
        "The core class structures include:\n"
        "• URLNormalizer: Encapsulates static utility methods (`normalize_url`, `extract_host`, `decode_punycode`) conforming to RFC 3986.\n"
        "• FeatureExtractor: Orchestrates lexical parsing, Shannon entropy computation (`calculate_entropy`), Levenshtein brand distance scanning "
        "(`check_brand_impersonation`), and consonant-to-vowel ratio evaluation (`calculate_dga_ratio`), returning a structured `FeatureVector`.\n"
        "• MLClassifier: Manages model persistence and inference (`predict_proba`, `predict_verdict`), wrapping an optimized Scikit-learn Random Forest ensemble.\n"
        "• ThreatIntelService: Manages feed synchronization, local caching, and hash lookups (`check_reputation`, `sync_feeds`).\n"
        "• RiskEngine: Acts as the primary orchestrator, synthesizing `FeatureVector`, `MLPrediction`, and `IntelReport` into a final `ScanReport`.\n"
        "• BlockchainVerifier: Interacts with EVM smart contracts via Web3.py (`anchor_verdict`, `verify_evidence_hash`).")

    add_image_box(doc, DIAGRAMS_DIR / "Fig_5_5_Class_Diagram.png",
                  "Figure 5.5: Core Object-Oriented Class Diagram for Detection & Risk Engines", width_in=5.8)

    # 5.6 Sequence Diagram
    add_heading_2(doc, "5.6 Sequence Diagram")
    add_para(doc,
        "Figure 5.6 models the temporal message exchange between distributed system components during an asynchronous evaluation cycle. "
        "The sequence highlights the asynchronous parallel execution of ML inference and threat intelligence lookups, which minimizes "
        "aggregate pipeline latency.")

    add_para(doc,
        "The operational sequence proceeds as follows:\n"
        "1. Client initiates an HTTP POST `/api/v1/scan` request to the FastAPI Application Gateway.\n"
        "2. Gateway delegates the raw string to `URLNormalizer`, receiving a canonicalized URL representation in return.\n"
        "3. Gateway passes the canonical URL to `FeatureExtractor`, which computes lexical metrics and Shannon entropy in <1.5 ms.\n"
        "4. Gateway initiates asynchronous concurrent calls: invoking `MLClassifier.predict_proba()` and `ThreatIntelService.query_feeds()`.\n"
        "5. Both subsystems return their respective outputs to `RiskEngine`, which executes Bayesian risk aggregation and generates a `ScanReport`.\n"
        "6. `RiskEngine` dispatches the canonical evidence hash to `BlockchainVerifier` for background cryptographic anchoring.\n"
        "7. Gateway serializes the final `ScanReport` into structured JSON and returns an HTTP 200 response to the client.")

    add_image_box(doc, DIAGRAMS_DIR / "Fig_5_6_Sequence_Diagram.png",
                  "Figure 5.6: System Sequence Diagram for Concurrent Multi-Engine URL Evaluation", width_in=5.8)

    # 5.7 Data Flow Diagram
    add_heading_2(doc, "5.7 Data Flow Diagram")
    add_para(doc,
        "Data Flow Diagrams (DFDs) track the movement, transformation, and storage of data across the URLSentinel boundaries. "
        "The architecture is documented across two levels of hierarchical abstraction: Context Level (Level 0) and Functional Decomposition (Level 1).")

    add_heading_3(doc, "5.7.1 DFD Level 0 — Context Level Diagram")
    add_para(doc,
        "Figure 5.7 depicts the Level 0 Context Diagram, representing URLSentinel as a single conceptual processing entity surrounded by external "
        "actors and data sources. End Users and Browser Extensions submit candidate URLs and receive threat reports and interstitial warnings. "
        "Security Analysts query historical forensic data. External Threat Feeds supply updated malicious indicators. The Blockchain Ledger "
        "receives evidence hashes and returns cryptographic transaction confirmations.")

    add_image_box(doc, DIAGRAMS_DIR / "Fig_5_7_DFD_Level_0.png",
                  "Figure 5.7: Data Flow Diagram Level 0 (Context Level Architecture)", width_in=5.8)

    add_heading_3(doc, "5.7.2 DFD Level 1 — Decomposition Diagram")
    add_para(doc,
        "Figure 5.8 presents the Level 1 DFD, decomposing Process 0 into seven discrete sub-processes interacting with four internal data stores:\n"
        "• Process 1.0 (Input Normalization & Canonicalization): Cleans incoming URLs and reads/writes to Data Store 1 (URL Cache).\n"
        "• Process 2.0 (Lexical & Entropy Feature Mining): Transforms canonical strings into numerical feature arrays.\n"
        "• Process 3.0 (ML Probability Inference): Evaluates feature vectors against trained model weights.\n"
        "• Process 4.0 (Threat Feed Correlation): Matches domains against Data Store 2 (Threat Intelligence Store).\n"
        "• Process 5.0 (Multi-Signal Risk Synthesis): Synthesizes ML probabilities and feed data into final risk verdicts, writing to Data Store 3 (Scan Reports Database).\n"
        "• Process 6.0 (Isolated Sandbox Scanning): Executes active page crawls within disposable, egress-isolated containers.\n"
        "• Process 7.0 (Cryptographic Blockchain Anchoring): Formulates SHA-256 evidence digests and commits state updates to Data Store 4 (Blockchain Ledger).")

    add_image_box(doc, DIAGRAMS_DIR / "Fig_5_8_DFD_Level_1.png",
                  "Figure 5.8: Data Flow Diagram Level 1 (Engine Pipeline & Sandbox Isolation Decomposition)", width_in=5.8)

    doc.add_page_break()
    print("Chapter 5 built successfully.")
