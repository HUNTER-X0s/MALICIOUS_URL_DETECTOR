"""
report_sections/chapter3_sys_analysis.py - Chapter 3: SYSTEM ANALYSIS for URLSentinel PPD Report
"""

from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from report_sections.common import (
    add_para, add_heading_1, add_heading_2, add_heading_3,
    set_cell_background, set_table_borders, style_table_header, style_table_cells
)

def build_chapter_3(doc):
    p_ch = doc.add_paragraph()
    p_ch.paragraph_format.space_before = Pt(12)
    p_ch.paragraph_format.space_after = Pt(12)
    r_ch = p_ch.add_run("CHAPTER 3\nSYSTEM ANALYSIS")
    r_ch.font.name = 'Times New Roman'
    r_ch.font.size = Pt(16)
    r_ch.bold = True
    p_ch.alignment = WD_ALIGN_PARAGRAPH.CENTER

    # 3.1 Overall Description
    add_heading_2(doc, "3.1 Overall Description")
    add_para(doc,
        "System analysis establishes the formal operational requirements, architectural boundaries, human user interactions, "
        "and environmental feasibility constraints governing the URLSentinel cybersecurity platform. The system operates as a "
        "hybrid cyber-defense ecosystem combining distributed endpoint protection (via browser extensions), centralized analytical "
        "microservices (via an asynchronous RESTful gateway), and decentralized verification registries (via blockchain smart contracts). "
        "The primary purpose of URLSentinel is to evaluate potentially malicious web targets prior to browser DOM rendering or user credential entry.")

    add_para(doc,
        "The system interacts with four primary stakeholder personas, each possessing defined access privileges, operational requirements, "
        "and security boundaries. Table 3.1 details these operational roles.")

    # Table 3.1
    p_t31 = doc.add_paragraph()
    p_t31.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_t31.paragraph_format.space_before = Pt(8)
    p_t31.paragraph_format.space_after = Pt(4)
    rt31 = p_t31.add_run("Table 3.1: URLSentinel User Roles, Access Privileges, and Functional Responsibilities")
    rt31.font.name = 'Times New Roman'
    rt31.font.size = Pt(10.5)
    rt31.bold = True

    roles_data = [
        ("End User\n(Consumer / Employee)",
         "Low privilege; Client-side only",
         "Web Browser Extension, Public Web Scanner UI",
         "Conduct on-demand URL scans; receive real-time interstitial warnings on suspicious links; view plain-English risk factors; manage extension allowlists."),

        ("SOC Analyst\n(Security Operations)",
         "Medium-High privilege; Read/Audit",
         "Enterprise Web Dashboard, REST API Analytics",
         "Inspect detailed forensic telemetry (entropy scores, DGA consonant ratios, SSL metadata); export structured JSON evidence; verify blockchain hashes."),

        ("Platform Engineer\n(System Administrator)",
         "Administrative privilege; Full access",
         "Backend CLI, Docker Orchestration, Settings API",
         "Manage threat intelligence feed synchronization; update ML classifier weights; configure rate limits; monitor sandbox container health; manage blockchain nodes."),

        ("Enterprise API Client\n(Third-Party System)",
         "Machine-to-Machine; Token authenticated",
         "FastAPI REST Endpoints (/api/v1/scan)",
         "Submit bulk URL batches programmatically; integrate automated web filtering into email gateways, SIEM pipelines, and enterprise proxy firewalls."),
    ]

    tbl_roles = doc.add_table(rows=len(roles_data) + 1, cols=4)
    tbl_roles.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(tbl_roles)

    rhdr = tbl_roles.rows[0]
    r_cols = ["User Role", "Privilege Level", "Primary Interface", "Operational Responsibilities"]
    c_widths = [1.5, 1.4, 1.6, 2.2]

    for idx, cell in enumerate(rhdr.cells):
        cell.paragraphs[0].add_run(r_cols[idx])
    style_table_header(rhdr, c_widths)

    for r_idx, r_row in enumerate(roles_data):
        row = tbl_roles.rows[r_idx + 1]
        for c_idx, val in enumerate(r_row):
            row.cells[c_idx].paragraphs[0].add_run(val)
    style_table_cells(tbl_roles, c_widths)

    # 3.2 Functional Requirements
    add_heading_2(doc, "3.2 Functional Requirements")
    add_para(doc,
        "Functional requirements delineate the explicit algorithmic capabilities, processing workflows, and system transformations that "
        "URLSentinel must execute. The platform specifies twelve core functional requirements (FR-01 through FR-12):")

    fr_list = [
        ("FR-01: Multi-Channel Ingestion",
         "The system shall accept arbitrary URL strings through three distinct channels: (a) interactive web scanner text input, (b) HTTP POST "
         "requests to the /api/v1/scan endpoint, and (c) Chromium browser navigation event listeners (webNavigation.onBeforeNavigate)."),

        ("FR-02: RFC 3986 Normalization and Decoding",
         "The system shall canonicalize incoming URL strings by stripping leading/trailing whitespace, resolving percent-encoded octets, "
         "converting uppercase scheme and host segments to lowercase, and decoding Internationalized Domain Names (IDN) via Punycode conversion."),

        ("FR-03: Real-Time Lexical Feature Extraction",
         "The system shall compute 25+ syntactic and lexical properties within 2 milliseconds, including URL length, domain depth, subdomain token "
         "count, path segment depth, special delimiter frequencies (@, -, _, ?, =), and numeric-to-alpha character ratios."),

        ("FR-04: Information-Theoretic Entropy Computation",
         "The system shall compute Shannon entropy H(X) independently across the domain string, path tokens, and entire URL to identify randomized "
         "and obfuscated token distributions characteristic of automated phishing toolkits."),

        ("FR-05: Algorithmic Brand Impersonation Protection",
         "The system shall isolate the registrable domain via the Public Suffix List (PSL) and calculate Levenshtein edit distances against an indexed "
         "lexicon of 50+ high-value corporate brands (e.g., PayPal, Microsoft, Apple, Google). If a distance of 1 or 2 is detected without apex "
         "authorization, a brand impersonation flag shall be triggered."),

        ("FR-06: Domain Generation Algorithm (DGA) Analysis",
         "The system shall evaluate consecutive consonant frequencies and consonant-to-vowel ratios on domain tokens. Domains exceeding a 3.0 ratio "
         "shall be classified with elevated DGA suspicion."),

        ("FR-07: Machine Learning Ensemble Classification",
         "The system shall pass the computed feature vector to a pre-trained Random Forest classifier ensemble to generate a statistical threat "
         "probability P(malicious|X) between 0.0 and 1.0."),

        ("FR-08: Threat Intelligence Feed Correlation",
         "The system shall cross-reference the canonical URL and domain against synchronized in-memory threat feeds (OpenPhish, URLhaus, PhishTank). "
         "Verified blacklist matches shall instantly yield a MALICIOUS verdict with a confidence rating of 1.0."),

        ("FR-09: Bayesian Risk Synthesis and Calibration",
         "The Risk Engine shall aggregate heuristic scores, ML probabilities, and threat intelligence into a unified 0–100 risk score, mapping "
         "the outcome into four discrete categories: SAFE (0–29), ELEVATED (30–59), SUSPICIOUS (60–84), and MALICIOUS (85–100)."),

        ("FR-10: Plain-Language Risk Factor Explainability",
         "The system shall generate human-readable, deterministic explanations for every non-zero risk score, detailing specific risk contributors "
         "(e.g., 'Excessive subdomain depth detected', 'Brand impersonation of Microsoft detected', 'Entropy indicates algorithmic obfuscation')."),

        ("FR-11: Chromium Manifest V3 Browser Protection",
         "The browser extension shall intercept web navigation prior to page commit. If an ELEVATED or MALICIOUS verdict is returned, the extension "
         "shall block DOM rendering and display a high-contrast interstitial warning screen offering safe retreat or explicit user override."),

        ("FR-12: Cryptographic Evidence Blockchain Anchoring",
         "The system shall compute a SHA-256 cryptographic digest over the combined tuple {URL, Verdict, Score, Timestamp, FeatureVector}. "
         "The resulting hash shall be anchored into a smart contract ledger on-chain to provide immutable, tamper-evident auditability."),
    ]

    for req_title, req_desc in fr_list:
        add_para(doc, f"• {req_title}: {req_desc}", space_before=2, space_after=4, font_size=11)

    # 3.3 Non-Functional Requirements
    add_heading_2(doc, "3.3 Non-Functional Requirements")
    add_para(doc,
        "Non-functional requirements specify the architectural quality attributes, operational limits, security postures, and performance "
        "budgets necessary to ensure production robustness. Table 3.2 outlines these requirements across six critical quality dimensions.")

    # Table 3.2
    p_t32 = doc.add_paragraph()
    p_t32.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_t32.paragraph_format.space_before = Pt(8)
    p_t32.paragraph_format.space_after = Pt(4)
    rt32 = p_t32.add_run("Table 3.2: Non-Functional System Specifications and Operational Quality Attributes")
    rt32.font.name = 'Times New Roman'
    rt32.font.size = Pt(10.5)
    rt32.bold = True

    nfr_data = [
        ("Performance & Latency",
         "Sub-millisecond feature extraction (<1.5 ms); Total REST API evaluation latency <50 ms; Browser extension policy lookup <20 ms; Throughput >1,000 req/sec under horizontal worker scaling."),

        ("Security & Isolation",
         "Zero-trust execution; Disposable Docker sandbox containers for active crawls; Non-root process execution (UID 10001); Strict egress iptables blocking RFC 1918 private subnets and AWS metadata (169.254.169.254)."),

        ("Reliability & Availability",
         "99.9% system availability target; Graceful degradation if external threat feeds become unreachable; In-memory LRU cache with Redis fallback; Comprehensive healthcheck endpoints (/healthz)."),

        ("Privacy & Data Governance",
         "Zero browsing history logging; Ephemeral URL caching with configurable 3600-second TTL; Anonymization of query client IP addresses; Full compliance with GDPR Article 25 (Privacy by Design)."),

        ("Usability & Accessibility",
         "FORTRESS v2.0 design system; WCAG 2.1 AA accessibility compliance; Contrast ratios exceeding 4.5:1; Responsive layout supporting desktop, tablet, and mobile views; Dynamic SVG animated threat gauges."),

        ("Maintainability & Portability",
         "Modular microservice architecture; 100% type annotations via Pydantic v2 and TypeScript; Automated CI/CD test gates via GitHub Actions; Multi-platform Docker containerization (Linux AMD64/ARM64)."),
    ]

    tbl_nfr = doc.add_table(rows=len(nfr_data) + 1, cols=2)
    tbl_nfr.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(tbl_nfr)

    nhdr = tbl_nfr.rows[0]
    nhdr.cells[0].paragraphs[0].add_run("Quality Attribute")
    nhdr.cells[1].paragraphs[0].add_run("Specification & Measurable Acceptance Criteria")
    style_table_header(nhdr, [2.0, 4.7])

    for r_idx, (q_attr, q_spec) in enumerate(nfr_data):
        row = tbl_nfr.rows[r_idx + 1]
        row.cells[0].paragraphs[0].add_run(q_attr)
        row.cells[1].paragraphs[0].add_run(q_spec)
    style_table_cells(tbl_nfr, [2.0, 4.7])

    # 3.4 Feasibility Study
    add_heading_2(doc, "3.4 Feasibility Study")
    add_para(doc,
        "Prior to committing significant engineering resources, a comprehensive three-dimensional feasibility study was conducted to "
        "evaluate technical viability, economic practicality, and operational sustainability.")

    add_heading_3(doc, "3.4.1 Technical Feasibility")
    add_para(doc,
        "The technical feasibility of URLSentinel is anchored upon mature, industry-standard open-source technologies. Python 3.12 provides "
        "the foundational runtime for core machine learning and lexical parsing, benefiting from JIT optimizations and asynchronous I/O primitives. "
        "FastAPI delivers an asynchronous ASGI web framework capable of handling thousands of concurrent connections with minimal memory overhead. "
        "Scikit-learn provides battle-tested Random Forest and Gradient Boosting algorithms requiring minimal CPU overhead during inference. "
        "Next.js 14 and Tailwind CSS allow rapid rendering of server-side components and highly responsive client dashboards. On the endpoint side, "
        "Chromium's Manifest V3 WebExtension architecture offers mature webNavigation and storage APIs capable of intercepting web requests "
        "without degrading user navigation performance. Extensive local prototyping confirmed that all technical dependencies integrate seamlessly.")

    add_heading_3(doc, "3.4.2 Economic Feasibility")
    add_para(doc,
        "From an economic perspective, URLSentinel is highly cost-effective. The entire technology stack comprises permissive open-source software "
        "(MIT and Apache 2.0 licenses), eliminating commercial software licensing fees. Threat intelligence is ingested from community and open "
        "cybersecurity feeds (OpenPhish Community, URLhaus, PhishTank) at zero monetary cost. The decoupled architecture runs comfortably on "
        "modest, cost-effective infrastructure (e.g., standard virtual machines with 2 vCPUs and 4GB RAM) capable of processing millions of monthly "
        "scans. For blockchain verification, utilizing a local EVM network or Layer-2 testnet eliminates public mainnet transaction gas fees entirely. "
        "Consequently, the system offers enterprise-grade threat protection at near-zero incremental operational expenditure.")

    add_heading_3(doc, "3.4.3 Operational Feasibility")
    add_para(doc,
        "Operational feasibility assesses the ease of system adoption, maintenance, and integration within everyday user workflows and enterprise SOCs. "
        "For non-technical end users, the browser extension operates fully autonomously: it requires zero manual configuration, incurs no noticeable "
        "browsing lag, and surfaces clear, actionable warnings only when genuine threats are intercepted. For enterprise security analysts, the "
        "system provides standardized REST API endpoints and structured JSON telemetry, allowing seamless integration into existing Security "
        "Information and Event Management (SIEM) systems (e.g., Splunk, Elastic, Sentinel). Deployment is encapsulated within Docker Compose "
        "manifests, ensuring that the entire platform can be instantiated in under five minutes on any modern server environment.")

    doc.add_page_break()
    print("Chapter 3 built successfully.")
