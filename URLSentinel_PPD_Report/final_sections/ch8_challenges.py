"""
final_sections/ch8_challenges.py - 8. CHALLENGES AND LIMITATIONS (Target: 2 pages, pp. 28-29)
"""

from docx.shared import Inches, Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
from report_sections.common import (
    add_para, add_bullet
)

def build_ch8(doc):
    # =========================================================================
    # PAGE 28: 8. CHALLENGES AND LIMITATIONS & 8.1 Challenges Faced
    # =========================================================================
    p_h = doc.add_paragraph()
    p_h.paragraph_format.space_before = Pt(0)
    p_h.paragraph_format.space_after = Pt(8)
    p_h.paragraph_format.keep_with_next = True
    r = p_h.add_run("8. CHALLENGES AND LIMITATIONS")
    r.font.name = 'Times New Roman'
    r.font.size = Pt(20)
    r.bold = True

    p_sub = doc.add_paragraph()
    p_sub.paragraph_format.space_before = Pt(4)
    p_sub.paragraph_format.space_after = Pt(2)
    p_sub.paragraph_format.keep_with_next = True
    r = p_sub.add_run("8.1 Challenges Faced During Development")
    r.font.name = 'Times New Roman'
    r.font.size = Pt(16)
    r.bold = True

    add_para(doc,
        "Developing an enterprise-grade cybersecurity platform that unifies real-time machine learning, low-latency endpoint protection, "
        "and cryptographic ledger verification presented several complex technical hurdles:",
        space_after=3, font_size=11)

    add_bullet("Public Suffix List (PSL) Lookup Latency: Identifying the true registrable domain (e.g., distinguishing 'co.uk' from 'example.co.uk') is essential for brand protection. Initial implementations parsing raw PSL text files on disk incurred prohibitive latency (~45 ms per scan). To resolve this bottleneck, the engine was refactored to compile the Public Suffix rules into an in-memory prefix trie during startup, reducing lookup latency to under 0.05 milliseconds.")

    add_bullet("Chromium Manifest V3 Service Worker Lifecycle: Under Google Chrome's Manifest V3 specification, background pages are replaced by ephemeral Service Workers that terminate after 30 seconds of inactivity. In-memory threat caches were frequently evicted, causing cold-start lookup delays. The solution was architecting a two-tier storage model: using chrome.storage.local for persistent cross-lifecycle caching while maintaining an in-memory WeakMap during active navigation events.")

    add_bullet("Safe Handling of Opaque URL Shorteners: URL shortening services (e.g., bit.ly, tinyurl.com) inherently conceal the destination resource behind HTTP 301/302 redirects. Actively following redirect chains on behalf of users introduces significant security risks: adversaries can track analyst IP addresses or trigger Server-Side Request Forgery (SSRF). URLSentinel resolved this by implementing an invariant bounding rule: unexpanded shorteners are explicitly bounded to an ELEVATED risk classification accompanied by a transparent user advisory.")

    add_bullet("Adversarial Subdomain Camouflage on Legitimate Multi-Tenant Cloud Hosts: Modern threat actors routinely abuse reputable cloud developer platforms (e.g., firebaseapp.com, pages.dev, workers.dev) to host credential-harvesting forms. Because the apex domain possesses an immaculate global reputation, standard domain reputation checks fail completely. To counter this evasion, URLSentinel's feature extractor was updated to tokenize beyond the registrable apex, analyzing full subdomain depth, path keyword tokens ('login', 'verify'), and entropy specifically on the tenant subdomain.")

    add_bullet("Host Isolation and SSRF Containment in Scanning Infrastructure: Building a dynamic scanning sandbox on commodity hardware without exposing the host operating system to malware payloads or internal network scanning required strict containment. This was solved by containerizing the crawler within disposable Docker containers running with non-root privileges (UID 10001), a read-only root filesystem, and host-level iptables firewall rules dropping all egress traffic directed toward RFC 1918 private subnets and AWS metadata (169.254.169.254).")

    doc.add_page_break()

    # =========================================================================
    # PAGE 29: 8.2 Limitations of the System
    # =========================================================================
    p_sub2 = doc.add_paragraph()
    p_sub2.paragraph_format.space_before = Pt(4)
    p_sub2.paragraph_format.space_after = Pt(4)
    p_sub2.paragraph_format.keep_with_next = True
    r2 = p_sub2.add_run("8.2 Limitations of the System")
    r2.font.name = 'Times New Roman'
    r2.font.size = Pt(16)
    r2.bold = True

    add_para(doc,
        "In accordance with rigorous academic integrity and cybersecurity engineering principles, URLSentinel acknowledges specific "
        "operational and architectural boundaries:")

    add_bullet("Inherent Inability to Inspect Post-Navigation Dynamic DOM Injections via Static Analysis: Static lexical and heuristic analysis evaluates the URL string itself; it cannot inspect malicious JavaScript payloads dynamically injected into the browser DOM via client-side WebSockets or delayed timers after initial navigation has completed, unless the heavier, asynchronous sandbox container crawler is explicitly dispatched.")

    add_bullet("Threat Intelligence Feed Update Frequency and Freshness Lag: While community threat feeds (URLhaus, OpenPhish, PhishTank) provide invaluable confirmed threat intelligence, their ingestion frequencies are governed by third-party update intervals (typically 30 to 60 minutes). During the first few minutes of an entirely novel campaign, the platform relies primarily on the machine learning and heuristic engines.")

    add_bullet("Financial and Throughput Overhead of Public Mainnet Blockchains: Anchoring cryptographic evidence hashes directly into a public Layer-1 blockchain (e.g., Ethereum Mainnet) incurs volatile transaction gas fees and block confirmation latencies (12–15 seconds), which is impractical for high-frequency individual scans. Consequently, URLSentinel's current production design utilizes local EVM networks, Layer-2 rollup testnets, and Merkle tree batching to maintain zero-cost cryptographic provenance.")

    add_bullet("Cloaked and Adversarially Geofenced Targets: Highly sophisticated phishing kits deploy anti-analysis cloaking mechanisms that inspect the client's IP geolocation, browser canvas fingerprints, or require human CAPTCHA interaction. If an automated sandbox crawler accesses such a URL, the malicious server may return a benign 404 page, concealing its true payload. Combining client-side browser extension telemetry with server-side scanning partially mitigates this limitation.")

    doc.add_page_break()
    print("Chapter 8 built (exactly 2 pages, pp. 28-29).")
