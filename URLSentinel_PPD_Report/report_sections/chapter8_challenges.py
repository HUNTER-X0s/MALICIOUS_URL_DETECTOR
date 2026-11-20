"""
report_sections/chapter8_challenges.py - Chapter 8: CHALLENGES AND LIMITATIONS for URLSentinel PPD Report
"""

from docx.shared import Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
from report_sections.common import (
    add_para, add_heading_1, add_heading_2, add_heading_3
)

def build_chapter_8(doc):
    p_ch = doc.add_paragraph()
    p_ch.paragraph_format.space_before = Pt(12)
    p_ch.paragraph_format.space_after = Pt(12)
    r_ch = p_ch.add_run("CHAPTER 8\nCHALLENGES AND LIMITATIONS")
    r_ch.font.name = 'Times New Roman'
    r_ch.font.size = Pt(16)
    r_ch.bold = True
    p_ch.alignment = WD_ALIGN_PARAGRAPH.CENTER

    # 8.1 Challenges Faced During Development
    add_heading_2(doc, "8.1 Challenges Faced During Development")
    add_para(doc,
        "Engineering an enterprise-grade cybersecurity platform that unifies real-time machine learning, low-latency endpoint protection, "
        "and cryptographic ledger verification presented numerous complex technical challenges. Documenting these hurdles provides "
        "valuable insight into the design trade-offs and engineering solutions implemented in URLSentinel:")

    add_para(doc,
        "1. Public Suffix List (PSL) Lookup Latency: Identifying the true registrable domain (e.g., distinguishing 'co.uk' from 'example.co.uk') "
        "is essential for brand protection. Initial implementations that parsed raw PSL text files on disk incurred prohibitive latency (~45 ms per scan). "
        "To resolve this bottleneck, the engine was refactored to compile the Public Suffix rules into an in-memory prefix trie during application startup, "
        "reducing domain resolution latency to under 0.05 milliseconds.")

    add_para(doc,
        "2. Chromium Manifest V3 Background Lifecycle Constraints: Under Google Chrome's Manifest V3 specification, persistent background pages "
        "are deprecated in favor of ephemeral Service Workers that terminate after 30 seconds of inactivity. In-memory threat caches were frequently "
        "evicted, causing cold-start lookup delays. The engineering solution required architecting a two-tier storage model: using `chrome.storage.local` "
        "for persistent cross-lifecycle caching while maintaining an in-memory WeakMap during active navigation events, guaranteeing zero dropped interceptions.")

    add_para(doc,
        "3. Safe Handling of Opaque URL Shorteners: URL shortening services (e.g., bit.ly, tinyurl.com, t.co) inherently conceal the destination "
        "resource behind HTTP 301/302 redirects. Actively following redirect chains on behalf of users introduces significant security risks: "
        "adversaries can track analyst IP addresses, fingerprint server environments, or trigger Server-Side Request Forgery (SSRF). URLSentinel "
        "resolved this challenge by implementing an invariant bounding rule: unexpanded shorteners are explicitly bounded to an ELEVATED risk "
        "classification accompanied by a transparent user advisory, informing the user that the true destination is camouflaged, rather than guessing "
        "or executing dangerous unconstrained network fetches.")

    add_para(doc,
        "4. Adversarial Subdomain Camouflage on Legitimate Multi-Tenant Cloud Hosts: Modern threat actors routinely abuse reputable cloud developer "
        "platforms (e.g., firebaseapp.com, pages.dev, workers.dev, github.io) to host credential-harvesting forms. Because the apex domain possesses "
        "an immaculate global reputation, standard domain reputation checks fail completely. To counter this evasion, URLSentinel's feature extractor "
        "was updated to tokenize beyond the registrable apex, analyzing full subdomain depth, path keyword tokens ('login', 'verify'), and entropy "
        "specifically on the tenant subdomain.")

    add_para(doc,
        "5. Host Isolation and SSRF Containment in Scanning Infrastructure: Building a dynamic scanning sandbox on commodity hardware without exposing "
        "the host operating system to malware payloads or internal network scanning required strict containment. This was solved by containerizing the "
        "crawler within disposable Docker containers running with non-root privileges (UID 10001), a read-only root filesystem (`read_only: true`), "
        "and host-level iptables firewall rules that drop all egress traffic directed toward RFC 1918 private subnets and AWS metadata (169.254.169.254).")

    # 8.2 Limitations of the System
    add_heading_2(doc, "8.2 Limitations of the System")
    add_para(doc,
        "In accordance with rigorous academic integrity and cybersecurity engineering principles, URLSentinel acknowledges specific operational "
        "and architectural boundaries that delineate its current capabilities:")

    add_para(doc,
        "1. Inherent Inability to Inspect Post-Navigation Dynamic DOM Injections via Static Analysis: Static lexical and heuristic analysis evaluates "
        "the URL string itself; it cannot inspect malicious JavaScript payloads dynamically injected into the browser DOM via client-side WebSockets "
        "or delayed timers after initial navigation has completed, unless the heavier, asynchronous sandbox container crawler is explicitly dispatched.")

    add_para(doc,
        "2. Threat Intelligence Feed Update Frequency and Freshness Lag: While community threat feeds (URLhaus, OpenPhish, PhishTank) provide invaluable "
        "confirmed threat intelligence, their ingestion frequencies are governed by third-party update intervals (typically 30 to 60 minutes). "
        "During the first few minutes of an entirely novel campaign, the platform relies primarily on the machine learning and heuristic engines.")

    add_para(doc,
        "3. Financial and Throughput Overhead of Public Mainnet Blockchains: Anchoring cryptographic evidence hashes directly into a public Layer-1 "
        "blockchain (e.g., Ethereum Mainnet) incurs volatile transaction gas fees and block confirmation latencies (12–15 seconds), which is "
        "impractical for high-frequency individual scans. Consequently, URLSentinel's current production design utilizes local EVM networks, "
        "Layer-2 rollup testnets, and Merkle tree batching to maintain zero-cost cryptographic provenance.")

    add_para(doc,
        "4. Cloaked and Adversarially Geofenced Targets: Highly sophisticated phishing kits deploy anti-analysis cloaking mechanisms that inspect "
        "the client's IP geolocation, browser canvas fingerprints, or require human CAPTCHA interaction. If an automated sandbox crawler accesses "
        "such a URL, the malicious server may return a benign 404 page, concealing its true payload. Combining client-side browser extension telemetry "
        "with server-side scanning partially mitigates this limitation.")

    doc.add_page_break()
    print("Chapter 8 built successfully.")
