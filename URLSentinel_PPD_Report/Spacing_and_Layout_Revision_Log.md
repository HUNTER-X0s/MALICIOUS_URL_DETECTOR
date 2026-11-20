# Spacing and Layout Revision Log
## URLSentinel PPD Report — Spacing, References, and Page 32/33 Layout Correction

**Date:** 2026-11-16  
**Files Updated:**
- `z:\URLSentinel\URLSentinel_PPD_Report\URLSentinel_PPD_Report_FINAL.docx` (3,195,648 bytes)
- `z:\URLSentinel\URLSentinel_PPD_Report\URLSentinel_PPD_Report_FINAL.pdf` (1,403,594 bytes)
- `z:\URLSentinel\URLSentinel_PPD_Report\URLSentinel_PPD_Report_SPACING_FIXED.docx` (3,195,648 bytes)
- `z:\URLSentinel\URLSentinel_PPD_Report\URLSentinel_PPD_Report_SPACING_FIXED.pdf` (1,403,594 bytes)

---

## 1. Executive Summary & Verification Matrix

| Check / Metric | Target | Verified Result | Status |
|---|---|---|:---:|
| **Total Report Pages** | 40–45 pages | **Exactly 44 pages** | **PASS** ✓ |
| **Preliminary Pages (Cover to viii)** | 9 pages | **Exactly 9 pages (Cover + i–viii)** | **PASS** ✓ |
| **Reference Part Word Spacing** | Uniform (~3.0 pt) | **Average 3.00 pt (Min 2.88 pt, Max 3.16 pt)** | **PASS** ✓ |
| **Displayed Page 32 Spacing (Ch 9.3/9.4)** | No orphan lines, tight gaps | **Average 3.30 pt (Min 2.49 pt, Max 5.49 pt)** | **PASS** ✓ |
| **Displayed Page 33 Spacing (Ch 10 Conclusion)** | Uniform, no stretched words | **All lines 2.7 pt – 6.3 pt (Down from 10.1 pt)** | **PASS** ✓ |
| **Algorithm Code Boxes (PDF pp. 31–32)** | Monospace Left-aligned | **Explicit LEFT alignment on all lines** | **PASS** ✓ |
| **Table 2.1 Research Analysis** | Continuous table | **Single merged table across pp. 5–6** | **PASS** ✓ |

---

## 2. Table of Contents vs. Actual Chapter Page Verification

Every chapter page in `FINAL.pdf` and `SPACING_FIXED.pdf` was scanned using PyMuPDF and verified against the Table of Contents:

| Chapter / Section | TOC Page No. | Actual PDF Page | Actual Displayed Page | Match? |
|---|:---:|:---:|:---:|:---:|
| **1. INTRODUCTION** | 1 | PDF Pg 10 | 1 | **100% MATCH** ✓ |
| **2. LITERATURE REVIEW** | 4 | PDF Pg 13 | 4 | **100% MATCH** ✓ |
| **3. SYSTEM ANALYSIS** | 8 | PDF Pg 17 | 8 | **100% MATCH** ✓ |
| **4. METHODOLOGY** | 11 | PDF Pg 20 | 11 | **100% MATCH** ✓ |
| **5. SYSTEM DESIGN** | 14 | PDF Pg 23 | 14 | **100% MATCH** ✓ |
| **6. IMPLEMENTATION** | 20 | PDF Pg 29 | 20 | **100% MATCH** ✓ |
| **7. TESTING** | 25 | PDF Pg 34 | 25 | **100% MATCH** ✓ |
| **8. CHALLENGES AND LIMITATIONS** | 28 | PDF Pg 37 | 28 | **100% MATCH** ✓ |
| **9. RESULT AND ANALYSIS** | 30 | PDF Pg 39 | 30 | **100% MATCH** ✓ |
| **- 9.3 Performance & 9.4 Advantages** | 32 | PDF Pg 41 | 32 | **100% MATCH** ✓ |
| **10. CONCLUSION & FUTURE SCOPE** | 33 | PDF Pg 42 | 33 | **100% MATCH** ✓ |
| **REFERENCE (Citations [1]–[16])** | 34 | PDF Pg 43 | 34 | **100% MATCH** ✓ |
| **REFERENCE (Citations [17]–[30])** | 34–35 | PDF Pg 44 | 35 | **100% MATCH** ✓ |

