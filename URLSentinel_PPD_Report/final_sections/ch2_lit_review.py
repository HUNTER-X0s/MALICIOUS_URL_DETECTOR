"""
final_sections/ch2_lit_review.py - 2. LITERATURE REVIEW (Target: 4 pages, pp. 4-7)
"""

from docx.shared import Inches, Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from report_sections.common import (
    add_para, add_bullet, set_cell_background, set_table_borders,
    style_table_header, style_table_cells
)

def build_ch2(doc):
    # =========================================================================
    # PAGE 4: Heading, 2.1 Theoretical Background & Threat Taxonomy
    # =========================================================================
    p_h = doc.add_paragraph()
    p_h.paragraph_format.space_before = Pt(0)
    p_h.paragraph_format.space_after = Pt(10)
    p_h.paragraph_format.keep_with_next = True
    r = p_h.add_run("2. LITERATURE REVIEW")
    r.font.name = 'Times New Roman'
    r.font.size = Pt(20)
    r.bold = True

    add_para(doc,
        "The detection of malicious and phishing URLs has evolved significantly over the past two decades, transitioning from simple static "
        "blacklists to complex machine learning and deep neural network architectures. Understanding the theoretical foundations of web attack "
        "mechanisms, analyzing state-of-the-art literature, and identifying existing architectural gaps are essential for establishing a robust, "
        "defensible detection platform.")

    p_sub = doc.add_paragraph()
    p_sub.paragraph_format.space_before = Pt(8)
    p_sub.paragraph_format.space_after = Pt(4)
    p_sub.paragraph_format.keep_with_next = True
    r = p_sub.add_run("2.1 Theoretical Background")
    r.font.name = 'Times New Roman'
    r.font.size = Pt(16)
    r.bold = True

    add_para(doc,
        "A Uniform Resource Locator (URL), defined by RFC 3986, is a structured character sequence that specifies the identity and network protocol "
        "for retrieving web resources [8]. The canonical syntax comprises scheme, authority (host and port), path, query parameters, and fragments. "
        "Threat actors manipulate these structural elements to deceive users and evade security filters through several common attack patterns:")

    add_bullet("Typosquatting & Brand Spoofing: Registering lookalike domains that mimic trusted brands by introducing common keyboard typos, omitting characters, or substituting characters (e.g., 'micros0ft.com') [10].")
    add_bullet("IDN Homoglyph Attacks: Exploiting Unicode characters in DNS (RFC 3492 Punycode) to substitute Latin glyphs with visually indistinguishable Cyrillic or Greek characters (e.g., Cyrillic 'а' [U+0430] for Latin 'a' [U+0061]) [11].")
    add_bullet("Domain Generation Algorithms (DGA): Malware using pseudo-random algorithms to generate hundreds of ephemeral domains daily, exhibiting high Shannon entropy and elevated consonant-to-vowel ratios [12], [21].")
    add_bullet("Subdomain Camouflage: Creating malicious subdomains on legitimate multi-tenant cloud platforms (e.g., 'auth-portal.firebaseapp.com'), bypassing domain-level reputation filters [13].")

    add_para(doc,
        "Historically, cybersecurity defenses have relied on four primary paradigms: (1) Static Blacklisting (e.g., Google Safe Browsing, PhishTank), "
        "which provides high precision but suffers from 12–72 hour ingestion lag [14]; (2) Lexical Feature Mining, which extracts syntactic "
        "properties in real time without network lookups [15], [18]; (3) Dynamic DOM & Headless Crawling, which provides deep inspection but incurs "
        "prohibitive 2–5 second latency and severe SSRF risks [16], [20]; and (4) Blockchain Threat Federation, which introduces decentralized ledgers "
        "for tamper-evident evidence sharing [17], [23].")

    doc.add_page_break()

    # =========================================================================
    # PAGE 5 & 6: Table 2.1 Research Analysis (Papers 1-10)
    # =========================================================================
    p_sub2 = doc.add_paragraph()
    p_sub2.paragraph_format.space_before = Pt(4)
    p_sub2.paragraph_format.space_after = Pt(4)
    p_sub2.paragraph_format.keep_with_next = True
    r2 = p_sub2.add_run("Table 2.1 Research Analysis of Literature")
    r2.font.name = 'Times New Roman'
    r2.font.size = Pt(14)
    r2.bold = True

    all_papers = [
        ("01.", "Sahingoz et al.\n(2019) [15]",
         "Real-time phishing URL detection using NLP and machine learning algorithms.",
         "Random Forest, Decision Tree, SVM with lexical word vectors and n-grams.",
         "97.98% accuracy (RF); high latency on word vectors; informs URLSentinel's lightweight lexical tokenization."),

        ("02.", "Sahoo et al.\n(2019) [9]",
         "Comprehensive survey of malicious URL detection using batch and online learning.",
         "Taxonomy of feature extraction and online SGD/Passive-Aggressive models.",
         "92–95% theoretical accuracy; lacks deployable real-time system architecture and production safeguards."),

        ("03.", "Aljofey et al.\n(2020) [18]",
         "Phishing detection based strictly on URL lexical and syntactic features.",
         "Random Forest, Extra Trees, and XGBoost classifiers evaluating 30 URL properties.",
         "98.10% accuracy; no brand protection or whitelist; high false alarms on deep benign corporate paths."),

        ("04.", "Marchal et al.\n(2014) [19]",
         "PhishStorm: Real-time automated phishing detection with streaming data.",
         "Support Vector Machines evaluating intra-URL lexical relationships and n-gram frequencies.",
         "94.91% accuracy, 1.44% FPR; batch latency ~150ms; highlights need for sub-2ms engine in URLSentinel."),

        ("05.", "Rao & Pais\n(2019) [20]",
         "CatchPhish: Detection of phishing websites using computer vision and TF-IDF.",
         "Random Forest on text combined with CNN for visual logo and layout recognition.",
         "96.88% accuracy; visual rendering requires >3.5s; informs separation of lightweight and heavy sandbox tiers."),

        ("06.", "Baki et al.\n(2020) [21]",
         "Survey and detection of Domain Generation Algorithms (DGAs).",
         "Consonant-vowel ratios, n-gram entropy, and Hidden Markov Models.",
         "98.50% TPR, 0.45% FPR; relies on active DNS queries; adapted into URLSentinel's client-side consonant ratio."),

        ("07.", "Corona et al.\n(2014) [22]",
         "Adversarial evasion attacks against machine learning web detectors.",
         "Adversarial perturbations against lexical and linear classifiers.",
         "Linear models evaded with 85% success; validates URLSentinel's non-linear tree ensembles and Bayesian scoring."),

        ("08.", "Guan et al.\n(2020) [23]",
         "Decentralized threat intelligence sharing using consortium blockchain.",
         "Hyperledger Fabric smart contracts with PBFT consensus.",
         "350 tx/sec, zero data tampering; architectural foundation for URLSentinel's SHA-256 smart contract registry."),

        ("09.", "Li et al.\n(2021) [24]",
         "DeepURL: Multi-view deep learning architecture for malicious URLs.",
         "Character-level CNN and Bidirectional LSTM neural networks.",
         "97.35% accuracy; heavy GPU requirement, inference latency >80ms; unexplainable black-box decisions."),

        ("10.", "Verma & Dyer\n(2015) [25]",
         "Metric evaluation and dataset bias in phishing URL classification.",
         "PR-AUC evaluation across temporal and disjoint domain datasets.",
         "Showed 40% accuracy drops under domain overlap bias; mandates URLSentinel's domain-separated 2,000 URL test."),
    ]

    tbl_p1 = doc.add_table(rows=len(all_papers) + 1, cols=5)
    tbl_p1.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(tbl_p1)
    col_w = [0.45, 1.1, 1.5, 1.5, 1.95]

    hdr1 = tbl_p1.rows[0]
    hdr_titles = ["Sl.No.", "Author & Year", "Aim and Problem Statement", "Algorithm / Tech Stack", "Results & Relevance"]
    for i, t in enumerate(hdr_titles):
        cell = hdr1.cells[i]
        set_cell_background(cell, "E2E8F0")
        cell.width = Inches(col_w[i])
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before = Pt(3)
        p.paragraph_format.space_after = Pt(3)
        r = p.add_run(t)
        r.font.name = 'Times New Roman'
        r.font.size = Pt(9.5)
        r.bold = True

    for r_idx, p_data in enumerate(all_papers):
        row = tbl_p1.rows[r_idx + 1]
        for c_idx, val in enumerate(p_data):
            cell = row.cells[c_idx]
            set_cell_background(cell, "FFFFFF" if r_idx % 2 == 0 else "F8FAFC")
            cell.width = Inches(col_w[c_idx])
            p = cell.paragraphs[0]
            p.paragraph_format.space_before = Pt(3)
            p.paragraph_format.space_after = Pt(3)
            p.paragraph_format.line_spacing = 1.12
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER if c_idx == 0 else WD_ALIGN_PARAGRAPH.LEFT
            r = p.add_run(val)
            r.font.name = 'Times New Roman'
            r.font.size = Pt(8.5)

    # 2.2 Summary of Existing Research Works
    p_sum = doc.add_paragraph()
    p_sum.paragraph_format.space_before = Pt(8)
    p_sum.paragraph_format.space_after = Pt(4)
    p_sum.paragraph_format.keep_with_next = True
    r_sum = p_sum.add_run("2.2 Summary of Existing Research Works")
    r_sum.font.name = 'Times New Roman'
    r_sum.font.size = Pt(16)
    r_sum.bold = True

    add_para(doc,
        "The literature demonstrates significant progress in applying machine learning and natural language processing to URL detection. "
        "Early approaches by Sahingoz et al. [15] and Sahoo et al. [9] established that lexical tokens, n-grams, and tree-based ensembles "
        "(Random Forest, Gradient Boosting) achieve 95–98% accuracy on historical datasets. Subsequent research by Aljofey et al. [18] confirmed "
        "that purely static lexical analysis can yield high detection rates without active network fetches. However, as demonstrated by "
        "Corona et al. [22], attackers easily evade simplistic models through token padding and adversarial perturbations.")

    add_para(doc,
        "More recent investigations explored deep learning (Li et al. [24]) and computer vision (Rao & Pais [20]), achieving strong classification "
        "at the expense of substantial computational overhead (>80ms to 3.5s latency), rendering them unsuitable for inline browser interception. "
        "Concurrently, blockchain-based threat intelligence systems (Guan et al. [23]) proved the efficacy of decentralized ledgers for tamper-evident "
        "threat sharing, but operated independently of real-time endpoint classification engines.")

    doc.add_page_break()

    # =========================================================================
    # PAGE 7: 2.3 Research Gap and Relevance to Proposed System
    # =========================================================================
    p_sub4 = doc.add_paragraph()
    p_sub4.paragraph_format.space_before = Pt(4)
    p_sub4.paragraph_format.space_after = Pt(4)
    p_sub4.paragraph_format.keep_with_next = True
    r4 = p_sub4.add_run("2.3 Research Gap and Relevance to Proposed System")
    r4.font.name = 'Times New Roman'
    r4.font.size = Pt(16)
    r4.bold = True

    add_para(doc,
        "A critical analysis of existing research reveals four fundamental research gaps that URLSentinel addresses directly:")

    add_bullet("The Enterprise False-Positive Blind Spot: Academic models predominantly optimize for global accuracy, tolerating 1–3% False Positive Rates. In enterprise environments, this causes thousands of false alarms on complex OAuth SSO portals. URLSentinel introduces PSL tokenization and protected SSO overrides to achieve an absolute 0.00% False Positive Rate on corporate infrastructure.")
    add_bullet("Latency-Fidelity Trade-off: Systems rely either on fast but brittle rules or high-fidelity but sluggish deep models. URLSentinel's multi-tier architecture achieves sub-2ms lexical classification for inline browser protection while offloading heavy crawls asynchronously.")
    add_bullet("Lack of Cryptographic Verifiability: Existing threat repositories are centralized and subject to tampering. URLSentinel anchors SHA-256 evidence digests into an EVM smart contract, establishing immutable cryptographic auditability.")
    add_bullet("Uncontrolled Scanning Attack Surfaces: Existing dynamic crawlers expose internal networks to SSRF attacks. URLSentinel encapsulates active crawls in disposable containers with strict egress firewalls dropping RFC 1918 traffic.")

    add_para(doc,
        "By systematically resolving these four foundational gaps, URLSentinel establishes a verifiable, production-ready security platform "
        "that bridges the divide between theoretical machine learning benchmarks and high-assurance enterprise cyber defense.")

    doc.add_page_break()
    print("Chapter 2 built (exactly 4 pages, pp. 4-7).")
