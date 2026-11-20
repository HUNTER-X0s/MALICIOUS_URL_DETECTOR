"""
final_sections/ch1_intro.py - 1. INTRODUCTION (Target: 3 pages, pp. 1-3)
"""

from docx.shared import Inches, Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
from report_sections.common import (
    add_para, add_bullet
)

def build_ch1(doc):
    # 1. INTRODUCTION
    p_h = doc.add_paragraph()
    p_h.paragraph_format.space_before = Pt(0)
    p_h.paragraph_format.space_after = Pt(10)
    p_h.paragraph_format.keep_with_next = True
    r = p_h.add_run("1. INTRODUCTION")
    r.font.name = 'Times New Roman'
    r.font.size = Pt(20)
    r.bold = True

    add_para(doc,
        "The exponential expansion of digital services, cloud applications, and e-commerce has made the World Wide Web "
        "indispensable to global commerce and daily communication. However, this ubiquity has established web navigation as the "
        "primary attack vector for cyber adversaries. Malicious URLs serve as the foundational delivery mechanism for credential "
        "harvesting, financial fraud, malware distribution, and social engineering attacks. According to reports by the Anti-Phishing "
        "Working Group (APWG) and CISA, web-borne attacks account for over 70% of enterprise security breaches annually [1], [2]. "
        "Traditional web security mechanisms rely on centralized blacklists, which suffer from a severe zero-hour detection lag, "
        "taking 12 to 72 hours to ingest newly generated domains. This project presents URLSentinel, an AI-powered cybersecurity "
        "platform combining real-time machine learning, threat intelligence, and blockchain-backed evidence verification to "
        "provide proactive, zero-hour protection against malicious URLs.")

    # 1.1 Motivation
    p_sub = doc.add_paragraph()
    p_sub.paragraph_format.space_before = Pt(8)
    p_sub.paragraph_format.space_after = Pt(4)
    p_sub.paragraph_format.keep_with_next = True
    r = p_sub.add_run("1.1 Motivation")
    r.font.name = 'Times New Roman'
    r.font.size = Pt(16)
    r.bold = True

    add_para(doc,
        "The contemporary threat landscape is characterized by rapid evasion tactics deployed by automated threat actor toolkits. "
        "Attackers routinely deploy Domain Generation Algorithms (DGA), fast-flux DNS networks, and automated phishing toolkits that "
        "spin up malicious landing pages within seconds. Research indicates that over 65% of malicious URLs remain active for less than "
        "eight hours, disappearing long before static blacklists and reputation databases ingest them [3], [4]. As a result, users "
        "navigating the web during this critical zero-hour window remain entirely unprotected by conventional reputation systems.")

    add_para(doc,
        "Furthermore, modern phishing attacks exploit sophisticated psychological and visual deception. Adversaries register typosquatted "
        "domains that visually mimic authentic brands (e.g., 'paypa1.com' or 'rnicrosoft.com') or utilize Internationalized Domain Name (IDN) "
        "homoglyph attacks where Latin characters are substituted with visually identical Cyrillic glyphs [10], [11]. In addition, attackers "
        "frequently abuse legitimate cloud hosting services (such as Firebase, GitHub Pages, and Cloudflare Pages) to camouflage malicious forms "
        "under reputable apex domains [13]. These realities establish a compelling motivation to construct an intelligent endpoint defense platform "
        "capable of extracting lexical, information-theoretic, and behavioral features in real time, issuing calibrated verdicts in under "
        "two milliseconds, and anchoring threat evidence into a decentralized ledger for tamper-evident auditability.")

    # 1.2 Problem Statement
    p_sub = doc.add_paragraph()
    p_sub.paragraph_format.space_before = Pt(8)
    p_sub.paragraph_format.space_after = Pt(4)
    p_sub.paragraph_format.keep_with_next = True
    r = p_sub.add_run("1.2 Problem Statement")
    r.font.name = 'Times New Roman'
    r.font.size = Pt(16)
    r.bold = True

    add_para(doc,
        "Existing malicious URL detection systems face severe systemic challenges that limit their effectiveness in real-world environments. "
        "The core technical problems addressed in this project are identified as follows:")

    add_bullet("Zero-Hour Detection Lag: Static blocklists and reputation feeds operate reactively, creating a vulnerability window of 12 to 72 hours during which newly registered malicious domains operate undetected [5].")
    add_bullet("Adversarial Obfuscation: Attackers bypass signature-based filters using typosquatting, character encoding, URL shorteners, and randomized high-entropy token strings [6], [10].")
    add_bullet("Opaque Black-Box Classifiers: Deep learning classifiers often output raw probabilities without explainable justifications, causing user confusion and alert fatigue among SOC analysts.")
    add_bullet("Centralized Tamper Vulnerability: Conventional threat intelligence databases are centralized, making detection records vulnerable to retroactive modification, deletion, or dispute.")
    add_bullet("Scanning Infrastructure Risk: Active webpage crawlers introduce significant vulnerability surfaces, particularly Server-Side Request Forgery (SSRF) against internal cloud metadata endpoints [7].")

    add_para(doc,
        "Therefore, there is an urgent need for an integrated cybersecurity platform that combines sub-millisecond lexical feature extraction, "
        "calibrated machine learning ensembles, real-time browser interception, and decentralized cryptographic evidence verification while "
        "enforcing strict zero-trust sandbox isolation.")

    # 1.3 Objective
    p_sub = doc.add_paragraph()
    p_sub.paragraph_format.space_before = Pt(8)
    p_sub.paragraph_format.space_after = Pt(4)
    p_sub.paragraph_format.keep_with_next = True
    r = p_sub.add_run("1.3 Objective")
    r.font.name = 'Times New Roman'
    r.font.size = Pt(16)
    r.bold = True

    add_para(doc, "The primary objectives of the URLSentinel project are:")
    add_bullet("To develop a high-throughput, low-latency URL evaluation pipeline that extracts 25+ lexical and structural features within 1.5 milliseconds.")
    add_bullet("To implement an algorithmic brand protection engine utilizing Levenshtein distance and Public Suffix List (PSL) tokenization to detect typosquatting with zero false alarms on enterprise portals.")
    add_bullet("To train and calibrate an Ensemble Random Forest classifier capable of detecting obfuscated phishing attacks with >95% accuracy.")
    add_bullet("To engineer a lightweight Chromium Manifest V3 browser extension that intercepts suspicious navigations in real time before page DOM execution.")
    add_bullet("To establish an immutable blockchain evidence ledger using SHA-256 digests and EVM smart contracts to guarantee tamper-evident auditability.")
    add_bullet("To enforce strict zero-trust sandboxing with egress firewall rules preventing SSRF attacks on scanning infrastructure.")

    # 1.4 Scope of the Project
    p_sub = doc.add_paragraph()
    p_sub.paragraph_format.space_before = Pt(8)
    p_sub.paragraph_format.space_after = Pt(4)
    p_sub.paragraph_format.keep_with_next = True
    r = p_sub.add_run("1.4 Scope of the Project")
    r.font.name = 'Times New Roman'
    r.font.size = Pt(16)
    r.bold = True

    add_para(doc,
        "The project scope encompasses the design, implementation, and empirical verification of a complete client-server cybersecurity platform. "
        "The system incorporates:")
    add_bullet("Web Application Layer: A responsive Next.js 14 dashboard providing URL submission, dynamic SVG threat gauges, and scan histories.")
    add_bullet("REST API Gateway: An asynchronous FastAPI backend providing OpenAPI-compliant endpoints with sub-50ms round-trip latency.")
    add_bullet("Analytical Core: In-memory lexical parsers, Shannon entropy calculators, Levenshtein brand comparators, and DGA consonant evaluators.")
    add_bullet("Threat Intelligence Layer: Automated synchronization of active community feeds (URLhaus, OpenPhish) with local TTL caching.")
    add_bullet("Endpoint Protection Layer: A Chromium Manifest V3 extension featuring webNavigation listeners and interstitial warning screens.")
    add_bullet("Cryptographic Layer: SHA-256 evidence hashing and EVM smart contract interfaces for decentralized verdict anchoring.")

    add_para(doc,
        "Out of scope: Native binary payload disassembly and public mainnet Ethereum gas expenditures (simulated on local EVM testnets).")

    # 1.5 Overview of the System
    p_sub = doc.add_paragraph()
    p_sub.paragraph_format.space_before = Pt(8)
    p_sub.paragraph_format.space_after = Pt(4)
    p_sub.paragraph_format.keep_with_next = True
    r = p_sub.add_run("1.5 Overview of the System")
    r.font.name = 'Times New Roman'
    r.font.size = Pt(16)
    r.bold = True

    add_para(doc,
        "URLSentinel operates as an integrated, multi-tier defense ecosystem. When a URL is submitted via the web dashboard, API, or browser extension, "
        "it is first canonicalized according to RFC 3986, stripping redundant ports and decoding Punycode. The URL is then checked against an in-memory "
        "cache and verified Single-Sign-On (SSO) whitelist. Uncached URLs undergo parallel processing: the lexical engine extracts 25+ features "
        "and computes Shannon entropy; the ML classifier evaluates decision trees; and the threat intelligence service queries local feed hashes. "
        "The Bayesian Risk Engine synthesizes these signals into a calibrated risk score (0 to 100) and categorical verdict (SAFE, ELEVATED, "
        "SUSPICIOUS, MALICIOUS) with plain-language explanations. Finally, a SHA-256 evidence digest is anchored to the blockchain registry for "
        "tamper-evident verification.")

    doc.add_page_break()
    print("Chapter 1 built (pages 1-3).")