---

## 3. Specific Root Causes Identified and Fixed

### A. Reference Part (Displayed Pages 34 & 35 / Citations [1] to [30])
- **Root Cause:** Citations were previously assigned `p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY`. When citations contained long unbroken strings (e.g. URLs such as `https://cheatsheetseries.owasp.org/`, `https://security.googleblog.com/`, `https://www.w3.org/community/webextensions/` or conference acronyms like `Distributed Comput. Syst. (ICDCS)`), Word wrapped the long string to the following line. The remaining tokens on that line were stretched across the entire margin width (6.25 inches minus hanging indent), creating excessive gaps (up to **9.50 pt**). Meanwhile, the final line of each citation was left un-stretched (having normal **2.88 pt** spaces), causing the noticeable "very large vs very small gaps" defect.
- **Correction Applied:**
  1. Updated `final_sections/references_sec.py` to enforce **`p.alignment = WD_ALIGN_PARAGRAPH.LEFT`** (standard IEEE ragged-right bibliography formatting) with `left_indent = Inches(0.35)` and `first_line_indent = Inches(-0.35)`.
  2. In LEFT alignment, every word space is rendered at the exact natural glyph space of 12pt Times New Roman (**3.00 pt** average across all lines).
  3. Cleaned page flow between Page 34 (citations [1]–[16]) and Page 35 (citations [17]–[30]), removing any stray blank page.

### B. Displayed Page 33 (Chapter 10: Conclusion & Future Scope)
- **Root Cause:**
  1. Key milestones were previously defined in a single paragraph using embedded `\n` characters with `JUSTIFY` alignment. Word rendered soft line breaks while forcing full line justification, leading to fragmented words (`entropy`, `in`, `an`, `ultra-fast`, `1.39`, `milliseconds.`) being stretched across isolated lines.
  2. Long compound words in prose lines (`comprehensive, enterprise-ready`, `classification accuracy`, `hardware-isolated`) caused loose lines with gaps up to **10.11 pt**.
- **Correction Applied:**
  1. Separated the 5 engineering milestones into individual bullet paragraphs using `add_bullet(doc, ...)`, which enforces explicit `LEFT` alignment.
  2. Balanced the prose sentence lengths in Section 10.1 (Paragraph 1 and Paragraph 3) and Section 10.2 (Future Scope) so that character counts per line are uniform (92–98 characters).
  3. Inter-word spacing on Displayed Page 33 dropped from 10.11 pt down to **2.7 pt – 6.3 pt** across all lines.

### C. Displayed Page 32 (Section 9.3 & 9.4 Advantages)
- **Root Cause:** The third bullet in Section 9.4 ("Actionable Human Explainability...") wrapped the single word `decisions.` to a third line on its own.
- **Correction Applied:**
  1. Refined the bullet text to: `"Actionable Explainability: Replaces opaque risk numbers with deterministic risk factor tags, empowering users to make informed navigation decisions."`
  2. All 5 advantage bullets now fit tightly on 2 lines each, with clean left-alignment and zero orphan words.
  3. Overall line spacing on Page 32: **2.49 pt to 5.49 pt** (zero lines over 6.0 pt).

### D. Table 2.1 Research Analysis of Literature (Chapter 2)
- **Root Cause:** Table 2.1 was previously separated into "Part 1" and "Part 2" with duplicate headers and an artificial page break.
- **Correction Applied:** Merged all 10 papers into a single continuous `Table 2.1 Research Analysis of Literature` directly in `final_sections/ch2_lit_review.py`. The table flows smoothly from Page 5 to Page 6, keeping Chapter 2 at exactly 4 pages.

### E. Algorithm Code Boxes (PDF Pages 31 & 32 / Displayed Pages 22 & 23)
- **Root Cause:** In `report_sections/common.py`, pseudocode steps in `add_algorithm_box()` inherited the default `Normal` style without an explicit alignment tag, causing code lines to be justified.
- **Correction Applied:** Added explicit `p_s.alignment = WD_ALIGN_PARAGRAPH.LEFT` in `report_sections/common.py` for all algorithm code lines.
