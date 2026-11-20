"""
report_sections/chapter4_methodology.py - Chapter 4: METHODOLOGY for URLSentinel PPD Report
"""

from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from report_sections.common import (
    add_para, add_heading_1, add_heading_2, add_heading_3,
    add_code_block
)

def build_chapter_4(doc):
    p_ch = doc.add_paragraph()
    p_ch.paragraph_format.space_before = Pt(12)
    p_ch.paragraph_format.space_after = Pt(12)
    r_ch = p_ch.add_run("CHAPTER 4\nMETHODOLOGY")
    r_ch.font.name = 'Times New Roman'
    r_ch.font.size = Pt(16)
    r_ch.bold = True
    p_ch.alignment = WD_ALIGN_PARAGRAPH.CENTER

    # 4.1 System Workflow
    add_heading_2(doc, "4.1 System Workflow")
    add_para(doc,
        "The methodological framework of URLSentinel is engineered as an end-to-end, multi-stage detection pipeline designed to process "
        "incoming web targets with deterministic latency and high classification fidelity. The operational workflow progresses through "
        "eight sequential phases:")

    workflow_steps = [
        ("Phase 1: Ingestion and Pre-Validation",
         "The system intercepts or receives a raw candidate URL via the web dashboard, REST API, or browser extension. Immediate syntactic "
         "sanity checks verify that the string conforms to RFC 3986 standards. If the string lacks an explicit scheme, an 'http://' protocol "
         "is provisionally prepended to ensure uniform structural decomposition."),

        ("Phase 2: Canonicalization and Normalization",
         "The candidate URL undergoes canonical normalization: percent-encoded octets (e.g., '%20', '%2F') are safely resolved, whitespace is trimmed, "
         "the host authority is converted to lowercase, and Internationalized Domain Names (IDN) are decoded from ASCII Punycode ('xn--') into "
         "standard UTF-8 Unicode characters to unmask homoglyph obfuscation."),

        ("Phase 3: Fast-Path Cache & Whitelist Interception",
         "Before executing computationally intensive routines, the canonical host is evaluated against an in-memory high-speed cache and a verified "
         "enterprise Single-Sign-On (SSO) whitelist. If the apex domain strictly matches a trusted infrastructure provider (e.g., accounts.google.com, "
         "login.microsoftonline.com), the URL is immediately assigned a verified SAFE verdict, bypassing statistical inference to eliminate false positives."),

        ("Phase 4: Multi-Dimensional Feature Mining",
         "If the URL is not cached, the Feature Extraction Engine parses the string into 25+ distinct lexical, structural, and information-theoretic "
         "metrics, calculating Shannon entropy across tokens, evaluating DGA consonant-to-vowel distribution ratios, and performing Levenshtein distance "
         "scans against a protected brand directory."),

        ("Phase 5: Concurrent Analytical Evaluation",
         "The extracted feature vector is dispatched to the Machine Learning Classifier tier (an optimized Random Forest ensemble), which outputs a "
         "continuous threat probability P(malicious). Concurrently, local threat intelligence feeds (URLhaus, OpenPhish) are queried to identify "
         "prior malicious listings."),

        ("Phase 6: Multi-Signal Risk Engine Synthesis",
         "The Risk Engine synthesizes the statistical ML probability, heuristic feature triggers, and threat feed indicators using a calibrated "
         "Bayesian aggregation model, yielding a final composite risk score (0 to 100) and mapping it to a categorical verdict (SAFE, ELEVATED, "
         "SUSPICIOUS, MALICIOUS)."),

        ("Phase 7: Explainable Factor Compilation",
         "The system traverses active heuristic flags to compile human-readable, deterministic explanations justifying the risk score (e.g., "
         "'Suspected typosquatting of Paypal', 'Excessive subdomain depth', 'Randomized token entropy')."),

        ("Phase 8: Cryptographic Attestation and Response Dispatch",
         "A canonical SHA-256 evidence hash is computed over the verdict payload for optional on-chain blockchain registration. The complete "
         "telemetry response is dispatched to the client (triggering browser extension navigation blocking if the verdict is dangerous) and stored "
         "ephemerally in off-chain cache."),
    ]

    for p_name, p_desc in workflow_steps:
        add_para(doc, f"• {p_name}: {p_desc}", space_before=2, space_after=4, font_size=11)

    # 4.2 Data Collection and Processing
    add_heading_2(doc, "4.2 Data Collection and Processing")
    add_para(doc,
        "Supervised machine learning requires high-quality, representative datasets reflecting the genuine distribution of contemporary web traffic. "
        "A chronic flaw in existing literature is 'dataset leakage' and 'temporal bias,' where classifiers memorize specific domain names rather "
        "than learning generalizable lexical patterns [25]. To prevent these biases, URLSentinel utilizes a curated, domain-separated corpus:")

    add_para(doc,
        "1. Malicious Ground-Truth Corpus: Comprises 1,000 verified malicious and phishing URLs harvested from active cybersecurity intelligence "
        "repositories, including PhishTank (community-verified active phishing campaigns), URLhaus (malware distribution and payload delivery links), "
        "and OpenPhish (zero-day credential harvesting feeds). All samples were collected across diverse threat types, including bank impersonations, "
        "cloud storage lures, and executive spear-phishing campaigns.")

    add_para(doc,
        "2. Benign Ground-Truth Corpus: Comprises 1,000 legitimate URLs extracted from the Tranco Top 1 Million list, the Majestic Million, and official "
        "corporate Single-Sign-On (SSO) portals. The benign corpus was deliberately enriched with highly complex, deep-path URLs (e.g., OAuth redirects, "
        "e-commerce checkout flows, academic research repositories) to ensure that the classifier does not erroneously flag long or complex legitimate links.")

    add_para(doc,
        "3. Domain-Aware Preprocessing and Train/Test Splitting: To guarantee valid empirical evaluation, the dataset was processed using domain-aware "
        "partitioning. All URLs sharing an identical apex domain (e.g., different paths on 'google.com' or 'paypal.com') were strictly restricted to "
        "either the training set or the testing set, never split across both. This methodology ensures that the model learns invariant syntactic and "
        "information-theoretic characteristics of malicious attacks rather than memorizing domain-level tokens.")

    # 4.3 URL Detection and Risk Assessment Approach
    add_heading_2(doc, "4.3 URL Detection and Risk Assessment Approach")
    add_para(doc,
        "URLSentinel adopts a mathematical, multi-signal detection approach that unifies information theory, computational linguistics, "
        "and probabilistic ensemble learning. The foundational mathematical models governing the engine are defined as follows:")

    add_heading_3(doc, "4.3.1 Shannon Entropy Formulation")
    add_para(doc,
        "Information entropy quantifies the degree of uncertainty, randomness, and information density contained within a character sequence. "
        "Phishing toolkits and malware frequently generate randomized subdomains, hex-encoded paths, and algorithmic tokens. For a given string S "
        "composed of characters x from an alphabet A, Shannon entropy H(S) is formulated as:")

    add_para(doc,
        "H(S) = - \\sum_{i=1}^{n} P(x_i) \\log_2 P(x_i)",
        align=WD_ALIGN_PARAGRAPH.CENTER, space_before=4, space_after=6, font_size=12, bold=True)

    add_para(doc,
        "Where P(x_i) represents the empirical probability of character x_i occurring in string S of length L:\n"
        "P(x_i) = \\frac{\\text{count}(x_i)}{L}\n"
        "In natural language domain names, entropy values typically range between 2.2 and 3.4 bits per character. Conversely, obfuscated "
        "phishing tokens, Base64 encodings, and DGA-generated hosts exhibit entropy values exceeding 3.8 to 4.5 bits per character, providing "
        "a reliable statistical indicator of algorithmic randomization.")

    add_heading_3(doc, "4.3.2 Levenshtein Edit Distance for Brand Impersonation")
    add_para(doc,
        "To detect typosquatting and visual brand spoofing without relying on brittle exact-match dictionaries, URLSentinel employs the "
        "Levenshtein distance metric. The Levenshtein distance between two string sequences a and b of lengths |a| and |b| represents the "
        "minimum number of single-character edits (insertions, deletions, or substitutions) required to transform a into b:")

    add_para(doc,
        "\\text{lev}_{a,b}(i, j) = \\begin{cases} \\max(i, j) & \\text{if } \\min(i, j) = 0, \\\\ \\min \\begin{cases} \\text{lev}_{a,b}(i-1, j) + 1 \\\\ \\text{lev}_{a,b}(i, j-1) + 1 \\\\ \\text{lev}_{a,b}(i-1, j-1) + 1_{(a_i \\neq b_j)} \\end{cases} & \\text{otherwise.} \\end{cases}",
        align=WD_ALIGN_PARAGRAPH.CENTER, space_before=4, space_after=6, font_size=11, bold=True)

    add_para(doc,
        "URLSentinel isolates the core label of the candidate domain via the Public Suffix List (e.g., extracting 'paypa1' from 'login.paypa1.xyz'). "
        "It then computes lev(candidate, brand) across a monitored brand dictionary B. If the edit distance satisfies 1 <= lev(candidate, brand) <= 2, "
        "and the apex domain is not an authorized property of brand B, an immediate high-confidence brand impersonation alert is triggered.")

    add_heading_3(doc, "4.3.3 Consonant-to-Vowel Ratio for DGA Identification")
    add_para(doc,
        "Domain Generation Algorithms (DGAs) frequently produce domain names featuring unnatural clusters of consonants that violate phonetic "
        "phonotactics. URLSentinel evaluates the consonant-to-vowel distribution ratio R_cv on domain labels:")

    add_para(doc,
        "R_{cv} = \\frac{N_{\\text{consonants}}}{N_{\\text{vowels}} + 1}",
        align=WD_ALIGN_PARAGRAPH.CENTER, space_before=4, space_after=6, font_size=12, bold=True)

    add_para(doc,
        "Where N_consonants and N_vowels denote the count of English consonants and vowels respectively. Standard dictionary-based domain names "
        "exhibit R_cv values between 1.0 and 2.5. Domains exhibiting R_cv >= 3.5, or featuring sequences of 5 or more consecutive consonants, are "
        "flagged for algorithmic generation.")

    add_heading_3(doc, "4.3.4 Bayesian Multi-Signal Risk Score Aggregation")
    add_para(doc,
        "To prevent reliance upon any single point of failure, the final risk score R_total (0 to 100) is synthesized through a weighted Bayesian "
        "aggregation function that balances machine learning probabilities, heuristic risk points, and threat intelligence feeds:")

    add_para(doc,
        "R_{\\text{total}} = \\min\\left(100, \\; w_{\\text{ml}} \\cdot (P_{\\text{ml}} \\times 100) + w_{\\text{heur}} \\cdot S_{\\text{heur}} + w_{\\text{intel}} \\cdot I_{\\text{intel}}\\right)",
        align=WD_ALIGN_PARAGRAPH.CENTER, space_before=4, space_after=6, font_size=11, bold=True)

    add_para(doc,
        "Where weights are empirically calibrated as w_ml = 0.40, w_heur = 0.35, and w_intel = 0.25. However, this statistical score is strictly "
        "subordinated to safety boundary invariants: if a verified threat intelligence match occurs, R_total is instantly clamped to 98 (MALICIOUS). "
        "Conversely, if the host belongs to the verified SSO infrastructure whitelist, R_total is hard-clamped to <= 10 (SAFE).")

    # 4.4 Tools and Technologies Used
    add_heading_2(doc, "4.4 Tools and Technologies Used")
    add_para(doc,
        "The URLSentinel implementation unifies a modern, production-grade technology stack engineered for high throughput, type safety, "
        "and modular deployment across platforms:")

    add_para(doc,
        "• Core Analytics Runtime: Python 3.12 (utilizing optimized bytecode execution, asynchronous asyncio pipelines, and native typing).\n"
        "• Asynchronous Web Framework: FastAPI 0.115 with Uvicorn ASGI server and Pydantic v2 data validation schemas.\n"
        "• Machine Learning Engine: Scikit-learn 1.5, NumPy, and SciPy for Random Forest ensemble modeling and feature array operations.\n"
        "• Frontend Web Application: Next.js 14 (React 18), Tailwind CSS, Lucide React icons, and custom SVG animation gauges.\n"
        "• Browser Protection Extension: Chromium Manifest V3 WebExtension architecture, JavaScript ES2024, and Chrome Storage API.\n"
        "• Decentralized Ledger & Cryptography: Web3.py, Solidity smart contracts, and hashlib SHA-256 for cryptographic evidence hashing.\n"
        "• Containerization & Sandboxing: Docker Engine, Docker Compose, Linux namespaces, and iptables egress network isolation.")

    # 4.5 Advantages of the Proposed Methodology
    add_heading_2(doc, "4.5 Advantages of the Proposed Methodology")
    add_para(doc,
        "The synthesized methodology delivers decisive advantages over conventional malicious URL detection architectures:\n"
        "1. Zero Detection Lag: Operates proactively at the point of navigation, identifying zero-hour phishing domains before external blacklist indexing.\n"
        "2. Ultra-Low Latency Execution: Feature extraction executes in under 1.5 milliseconds, allowing seamless real-time inline browser interception.\n"
        "3. Zero False Alarms on Enterprise Services: Protected domain whitelisting eliminates disruptive false positives on complex corporate OAuth URLs.\n"
        "4. Tamper-Evident Verification: Merkle-hashed blockchain anchoring guarantees that threat verdicts cannot be retroactively altered.\n"
        "5. Complete Scanning Infrastructure Containment: Disposable, egress-restricted sandboxes prevent SSRF vulnerabilities and internal network compromise.")

    doc.add_page_break()
    print("Chapter 4 built successfully.")
