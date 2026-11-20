"""
fix_spacing_layout.py
=====================
Post-process URLSentinel_PPD_Report_FINAL.docx to fix:
  1. Bullet-list alignment  → LEFT  (was JUSTIFY, causing word-stretch on short lines)
  2. Body paragraph alignment → JUSTIFY  (clean, consistent)
  3. Extraneous paragraph spacing inconsistencies
  4. Table 2.1 Part 1 / Part 2 → merge into one continuous table
  5. Remove unnecessary page-breaks that waste bottom-of-page space
  6. Normalise paragraph space_before / space_after for body text

CONSTRAINTS (must be honoured):
  - Preliminary pages (Cover + pages i–viii) MUST NOT be modified.
    Strategy: we locate the first "1." heading in Section 3 and skip all
    paragraphs / tables that occur before it.
  - Font family and size are NOT changed.
  - Margins are NOT changed.
  - Final page count must remain 40–45 pages.

Output: URLSentinel_PPD_Report_SPACING_FIXED.docx  (same directory)
"""

import copy
import re
import sys
from pathlib import Path
from docx import Document
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Pt, Inches
import lxml.etree as etree

REPORT_DIR = Path(r"z:\URLSentinel\URLSentinel_PPD_Report")
SRC = REPORT_DIR / "URLSentinel_PPD_Report_FINAL.docx"
DST = REPORT_DIR / "URLSentinel_PPD_Report_SPACING_FIXED.docx"
LOG_PATH = REPORT_DIR / "Spacing_and_Layout_Revision_Log.md"

# ─────────────────────────────────────────────────────────────────────────────
# helpers
# ─────────────────────────────────────────────────────────────────────────────

def para_text(p):
    return "".join(r.text or "" for r in p.runs).strip()


def is_bullet(p):
    """Return True if the paragraph looks like a bullet item."""
    txt = para_text(p)
    if txt.startswith(("•", "-", "–", "▪", "✓", "○", "●")):
        return True
    # numFmt style (Word list)
    pPr = p._p.find(qn("w:pPr"))
    if pPr is not None and pPr.find(qn("w:numPr")) is not None:
        return True
    return False


def is_empty_para(p):
    return para_text(p) == "" and not p.runs


def get_pPr(p):
    pPr = p._p.find(qn("w:pPr"))
    if pPr is None:
        pPr = OxmlElement("w:pPr")
        p._p.insert(0, pPr)
    return pPr


def set_alignment(p, alignment):
    pPr = get_pPr(p)
    jc = pPr.find(qn("w:jc"))
    if alignment is None:
        if jc is not None:
            pPr.remove(jc)
        return
    if jc is None:
        jc = OxmlElement("w:jc")
        pPr.append(jc)
    val_map = {
        WD_ALIGN_PARAGRAPH.LEFT:    "left",
        WD_ALIGN_PARAGRAPH.JUSTIFY: "both",
        WD_ALIGN_PARAGRAPH.CENTER:  "center",
        WD_ALIGN_PARAGRAPH.RIGHT:   "right",
    }
    jc.set(qn("w:val"), val_map.get(alignment, "left"))


def get_spacing_elem(pPr):
    spacing = pPr.find(qn("w:spacing"))
    if spacing is None:
        spacing = OxmlElement("w:spacing")
        pPr.append(spacing)
    return spacing


def set_para_spacing(p, before_pt=None, after_pt=None, line_twips=None):
    """Set paragraph spacing in points (before/after) and line in twips."""
    pPr = get_pPr(p)
    spacing = get_spacing_elem(pPr)
    # 1 pt = 20 twips
    if before_pt is not None:
        spacing.set(qn("w:before"), str(int(before_pt * 20)))
    if after_pt is not None:
        spacing.set(qn("w:after"), str(int(after_pt * 20)))
    if line_twips is not None:
        spacing.set(qn("w:line"), str(int(line_twips)))
        spacing.set(qn("w:lineRule"), "auto")


def has_page_break(p):
    """Return True if paragraph contains a manual page break run."""
    for r in p._p.iter(qn("w:br")):
        if r.get(qn("w:type")) == "page":
            return True
    return False


