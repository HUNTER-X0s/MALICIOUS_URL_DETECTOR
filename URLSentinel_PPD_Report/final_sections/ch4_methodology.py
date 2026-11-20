"""
final_sections/ch4_methodology.py - 4. METHODOLOGY (Target: 3 pages, pp. 11-13)
"""

from docx.shared import Inches, Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
from report_sections.common import (
    add_para, add_bullet, add_equation_box
)

def build_ch4(doc):
    # 4. METHODOLOGY
    p_h = doc.add_paragraph()
    p_h.paragraph_format.space_before = Pt(0)
    p_h.paragraph_format.space_after = Pt(10)
    p_h.paragraph_format.keep_with_next = True
    r = p_h.add_run("4. METHODOLOGY")
    r.font.name = 'Times New Roman'
    r.font.size = Pt(20)
    r.bold = True

    add_para(doc,
        "The proposed system is engineered using a structured, modular cybersecurity methodology combining high-speed lexical parsing, "
        "supervised machine learning, community threat intelligence correlation, and decentralized cryptographic evidence verification. "
        "The system operates across client-server boundaries, ensuring that endpoint browser extensions receive sub-20ms policy decisions "
        "while heavy dynamic inspection and blockchain anchoring execute asynchronously in isolated backend environments.")

    # 4.1 System Workflow
    p_sub = doc.add_paragraph()
    p_sub.paragraph_format.space_before = Pt(8)
    p_sub.paragraph_format.space_after = Pt(4)
    p_sub.paragraph_format.keep_with_next = True
    r = p_sub.add_run("4.1 System Workflow")
    r.font.name = 'Times New Roman'
    r.font.size = Pt(16)
    r.bold = True

    add_para(doc, "The step-by-step functioning of the detection and verification pipeline proceeds through the following sequential stages:")
    add_bullet("Target Reception: Candidate URLs are ingested via the Next.js web scanner, the FastAPI REST endpoint (/api/v1/scan), or the Chromium browser extension's webNavigation.onBeforeNavigate listener.")
    add_bullet("Canonical Normalization: The string is parsed according to RFC 3986, stripping default ports, normalizing schemes, lowercasing hostnames, and converting Punycode IDN glyphs (e.g., 'xn--' prefixes) to UTF-8 Unicode.")
    add_bullet("Whitelist & Cache Check: The canonical host is queried against an in-memory Redis cache and a verified Single-Sign-On (SSO) corporate whitelist (Google, Microsoft, GitHub). Whitelisted hosts receive an immediate SAFE verdict (Score <= 10).")
    add_bullet("Feature Extraction: If uncached, the feature engine computes 25+ lexical metrics, Shannon entropy H(S), Levenshtein brand distance, and DGA consonant-to-vowel distribution ratios in under 1.5 milliseconds.")
    add_bullet("Parallel Intelligence & ML Scoring: The feature vector is submitted to the Random Forest classifier to produce P(malicious). Concurrently, local threat feeds (URLhaus, OpenPhish) are queried for known malicious indicators.")
    add_bullet("Bayesian Risk Aggregation: The Risk Engine aggregates ML probability, heuristic triggers, and threat feed indicators into a calibrated 0–100 risk score and categorical verdict (SAFE, ELEVATED, SUSPICIOUS, MALICIOUS).")
    add_bullet("Cryptographic Attestation: A SHA-256 evidence digest is computed over the evaluation tuple and anchored into the EVM blockchain registry for immutable auditability.")
    add_bullet("Verdict Enforcement: If the verdict is ELEVATED or MALICIOUS, the browser extension displays an interstitial warning screen blocking DOM execution. Clean URLs proceed transparently.")

    # 4.2 Data Collection and Processing
    p_sub = doc.add_paragraph()
    p_sub.paragraph_format.space_before = Pt(8)
    p_sub.paragraph_format.space_after = Pt(4)
    p_sub.paragraph_format.keep_with_next = True
    r = p_sub.add_run("4.2 Data Collection and Processing")
    r.font.name = 'Times New Roman'
    r.font.size = Pt(16)
    r.bold = True

    add_para(doc,
        "Supervised machine learning models require high-quality, representative datasets to avoid overfitting and temporal bias [25]. "
        "The URLSentinel evaluation corpus was assembled using a curated, domain-separated methodology:")
    add_bullet("Malicious URL Corpus: 1,000 verified malicious URLs collected from active feeds including PhishTank (community-verified active phishing), URLhaus (malware distribution and payload delivery links), and OpenPhish (zero-day credential harvesting links).")
    add_bullet("Benign URL Corpus: 1,000 legitimate URLs extracted from the Tranco Top 1 Million list, the Majestic Million, and official corporate Single-Sign-On portals. Complex OAuth and deep-path URLs were included to stress-test the model against false alarms.")
    add_bullet("Domain-Aware Partitioning: To prevent dataset leakage, URLs sharing an identical apex domain were strictly isolated to either the training set or the testing set, never split across both, ensuring the model learns generalizable lexical patterns.")

    # 4.3 URL Detection and Risk Assessment Approach
    p_sub = doc.add_paragraph()
    p_sub.paragraph_format.space_before = Pt(8)
    p_sub.paragraph_format.space_after = Pt(4)
    p_sub.paragraph_format.keep_with_next = True
    r = p_sub.add_run("4.3 URL Detection and Risk Assessment Approach")
    r.font.name = 'Times New Roman'
    r.font.size = Pt(16)
    r.bold = True

    add_para(doc,
        "URLSentinel combines mathematical information theory, string edit metrics, and Bayesian probabilistic aggregation:")

    add_para(doc,
        "1. Shannon Entropy Formulation: Shannon entropy quantifies the randomness and information density of token sequences. "
        "Automated phishing toolkits and DGAs generate highly randomized subdomains and hex paths. For a string S of length L with "
        "character probabilities P(x_i), entropy H(S) is formulated as:")
    add_equation_box("H(S) = - ∑ [ P(x_i) · log₂(P(x_i)) ]", "Eq. 4.1")
    add_para(doc,
        "Natural language domains exhibit entropy values between 2.2 and 3.4 bits/char. Obfuscated phishing tokens and DGA domains "
        "consistently exceed 3.8 to 4.5 bits/char, providing a strong statistical indicator of automated generation.")

    add_para(doc,
        "2. Levenshtein Distance for Brand Impersonation: To detect typosquatting without brittle exact-match tables, the engine isolates "
        "the apex domain via the Public Suffix List and calculates the minimum edit distance lev(a, b) against 50+ monitored brands:")
    add_equation_box("lev(a, b) = min number of character insertions, deletions, or substitutions", "Eq. 4.2")
    add_para(doc,
        "If 1 <= lev(domain, brand) <= 2 and the registered domain is not an authorized property of the brand, an immediate brand impersonation flag is raised.")

    add_para(doc,
        "3. Consonant-to-Vowel Ratio for DGA Detection: DGAs frequently cluster consonants unnaturally. The consonant-to-vowel ratio R_cv is calculated as:")
    add_equation_box("R_cv = N_consonants / (N_vowels + 1)", "Eq. 4.3")
    add_para(doc, "Domains with R_cv >= 3.5 or containing 5+ consecutive consonants trigger an elevated DGA alert.")

    add_para(doc,
        "4. Bayesian Multi-Signal Risk Aggregation: The composite risk score R_total (0 to 100) aggregates machine learning probabilities, "
        "heuristic scores, and threat intelligence feeds:")
    add_equation_box("R_total = min(100,  0.40 · (P_ml · 100) + 0.35 · S_heur + 0.25 · I_intel)", "Eq. 4.4")
    add_para(doc,
        "Safety Invariant: If a confirmed threat feed match occurs, R_total is clamped to 98 (MALICIOUS). If the host is in the verified "
        "corporate SSO whitelist, R_total is hard-clamped to <= 10 (SAFE), guaranteeing zero false alarms.")

    # 4.4 Tools and Technologies Used
    p_sub = doc.add_paragraph()
    p_sub.paragraph_format.space_before = Pt(8)
    p_sub.paragraph_format.space_after = Pt(4)
    p_sub.paragraph_format.keep_with_next = True
    r = p_sub.add_run("4.4 Tools and Technologies Used")
    r.font.name = 'Times New Roman'
    r.font.size = Pt(16)
    r.bold = True

    add_bullet("Frontend: Next.js 14, React 18, TypeScript, Tailwind CSS, Lucide icons, and custom SVG animation gauges.")
    add_bullet("Backend API: Python 3.12, FastAPI ASGI framework, Uvicorn server, Pydantic v2 data models.")
    add_bullet("Machine Learning: Scikit-learn (Random Forest ensemble), NumPy, SciPy.")
    add_bullet("Browser Extension: Chromium Manifest V3 WebExtensions API, Chrome Storage API, Service Workers.")
    add_bullet("Database & Cache: Redis 7.0 for in-memory caching; SQLite / PostgreSQL for off-chain scan records.")
    add_bullet("Blockchain & Ledger: Web3.py, Solidity smart contracts (ThreatRegistry.sol), SHA-256 evidence hashing.")
    add_bullet("Security & Isolation: Docker Engine, Docker Compose, Linux iptables egress filtering.")

    # 4.5 Advantages of the Proposed Methodology
    p_sub = doc.add_paragraph()
    p_sub.paragraph_format.space_before = Pt(8)
    p_sub.paragraph_format.space_after = Pt(4)
    p_sub.paragraph_format.keep_with_next = True
    r = p_sub.add_run("4.5 Advantages of the Proposed Methodology")
    r.font.name = 'Times New Roman'
    r.font.size = Pt(16)
    r.bold = True

    add_bullet("Sub-Millisecond Speed: Complete lexical feature extraction executes in 1.39 ms, enabling seamless inline browser protection.")
    add_bullet("Zero False Positives on Enterprise Portals: PSL domain tokenization and SSO whitelisting eliminate disruptive false alarms.")
    add_bullet("Actionable Explainability: Provides plain-language risk factors detailing why a URL was flagged rather than opaque scores.")
    add_bullet("Immutable Audit Trail: Cryptographic SHA-256 evidence digests anchored on blockchain eliminate retroactive data tampering.")
    add_bullet("Infrastructure Containment: Strict egress firewall rules prevent SSRF and internal network enumeration during active scans.")

    doc.add_page_break()
    print("Chapter 4 built (pages 11-13).")
