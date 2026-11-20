"""
report_sections/chapter1_intro.py - Chapter 1: INTRODUCTION for URLSentinel PPD Report
"""

from docx.shared import Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
from report_sections.common import (
    add_para, add_heading_1, add_heading_2, add_heading_3
)

def build_chapter_1(doc):
    # Chapter Title
    p_ch = doc.add_paragraph()
    p_ch.paragraph_format.space_before = Pt(12)
    p_ch.paragraph_format.space_after = Pt(12)
    r_ch = p_ch.add_run("CHAPTER 1\nINTRODUCTION")
    r_ch.font.name = 'Times New Roman'
    r_ch.font.size = Pt(16)
    r_ch.bold = True
    p_ch.alignment = WD_ALIGN_PARAGRAPH.CENTER

    # 1.1 Motivation
    add_heading_2(doc, "1.1 Motivation")
    add_para(doc,
        "The modern digital economy is fundamentally anchored upon the World Wide Web. Daily personal communication, financial transactions, "
        "enterprise enterprise resource planning, healthcare records, and critical government infrastructure rely upon the Uniform Resource Locator "
        "(URL) as the primary navigational mechanism for internet resource discovery. However, this ubiquity has established web navigation as the "
        "foremost attack vector for global cyber adversaries. According to recent threat reports published by the Anti-Phishing Working Group (APWG) "
        "and the Cybersecurity and Infrastructure Security Agency (CISA), phishing and malicious URL distributions have reached unprecedented volumes, "
        "accounting for over 70% of initial enterprise compromises and millions of consumer identity thefts annually [1], [2].")

    add_para(doc,
        "Historically, cybersecurity defenses have relied upon reactive blocklists and centralized reputation services, such as Google Safe Browsing, "
        "Spamhaus, and PhishTank. While these services provide baseline protection against known threats, they suffer from a fundamental systemic "
        "limitation: detection lag. The typical lifespan of a malicious phishing campaign is now measured in hours, or even minutes. Adversaries "
        "routinely deploy automated Phishing-as-a-Service (PaaS) platforms, bulletproof hosting, fast-flux DNS networks, and Domain Generation "
        "Algorithms (DGA) to cycle through thousands of ephemeral domain names. Studies indicate that over 65% of malicious URLs disappear within "
        "four to eight hours of generation, whereas centralized blacklist ingestion, verification, and client synchronization cycles typically require "
        "between 12 and 72 hours [3], [4]. Consequently, victims navigate to malicious links during this critical zero-hour detection gap when traditional "
        "blacklists report the destination as benign or unknown.")

    add_para(doc,
        "Furthermore, contemporary web users face increasingly sophisticated psychological and technical deception. Threat actors utilize Internationalized "
        "Domain Name (IDN) homograph attacks, lookalike Unicode characters, sub-domain abuse on legitimate cloud providers, and complex redirect chains "
        "designed to bypass perimeter firewalls. In consumer environments, the growing reliance on mobile and desktop web browsers without robust, "
        "privacy-preserving endpoint telemetry leaves end-users vulnerable to deceptive credential harvesting and zero-day drive-by downloads.")

    add_para(doc,
        "These realities establish an urgent, non-negotiable imperative for a proactive, intelligent, and decentralized cybersecurity platform. "
        "To protect users effectively, a detection architecture must evaluate URLs in real time at the point of click, synthesize multi-dimensional "
        "lexical and behavioral features using artificial intelligence, maintain cryptographic auditability without central tampering, and enforce "
        "strict data privacy and zero-trust isolation boundaries. This challenging engineering objective constitutes the primary motivation behind "
        "the URLSentinel research and product development project.")

    # 1.2 Problem Statement
    add_heading_2(doc, "1.2 Problem Statement")
    add_para(doc,
        "Conventional malicious URL detection mechanisms are fundamentally incapable of addressing modern web-borne threats due to critical structural "
        "deficiencies across velocity, accuracy, security, and trust. The core engineering problem addressed by this project can be formally stated "
        "across five distinct technical dimensions:")

    add_para(doc,
        "1. Zero-Hour Detection Latency: Static blacklists and signature-based scanning tools operate reactively, creating a vulnerability window of "
        "12 to 72 hours during which newly registered malicious domains and phishing sites operate with complete impunity [5].")

    add_para(doc,
        "2. Adversarial Evasion and Lexical Camouflage: Attackers systematically evade pattern-matching filters through typosquatting, brand impersonation, "
        "excessive entropy, path obfuscation, hex-encoding, and legitimate cloud hosting platforms (e.g., Firebase, GitHub Pages, Vercel), rendering "
        "simplistic rule-based inspection ineffective [6].")

    add_para(doc,
        "3. Lack of Explainability and Transparency: Emerging black-box deep learning models often output opaque risk probabilities without actionable "
        "evidence. Security analysts and end users are left without verifiable justifications, leading to alert fatigue or dangerous false dismissals.")

    add_para(doc,
        "4. Tamper Vulnerability and Centralized Data Monopoly: Existing commercial threat intelligence repositories operate as centralized black "
        "boxes. Threat data can be arbitrarily altered, censored, or retroactively falsified, preventing cross-organizational trust and cryptographic "
        "proof of historical detection verdicts.")

    add_para(doc,
        "5. Active Scanning Containment Risks: When security systems actively inspect suspicious URLs, they introduce severe security vulnerabilities "
        "into their own infrastructure, including Server-Side Request Forgery (SSRF) against internal metadata endpoints, container escapes, and "
        "malware contamination of operational hosts [7].")

    add_para(doc,
        "Therefore, the engineering challenge is to synthesize a high-throughput, low-latency, and tamper-resistant cybersecurity architecture "
        "capable of performing proactive, zero-hour malicious URL classification with sub-50ms inference latency, zero false alarms on legitimate "
        "corporate domains, cryptographically verifiable threat evidence, and complete isolation from active infrastructure threats.")

    # 1.3 Objective
    add_heading_2(doc, "1.3 Objective")
    add_para(doc,
        "The primary objective of the URLSentinel project is to design, engineer, evaluate, and deploy a production-grade, AI-powered cybersecurity "
        "platform that protects end users and enterprise systems against phishing and malicious web destinations through real-time multi-layered "
        "analysis and blockchain-backed threat intelligence. The specific technical objectives include:")

    add_para(doc,
        "• High-Performance Lexical Feature Engineering: Implement an ultra-fast feature extraction pipeline capable of parsing raw URLs into 25+ "
        "structural, lexical, and information-theoretic indicators (such as Shannon entropy, token depth, vowel-to-consonant ratios, and character "
        "frequencies) in sub-millisecond execution times.")

    add_para(doc,
        "• Resilient Multi-Layer AI Classification: Develop and calibrate machine learning classifiers (Ensemble Random Forest, Gradient Boosting, "
        "and Heuristic Tokenizers) capable of detecting obfuscated phishing attacks with >95% accuracy and an absolute 0.00% False Positive Rate on "
        "trusted enterprise infrastructure.")

    add_para(doc,
        "• Zero-False-Positive Brand Impersonation Defense: Engineer an algorithmic brand protection engine combining Levenshtein string distance, "
        "exact brand matching, and Public Suffix List (PSL) domain isolation to prevent spoofing of global brands (e.g., PayPal, Microsoft, Google, Apple).")

    add_para(doc,
        "• Explainable Bayesian Multi-Signal Risk Scoring: Aggregate independent signals—lexical heuristics, machine learning probabilities, live "
        "reputation feeds, DNS metadata, and SSL/TLS certificate indicators—into a normalized risk score (0 to 100) accompanied by plain-language "
        "explainability factors.")

    add_para(doc,
        "• Real-Time Chromium Manifest V3 Browser Extension: Construct a privacy-preserving browser extension that inspects web navigation hooks "
        "locally, queries cached verdicts, enforces sub-20ms policy enforcement, and intercepts malicious navigations before payload delivery.")

    add_para(doc,
        "• Tamper-Evident Blockchain Evidence Provenance: Establish a verifiable threat intelligence ledger where cryptographic hashes (SHA-256) of "
        "authoritative threat verdicts are anchored into a decentralized Merkle registry, guaranteeing immutable tamper evidence.")

    add_para(doc,
        "• Zero-Trust Sandboxed Scanning Boundary: Design an ephemeral, isolated container analysis environment equipped with non-root execution, "
        "read-only root filesystems, and strict egress firewall rules that neutralize SSRF vectors and protect internal service networks.")

    # 1.4 Scope of the Project
    add_heading_2(doc, "1.4 Scope of the Project")
    add_para(doc,
        "The architectural and operational scope of URLSentinel is structured to encompass both client-side protective agents and cloud-scale analytical "
        "backends. The project boundaries are formally delineated as follows:")

    add_para(doc,
        "In-Scope Functional Boundaries:\n"
        "1. Full-Stack Web Platform: A high-performance web dashboard developed with Next.js 14, React, and Tailwind CSS, featuring an enterprise dark-mode "
        "interface (FORTRESS v2.0 design system), dynamic SVG threat gauge telemetry, and interactive scan histories.\n"
        "2. Asynchronous REST API: A production-ready backend engineered with Python 3.12 and FastAPI, fully compliant with OpenAPI 3.1 standards, "
        "providing sub-millisecond payload routing, structured Pydantic v2 data models, and strict rate-limiting controls.\n"
        "3. Modular Detection Engine: A decoupled core library comprising lexical parsers, Shannon entropy calculators, Levenshtein brand comparators, "
        "DGA consonant counters, and pre-trained scikit-learn random forest ensembles.\n"
        "4. Threat Intelligence Feeds Integration: Automated ingestion pipelines supporting active community feeds (PhishTank, URLhaus, OpenPhish) "
        "with local TTL-governed cache storage.\n"
        "5. Manifest V3 Browser Protection: Chromium-compatible extension utilizing asynchronous webNavigation hooks, local storage caching, "
        "and client-side red-screen interstitial warning screens.\n"
        "6. Cryptographic Provenance Registry: Smart contract data models and Merkle tree hashing modules designed for verifiable threat registration.\n"
        "7. Comprehensive Quality & Test Suite: Full test coverage incorporating unit tests, adversarial payload suites, SSRF security validation, "
        "and 2,000-URL empirical evaluation benchmarks.")

    add_para(doc,
        "Out-of-Scope System Limitations:\n"
        "1. Native Operating System Binary Decompilation: The platform focuses specifically on URL navigation, domain intelligence, and web landing "
        "page analysis; native Windows/Linux PE binary disassembly or kernel-level memory exploitation analysis is out of scope.\n"
        "2. Public Mainnet Blockchain Gas Expenditure: To prevent prohibitive financial overhead, on-chain transactions are demonstrated on a local "
        "Ethereum Virtual Machine (EVM) testnet environment rather than public Ethereum/Polygon mainnet.\n"
        "3. Core Browser Engine Source Modification: The system operates strictly via standard W3C WebExtension APIs without patching underlying C++ "
        "rendering engines in Chromium or Gecko.")

    # 1.5 Overview of the System
    add_heading_2(doc, "1.5 Overview of the System")
    add_para(doc,
        "The URLSentinel platform operates as an integrated, multi-tier defense ecosystem designed to intercept, analyze, classify, and record "
        "suspicious web destinations before user compromise can occur. The system operates across four primary operational tiers:")

    add_para(doc,
        "1. Ingestion Tier: Receives URL evaluation requests across three distinct access channels: the Next.js FORTRESS web application, automated "
        "programmatic clients via the FastAPI REST gateway, and real-time navigation events from the Chromium Manifest V3 browser extension. "
        "Input requests undergo immediate RFC 3986 normalization, UTF-8 punycode decoding, and structural sanity checks.")

    add_para(doc,
        "2. Analytical & Feature Extraction Tier: Once normalized, the URL is processed concurrently by the Feature Extraction Pipeline. The system "
        "extracts 25+ lexical and structural features, evaluates Shannon entropy across domain and path tokens, computes Levenshtein distances against "
        "an indexed catalog of global financial and technology brands, and calculates consonant-to-vowel distribution ratios to identify algorithmic domain generation.")

    add_para(doc,
        "3. Multi-Signal Risk Engine & Intelligence Tier: Feature vectors are supplied to a pre-trained Ensemble Random Forest classifier to generate "
        "a baseline statistical threat probability. Simultaneously, local threat feeds and reputation databases are queried in parallel. The Risk Engine "
        "applies calibrated Bayesian aggregation rules to synthesize these heterogeneous inputs into a definitive risk verdict (SAFE, ELEVATED, "
        "SUSPICIOUS, MALICIOUS), a normalized score (0–100), and a structured array of human-readable explanation factors.")

    add_para(doc,
        "4. Isolation & Verification Tier: When active page inspection is required, untrusted targets are dispatched to an isolated container sandbox "
        "operating behind zero-trust egress firewall rules, preventing internal network enumeration. Finally, the authoritative scan verdict, "
        "timestamp, and feature hash are combined into a canonical SHA-256 evidence digest, ready for immutable anchoring on the cryptographic "
        "blockchain registry.")

    add_para(doc,
        "The subsequent chapters of this report present an exhaustive literature review of contemporary threat detection research (Chapter 2), "
        "formal system analysis and requirements modeling (Chapter 3), mathematical and architectural methodology (Chapter 4), comprehensive "
        "system design diagrams (Chapter 5), detailed technical implementation and algorithmic specifications (Chapter 6), rigorous verification "
        "and test suite results (Chapter 7), development challenges and architectural limitations (Chapter 8), empirical performance analysis across "
        "2,000 real-world benchmark URLs (Chapter 9), and concluding remarks with future research horizons (Chapter 10).")

    doc.add_page_break()
    print("Chapter 1 built successfully.")