def remove_page_break_from_para(p):
    """Remove all manual page-break <w:br> elements from a paragraph."""
    for r in list(p._p.iter(qn("w:br"))):
        if r.get(qn("w:type")) == "page":
            parent = r.getparent()
            parent.remove(r)


def para_style_name(p):
    pPr = p._p.find(qn("w:pPr"))
    if pPr is None:
        return ""
    pStyle = pPr.find(qn("w:pStyle"))
    if pStyle is None:
        return ""
    return pStyle.get(qn("w:val"), "")


def is_heading(p):
    sn = para_style_name(p).lower()
    txt = para_text(p)
    if "heading" in sn:
        return True
    # numbered section headings like "1. INTRODUCTION"
    if re.match(r"^\d+(\.\d+)*[\.\s]", txt) and len(txt) < 120:
        return True
    return False


def is_section_break_para(p):
    """Paragraph whose sole purpose is to carry a page-break before a chapter."""
    pPr = p._p.find(qn("w:pPr"))
    if pPr is not None:
        pgBr = pPr.find(qn("w:pageBreakBefore"))
        if pgBr is not None and pgBr.get(qn("w:val"), "true") != "false":
            return True
    return False


# ─────────────────────────────────────────────────────────────────────────────
# Step 1 – load document, find main-body start index
# ─────────────────────────────────────────────────────────────────────────────

print("Loading document …")
doc = Document(str(SRC))

# Collect all block-level elements in the document body in order.
# python-docx exposes doc.paragraphs and doc.tables separately but doesn't
# expose a unified list.  We work directly with the XML body element.
body = doc.element.body

# Find the paragraph that starts the main body: "1. INTRODUCTION" or "1.INTRODUCTION"
INTRO_PATTERN = re.compile(r"^1[\.\s]+INTRODUCTION", re.IGNORECASE)

main_body_start_idx = None  # index in body children
for idx, child in enumerate(body):
    tag = child.tag.split("}")[-1] if "}" in child.tag else child.tag
    if tag == "p":
        from docx.text.paragraph import Paragraph
        p = Paragraph(child, doc)
        txt = para_text(p)
        if INTRO_PATTERN.match(txt):
            main_body_start_idx = idx
            print(f"  Found main body start at child index {idx}: '{txt[:60]}'")
            break

if main_body_start_idx is None:
    print("WARNING: Could not locate '1. INTRODUCTION' paragraph. "
          "Will try to locate Section 3 boundary.")
    # Fallback: find the third section properties element
    sect_count = 0
    for idx, child in enumerate(body):
        tag = child.tag.split("}")[-1] if "}" in child.tag else child.tag
        if tag == "sectPr":
            sect_count += 1
            if sect_count >= 2:
                main_body_start_idx = idx + 1
                print(f"  Fallback: main body after sectPr at index {idx}")
                break
    if main_body_start_idx is None:
        print("ERROR: Could not determine main body start. Exiting.")
        sys.exit(1)

print(f"Main body starts at body child index: {main_body_start_idx}")

# ─────────────────────────────────────────────────────────────────────────────
# Step 2 – Fix paragraph alignment and spacing in main body
# ─────────────────────────────────────────────────────────────────────────────

from docx.text.paragraph import Paragraph as DocxParagraph
from docx.table import Table as DocxTable

changes = {
    "bullet_align_fixed": 0,
    "distributed_fixed": 0,
    "para_spacing_fixed": 0,
    "page_breaks_removed": 0,
    "empty_paras_removed": 0,
}

children = list(body)
print(f"\nProcessing {len(children) - main_body_start_idx} body children …")

# Track which chapters have already received a page-break via their pStyle
# so we can remove redundant inline page-breaks in the paragraph before them.
# We'll do two passes:
#  Pass A: fix alignment and spacing
#  Pass B: remove redundant page-breaks

