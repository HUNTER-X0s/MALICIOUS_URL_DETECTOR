"""
final_sections/ch10_conclusion.py - 10. CONCLUSION (Target: 1 page, p. 33)
"""

from docx.shared import Inches, Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
from report_sections.common import (
    add_para, add_bullet
)

def build_ch10(doc):
    # 10. CONCLUSION
    p_h = doc.add_paragraph()
    p_h.paragraph_format.space_before = Pt(0)
    p_h.paragraph_format.space_after = Pt(10)
    p_h.paragraph_format.keep_with_next = True
    r = p_h.add_run("10. CONCLUSION")
    r.font.name = 'Times New Roman'
    r.font.size = Pt(20)
    r.bold = True

    # 10.1 Conclusion
    p_sub = doc.add_paragraph()
    p_sub.paragraph_format.space_before = Pt(6)
    p_sub.paragraph_format.space_after = Pt(4)
    p_sub.paragraph_format.keep_with_next = True
    r = p_sub.add_run("10.1 Conclusion")
    r.font.name = 'Times New Roman'
    r.font.size = Pt(16)
    r.bold = True

    add_para(doc,
        "The URLSentinel platform implements an enterprise-grade cybersecurity system that transitions "
        "malicious URL protection from vulnerable, reactive blacklists to proactive, explainable, and "
        "cryptographically verifiable artificial intelligence. By synthesizing computational linguistics, "
        "Shannon entropy modeling, supervised machine learning ensembles, and decentralized blockchain "
        "registries, the platform resolves the zero-hour detection latency gap that leaves contemporary web "
        "users vulnerable to credential theft and malware.",
        align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=4, font_size=11)

    add_para(doc,
        "Key engineering milestones accomplished in this B.Tech Project for Product Development include:",
        align=WD_ALIGN_PARAGRAPH.LEFT, space_before=2, space_after=2, font_size=11)

    add_bullet(doc, "High-Performance Lexical Pipeline: Extracts 25+ syntactic metrics and Shannon entropy in an ultra-fast 1.39 ms.")
    add_bullet(doc, "Algorithmic Brand Protection Engine: Achieved 0.00% False Positive Rate on 1,000 corporate Single-Sign-On URLs.")
    add_bullet(doc, "Lightweight Chromium Manifest V3 Extension: Delivers real-time endpoint interception without browsing latency.")
    add_bullet(doc, "Immutable Blockchain Evidence Ledger: Anchors SHA-256 digests to EVM smart contracts for tamper-evident provenance.")
    add_bullet(doc, "Strict Zero-Trust Sandbox Isolation: Prevents SSRF attacks and container escapes during active dynamic crawls.")

    add_para(doc,
        "Comprehensive empirical evaluation on 2,000 real-world benchmark URLs demonstrated 97.15% classification "
        "accuracy, 100.00% precision, 94.30% recall, and a 0.9707 F1-score, significantly outperforming "
        "static community blacklists (68.95%) and baseline ML models (88.60%). All 70 automated regression "
        "test suites passed in 22.44 seconds, confirming complete compliance with all architectural quality gates.",
        align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_before=4, space_after=6, font_size=11)

    # 10.2 Future Scope
    p_sub2 = doc.add_paragraph()
    p_sub2.paragraph_format.space_before = Pt(6)
    p_sub2.paragraph_format.space_after = Pt(2)
    p_sub2.paragraph_format.keep_with_next = True
    r2 = p_sub2.add_run("10.2 Future Scope")
    r2.font.name = 'Times New Roman'
    r2.font.size = Pt(16)
    r2.bold = True

    add_para(doc,
        "Future research and engineering enhancements for URLSentinel include: (1) Multimodal Deep Learning, "
        "integrating lightweight Vision Transformers into the sandbox tier to compare rendered screenshots against authentic corporate logos; "
        "(2) Peer-to-Peer Threat Federation, expanding the smart contract registry into an IPFS-backed libp2p network for decentralized cross-organizational threat intelligence sharing; "
        "(3) MicroVM Sandboxing, deploying AWS Firecracker microVMs for safe hardware-isolated redirect execution; (4) Enterprise IdP and EDR Integrations, "
        "connecting to Okta and CrowdStrike APIs for automated session termination upon threat detection; and (5) Zero-Knowledge Proofs "
        "(zk-SNARKs), enabling clients to verify threat feed membership with absolute cryptographic browsing privacy.",
        align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_before=2, space_after=4, font_size=11)

    doc.add_page_break()
    print("Chapter 10 built (page 33).")
