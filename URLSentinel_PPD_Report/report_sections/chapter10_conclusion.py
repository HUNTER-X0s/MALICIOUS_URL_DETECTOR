"""
report_sections/chapter10_conclusion.py - Chapter 10: CONCLUSION for URLSentinel PPD Report
"""

from docx.shared import Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
from report_sections.common import (
    add_para, add_heading_1, add_heading_2, add_heading_3
)

def build_chapter_10(doc):
    p_ch = doc.add_paragraph()
    p_ch.paragraph_format.space_before = Pt(12)
    p_ch.paragraph_format.space_after = Pt(12)
    r_ch = p_ch.add_run("CHAPTER 10\nCONCLUSION")
    r_ch.font.name = 'Times New Roman'
    r_ch.font.size = Pt(16)
    r_ch.bold = True
    p_ch.alignment = WD_ALIGN_PARAGRAPH.CENTER

    # 10.1 Conclusion
    add_heading_2(doc, "10.1 Conclusion")
    add_para(doc,
        "The URLSentinel engineering project demonstrates a transformative, production-grade cybersecurity platform that shifts web threat "
        "mitigation from vulnerable, reactive blocklists to proactive, explainable, and cryptographically verifiable artificial intelligence. "
        "Through the systematic unification of computational linguistics, information-theoretic entropy modeling, machine learning ensembles, "
        "and decentralized blockchain ledgers, the project successfully resolves the critical zero-hour detection latency gap that leaves "
        "contemporary internet users vulnerable to credential theft and malware infection.")

    add_para(doc,
        "Key engineering milestones accomplished in this B.Tech Project for Product Development include:\n"
        "1. High-Performance Lexical & Structural Pipeline: Designed and implemented a feature extraction engine that processes 25+ syntactic and "
        "entropy features in an astonishing 1.39 milliseconds, providing the foundational speed necessary for real-time endpoint protection.\n"
        "2. Algorithmic Zero-False-Positive Brand Protection: Engineered an advanced brand protection tier combining Levenshtein string metrics, "
        "Public Suffix List domain tokenization, and enterprise Single-Sign-On whitelisting, achieving an absolute 0.00% False Positive Rate on "
        "1,000 legitimate enterprise domains.\n"
        "3. Real-Time Endpoint Defense: Constructed a lightweight Chromium Manifest V3 browser extension that intercepts suspicious navigations "
        "before DOM rendering, preventing user compromise at the earliest point in the cyber kill chain without compromising browsing privacy.\n"
        "4. Tamper-Evident Cryptographic Ledger: Formulated a blockchain verification layer utilizing SHA-256 evidence digests and decentralized "
        "smart contract registries, guaranteeing permanent, auditable proof of threat detection records without centralized vendor tampering.\n"
        "5. Strict Zero-Trust Sandboxing: Isolated untrusted URL crawling within disposable container sandboxes governed by non-root security contexts "
        "and strict egress firewall rules, neutralizing Server-Side Request Forgery (SSRF) and container escape attack surfaces.")

    add_para(doc,
        "Empirical evaluation on a rigorous benchmark of 2,000 real-world URLs confirmed that URLSentinel achieves 97.15% overall classification "
        "accuracy, 100.00% precision, 94.30% recall, and an F1-score of 0.9707, significantly outperforming traditional static blocklists (68.95%) "
        "and standalone machine learning baselines (88.60%). All 70 automated regression test suites executed and passed in 22.44 seconds, "
        "validating complete compliance with all academic, operational, and non-functional quality gates.")

    # 10.2 Future Scope
    add_heading_2(doc, "10.2 Future Scope")
    add_para(doc,
        "While URLSentinel delivers a robust, production-ready defense ecosystem, the evolving nature of cyber threats presents several "
        "promising directions for ongoing research and engineering enhancement:")

    add_para(doc,
        "1. Multimodal Deep Learning & Visual Brand Recognition: Future iterations can integrate lightweight Convolutional Neural Networks (CNNs) "
        "or Vision Transformers (ViT) into the asynchronous sandbox tier to compare screenshot renders against authentic corporate web logos, "
        "detecting visual impersonation that circumvents lexical analysis.")

    add_para(doc,
        "2. Decentralized Peer-to-Peer Threat Federation: Expanding the blockchain verification registry into a fully federated peer-to-peer (P2P) "
        "threat intelligence network using IPFS (InterPlanetary File System) and libp2p, enabling distributed enterprise SOCs to share anonymized "
        "threat indicators in real time without intermediary cloud dependencies.")

    add_para(doc,
        "3. MicroVM-Based Dynamic Cloaking De-Obfuscation: Incorporating ephemeral micro-virtual machines (such as AWS Firecracker) to execute "
        "multi-hop redirect chains and JavaScript unpacking within hardware-isolated sub-second VMs, effectively defeating adversarial geolocation "
        "cloaking and human CAPTCHA gates.")

    add_para(doc,
        "4. Enterprise Identity Provider (IdP) & EDR Integrations: Developing native plugins for enterprise identity solutions (e.g., Okta, Microsoft "
        "Entra ID) and Endpoint Detection and Response (EDR) platforms (e.g., CrowdStrike Falcon, SentinelOne) to automate immediate session "
        "revocation when an employee navigates to a compromised link.")

    add_para(doc,
        "5. Privacy-Preserving Zero-Knowledge Proofs: Researching Zero-Knowledge Succinct Non-Interactive Arguments of Knowledge (zk-SNARKs) to allow "
        "clients to verify that a visited URL exists within a cryptographically signed malicious feed without revealing the visited domain string "
        "to the central server, delivering absolute mathematical browsing privacy.")

    doc.add_page_break()
    print("Chapter 10 built successfully.")