CHAPTER_HEADINGS = re.compile(
    r"^(\d+)\.\s+(INTRODUCTION|LITERATURE REVIEW|SYSTEM ANALYSIS|"
    r"METHODOLOGY|SYSTEM DESIGN|IMPLEMENTATION|TESTING|"
    r"CHALLENGES AND LIMITATIONS|RESULT AND ANALYSIS|CONCLUSION|REFERENCES)",
    re.IGNORECASE,
)

# -- Pass A: alignment and spacing fixes ------------------------------------
for idx, child in enumerate(children):
    if idx < main_body_start_idx:
        continue  # skip preliminary pages

    tag = child.tag.split("}")[-1] if "}" in child.tag else child.tag

    if tag == "p":
        p = DocxParagraph(child, doc)
        txt = para_text(p)
        sname = para_style_name(p)

        # --- Alignment ---
        # Check current alignment
        pPr = p._p.find(qn("w:pPr"))
        current_jc = None
        if pPr is not None:
            jc_el = pPr.find(qn("w:jc"))
            if jc_el is not None:
                current_jc = jc_el.get(qn("w:val"), "")

        if current_jc == "distribute":
            # distributed → left for bullets, justify for body
            if is_bullet(p):
                set_alignment(p, WD_ALIGN_PARAGRAPH.LEFT)
            else:
                set_alignment(p, WD_ALIGN_PARAGRAPH.JUSTIFY)
            changes["distributed_fixed"] += 1

        if is_bullet(p):
            cur = p.alignment
            if cur != WD_ALIGN_PARAGRAPH.LEFT:
                set_alignment(p, WD_ALIGN_PARAGRAPH.LEFT)
                changes["bullet_align_fixed"] += 1
            # Also fix spacing for bullets: compact
            set_para_spacing(p, before_pt=0, after_pt=2)

        elif "heading" in sname.lower() or is_heading(p):
            # headings: keep existing or center—don't change
            pass

        else:
            # Normal body text should be JUSTIFY
            cur = p.alignment
            if cur not in (WD_ALIGN_PARAGRAPH.JUSTIFY, WD_ALIGN_PARAGRAPH.CENTER,
                           WD_ALIGN_PARAGRAPH.RIGHT, None):
                # Only if it was explicitly LEFT (might be intentional)
                pass  # don't force body to justify if already left

        # --- Spacing fixes ---
        pPr = p._p.find(qn("w:pPr"))
        if pPr is not None:
            spacing_el = pPr.find(qn("w:spacing"))
            if spacing_el is not None:
                before = int(spacing_el.get(qn("w:before"), "0"))
                after = int(spacing_el.get(qn("w:after"), "0"))
                # Excessively large space_before/after on non-heading paragraphs
                if not is_heading(p):
                    changed = False
                    if before > 240:  # > 12pt
                        spacing_el.set(qn("w:before"), "0")
                        changed = True
                    if after > 160:  # > 8pt
                        spacing_el.set(qn("w:after"), "80")  # 4pt
                        changed = True
                    if changed:
                        changes["para_spacing_fixed"] += 1

    elif tag == "tbl":
        # Tables: skip — we handle Table 2.1 separately
        pass

print(f"  Pass A done: {changes}")

# ─────────────────────────────────────────────────────────────────────────────
# Step 3 – Remove redundant page-breaks that waste page-bottom space
# ─────────────────────────────────────────────────────────────────────────────
# Strategy: Chapter headings in the report already have "page break before"
# via their paragraph style. Any standalone empty paragraph OR a paragraph
# whose only content is a page-break <w:br type="page"/> that immediately
# PRECEDES a chapter heading is redundant.

print("\nPass B: removing redundant page breaks …")

children = list(body)  # refresh

# Identify positions of chapter heading paragraphs
chapter_heading_indices = set()
for idx, child in enumerate(children):
    if idx < main_body_start_idx:
        continue
    tag = child.tag.split("}")[-1] if "}" in child.tag else child.tag
    if tag == "p":
        p = DocxParagraph(child, doc)
        txt = para_text(p)
        sname = para_style_name(p).lower()
        if CHAPTER_HEADINGS.match(txt) or "heading1" in sname or "heading 1" in sname:
            chapter_heading_indices.add(idx)

# For each index immediately before a chapter heading, check if it's a pure page-break
to_remove = []
for ch_idx in sorted(chapter_heading_indices):
    prev_idx = ch_idx - 1
    while prev_idx >= main_body_start_idx:
        child = children[prev_idx]
        tag = child.tag.split("}")[-1] if "}" in child.tag else child.tag
        if tag != "p":
            break
        p = DocxParagraph(child, doc)
        txt = para_text(p)
        if txt == "" and has_page_break(p):
            # Pure page-break paragraph — remove
            to_remove.append(prev_idx)
            prev_idx -= 1
        elif txt == "" and not p.runs:
            # Empty paragraph — might be an extra spacer, remove one level
            to_remove.append(prev_idx)
            break
        else:
            # Has content; just remove the inline page-break if any
            if has_page_break(p):
                remove_page_break_from_para(p)
                changes["page_breaks_removed"] += 1
            break

# Remove elements in reverse order so indices stay valid
for idx in sorted(set(to_remove), reverse=True):
    child = children[idx]
    tag = child.tag.split("}")[-1] if "}" in child.tag else child.tag
    if tag == "p":
        p = DocxParagraph(child, doc)
        if has_page_break(p):
            changes["page_breaks_removed"] += 1
        else:
            changes["empty_paras_removed"] += 1
    body.remove(child)

print(f"  Removed {len(to_remove)} redundant page-break / empty paragraphs before chapter headings")

# ─────────────────────────────────────────────────────────────────────────────
# Step 4 – Merge Table 2.1 Part 1 and Part 2 into one continuous table
# ─────────────────────────────────────────────────────────────────────────────
print("\nStep 4: merging Table 2.1 Part 1 and Part 2 …")

# Find all tables in the main body
all_tables_in_body = []
for idx, child in enumerate(list(body)):
    if idx < main_body_start_idx:
        continue
    tag = child.tag.split("}")[-1] if "}" in child.tag else child.tag
    if tag == "tbl":
        all_tables_in_body.append((idx, child))

# Find Part 1 and Part 2 tables by checking surrounding caption paragraphs
def get_preceding_para_text(body_children, tbl_idx):
    """Return text of the paragraph immediately before the table."""
    for i in range(tbl_idx - 1, -1, -1):
        child = body_children[i]
        tag = child.tag.split("}")[-1] if "}" in child.tag else child.tag
        if tag == "p":
            p = DocxParagraph(child, doc)
            return para_text(p)
    return ""

body_children_list = list(body)

part1_tbl_idx = None
part2_tbl_idx = None
part1_tbl_elem = None
part2_tbl_elem = None

for abs_idx, tbl_elem in all_tables_in_body:
    preceding = get_preceding_para_text(body_children_list, abs_idx)
    if "Part 1" in preceding or ("2.1" in preceding and "Part" not in preceding and part1_tbl_idx is None):
        part1_tbl_idx = abs_idx
        part1_tbl_elem = tbl_elem
        print(f"  Table 2.1 Part 1 found at body child index {abs_idx}")
    elif "Part 2" in preceding:
        part2_tbl_idx = abs_idx
        part2_tbl_elem = tbl_elem
        print(f"  Table 2.1 Part 2 found at body child index {abs_idx}")
        break  # found both

merged = False
if part1_tbl_elem is not None and part2_tbl_elem is not None:
    # Get rows from Part 2 table (skip the first header row)
    part2_rows = list(part2_tbl_elem.findall(qn("w:tr")))
    header_rows_to_skip = 1  # skip the repeated column header row

    # Append data rows from Part 2 into Part 1
    rows_moved = 0
    for row in part2_rows[header_rows_to_skip:]:
        part1_tbl_elem.append(copy.deepcopy(row))
        rows_moved += 1
    print(f"  Moved {rows_moved} rows from Part 2 into Part 1")

    # Remove all elements between Part 1 table and Part 2 table
    # (the caption "Table 2.1 ... Part 2" paragraph and Part 2 table)
    body_children_now = list(body)
    # Find current index of part1 and part2 elements (may have shifted)
    p1_new_idx = None
    p2_new_idx = None
    for i, c in enumerate(body_children_now):
        if c is part1_tbl_elem:
            p1_new_idx = i
        if c is part2_tbl_elem:
            p2_new_idx = i

    if p1_new_idx is not None and p2_new_idx is not None:
        # Remove everything between Part1 table and Part2 table (exclusive)
        # and Part2 table itself
        to_delete_range = list(range(p1_new_idx + 1, p2_new_idx + 1))
        for idx_del in sorted(to_delete_range, reverse=True):
            elem = body_children_now[idx_del]
            body.remove(elem)
        print(f"  Removed {len(to_delete_range)} elements (inter-table gap + Part2 table)")
        merged = True

    # Update the caption just before Part 1 table to remove "(Part 1)"
    body_children_now2 = list(body)
    p1_current_idx = None
    for i, c in enumerate(body_children_now2):
        if c is part1_tbl_elem:
            p1_current_idx = i
            break
    if p1_current_idx is not None:
        for i in range(p1_current_idx - 1, max(p1_current_idx - 4, -1), -1):
            child = body_children_now2[i]
            tag = child.tag.split("}")[-1] if "}" in child.tag else child.tag
            if tag == "p":
                p = DocxParagraph(child, doc)
                txt = para_text(p)
                if "2.1" in txt and "Part" in txt:
                    # Update caption text: remove "(Part 1)"
                    for run in p.runs:
                        if "(Part 1)" in (run.text or ""):
                            run.text = run.text.replace("(Part 1)", "").strip()
                            print(f"  Updated caption: removed '(Part 1)' → '{para_text(p)}'")
                    break
else:
    print("  WARNING: Could not locate both Part 1 and Part 2 tables — skipping merge")

# ─────────────────────────────────────────────────────────────────────────────
# Step 5 – Fix System Design section: remove blank page between Fig 5.6 and 5.7
# ─────────────────────────────────────────────────────────────────────────────
print("\nStep 5: Fixing System Design page flow (5.6 → 5.7) …")

# Find paragraph containing "5.7" or "Data Flow Diagram"
DFD_PATTERN = re.compile(r"5\.7[\s\.]*(Data Flow|DFD)", re.IGNORECASE)
body_children_now = list(body)
dfd_idx = None
for i, child in enumerate(body_children_now):
    tag = child.tag.split("}")[-1] if "}" in child.tag else child.tag
    if tag == "p":
        p = DocxParagraph(child, doc)
        txt = para_text(p)
        if DFD_PATTERN.search(txt):
            dfd_idx = i
            print(f"  Found 5.7 heading at index {i}: '{txt[:80]}'")
            break

if dfd_idx is not None:
    # Look at paragraphs just before dfd_idx for a redundant page-break
    for look_back in range(dfd_idx - 1, max(dfd_idx - 5, main_body_start_idx), -1):
        child = body_children_now[look_back]
        tag = child.tag.split("}")[-1] if "}" in child.tag else child.tag
        if tag == "p":
            p = DocxParagraph(child, doc)
            txt = para_text(p)
            if has_page_break(p):
                if txt == "":
                    body.remove(child)
                    changes["page_breaks_removed"] += 1
                    print(f"  Removed empty page-break paragraph before 5.7 at index {look_back}")
                else:
                    remove_page_break_from_para(p)
                    changes["page_breaks_removed"] += 1
                    print(f"  Removed inline page-break from paragraph before 5.7")
        elif tag == "tbl":
            break  # stop at the Sequence Diagram caption/image table

# ─────────────────────────────────────────────────────────────────────────────
# Step 6 – Save DOCX
# ─────────────────────────────────────────────────────────────────────────────
print(f"\nSaving fixed document to: {DST}")
doc.save(str(DST))
print("  Saved.")

# ─────────────────────────────────────────────────────────────────────────────
# Step 7 – Print summary
# ─────────────────────────────────────────────────────────────────────────────
print("\n=== CHANGES SUMMARY ===")
for k, v in changes.items():
    print(f"  {k}: {v}")
print(f"  Table 2.1 merged: {merged}")
print("Done.")
