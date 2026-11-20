"""
fix_spacing_layout_v2.py
========================
Conservative post-processing of URLSentinel_PPD_Report_FINAL.docx.

Changes made (all within main body only, NEVER preliminary pages):
  1. Bullet paragraphs: alignment → LEFT  (was JUSTIFY → word-stretch on short lines)
  2. Excessively spaced body paragraphs: trim space_before/after if > limits
  3. Table 2.1 Part 1 / Part 2 → merge into one continuous table
  4. Remove empty page-break paragraphs between Fig 5.6 and section 5.7 DFD
     (only the ONE blank spacer between them, not the chapter-level breaks)

WHAT WE DO NOT DO:
  - Do NOT remove chapter-level page-breaks (those keep TOC page numbers correct)
  - Do NOT touch any paragraph before '1. INTRODUCTION'
  - Do NOT change font, margins, or content

Output: URLSentinel_PPD_Report_SPACING_FIXED.docx
"""

import copy
import re
import sys
from pathlib import Path
from docx import Document
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Pt
from docx.text.paragraph import Paragraph as DocxParagraph
from docx.table import Table as DocxTable

REPORT_DIR = Path(r"z:\URLSentinel\URLSentinel_PPD_Report")
SRC = REPORT_DIR / "URLSentinel_PPD_Report_FINAL.docx"
DST = REPORT_DIR / "URLSentinel_PPD_Report_SPACING_FIXED.docx"

# ─────────────────────────────────────────────────────────────────────────────
# helpers
# ─────────────────────────────────────────────────────────────────────────────

def para_text(p):
    return "".join(r.text or "" for r in p.runs).strip()

def is_bullet(p):
    txt = para_text(p)
    if txt.startswith(("•", "–", "-", "▪", "✓", "○", "●")):
        return True
    pPr = p._p.find(qn("w:pPr"))
    if pPr is not None and pPr.find(qn("w:numPr")) is not None:
        return True
    return False

def get_pPr(p):
    pPr = p._p.find(qn("w:pPr"))
    if pPr is None:
        pPr = OxmlElement("w:pPr")
        p._p.insert(0, pPr)
    return pPr

def set_alignment_left(p):
    pPr = get_pPr(p)
    jc = pPr.find(qn("w:jc"))
    if jc is None:
        jc = OxmlElement("w:jc")
        pPr.append(jc)
    jc.set(qn("w:val"), "left")

def has_page_break(p):
    for br in p._p.iter(qn("w:br")):
        if br.get(qn("w:type")) == "page":
            return True
    return False

def remove_all_page_breaks(p):
    for br in list(p._p.iter(qn("w:br"))):
        if br.get(qn("w:type")) == "page":
            parent = br.getparent()
            parent.remove(br)

def is_heading_style(p):
    pPr = p._p.find(qn("w:pPr"))
    if pPr is None:
        return False
    pStyle = pPr.find(qn("w:pStyle"))
    if pStyle is None:
        return False
    return "heading" in pStyle.get(qn("w:val"), "").lower()

# ─────────────────────────────────────────────────────────────────────────────
# Load document
# ─────────────────────────────────────────────────────────────────────────────
print("Loading document …")
doc = Document(str(SRC))
body = doc.element.body

# Find main body start (paragraph "1. INTRODUCTION")
INTRO_PATTERN = re.compile(r"^1[\.\s]+INTRODUCTION", re.IGNORECASE)
main_body_start_idx = None
for idx, child in enumerate(body):
    tag = child.tag.split("}")[-1]
    if tag == "p":
        p = DocxParagraph(child, doc)
        if INTRO_PATTERN.match(para_text(p)):
            main_body_start_idx = idx
            print(f"  Main body starts at child index {idx}")
            break

if main_body_start_idx is None:
    print("ERROR: Could not find '1. INTRODUCTION'. Exiting.")
    sys.exit(1)

# ─────────────────────────────────────────────────────────────────────────────
# Step 1: Fix bullet alignment → LEFT in main body only
# ─────────────────────────────────────────────────────────────────────────────
print("\nStep 1: fixing bullet alignment …")
bullet_fixed = 0

for idx, child in enumerate(list(body)):
    if idx < main_body_start_idx:
        continue
    tag = child.tag.split("}")[-1]
    if tag == "p":
        p = DocxParagraph(child, doc)
        if is_bullet(p) and not is_heading_style(p):
            cur_jc = None
            pPr = p._p.find(qn("w:pPr"))
            if pPr is not None:
                jc_el = pPr.find(qn("w:jc"))
                if jc_el is not None:
                    cur_jc = jc_el.get(qn("w:val"), "")
            # Only change if it's justify ("both") or distribute
            if cur_jc in ("both", "distribute"):
                set_alignment_left(p)
                bullet_fixed += 1

print(f"  Bullet alignment fixed: {bullet_fixed} paragraphs")

# ─────────────────────────────────────────────────────────────────────────────
# Step 2: Fix distributed alignment anywhere in body
# ─────────────────────────────────────────────────────────────────────────────
print("\nStep 2: fixing distributed alignment …")
distributed_fixed = 0

for idx, child in enumerate(list(body)):
    if idx < main_body_start_idx:
        continue
    tag = child.tag.split("}")[-1]
    if tag == "p":
        p = DocxParagraph(child, doc)
        pPr = p._p.find(qn("w:pPr"))
        if pPr is not None:
            jc_el = pPr.find(qn("w:jc"))
            if jc_el is not None and jc_el.get(qn("w:val"), "") == "distribute":
                # Use justify for body, left for bullets
                if is_bullet(p):
                    jc_el.set(qn("w:val"), "left")
                else:
                    jc_el.set(qn("w:val"), "both")
                distributed_fixed += 1

print(f"  Distributed alignment fixed: {distributed_fixed}")

# ─────────────────────────────────────────────────────────────────────────────
# Step 3: Trim excessive paragraph space_before/after in main body
#          (only if > 12pt before or > 8pt after on non-heading paragraphs)
# ─────────────────────────────────────────────────────────────────────────────
print("\nStep 3: trimming excessive paragraph spacing …")
spacing_fixed = 0

for idx, child in enumerate(list(body)):
    if idx < main_body_start_idx:
        continue
    tag = child.tag.split("}")[-1]
    if tag == "p":
        p = DocxParagraph(child, doc)
        if is_heading_style(p):
            continue
        pPr = p._p.find(qn("w:pPr"))
        if pPr is not None:
            sp = pPr.find(qn("w:spacing"))
            if sp is not None:
                before = int(sp.get(qn("w:before"), "0"))
                after = int(sp.get(qn("w:after"), "0"))
                changed = False
                if before > 240:  # > 12pt
                    sp.set(qn("w:before"), "0")
                    changed = True
                if after > 160:  # > 8pt
                    sp.set(qn("w:after"), "80")  # 4pt
                    changed = True
                if changed:
                    spacing_fixed += 1

print(f"  Paragraph spacing trimmed: {spacing_fixed}")

# ─────────────────────────────────────────────────────────────────────────────
# Step 4: Merge Table 2.1 Part 1 and Part 2
# ─────────────────────────────────────────────────────────────────────────────
print("\nStep 4: merging Table 2.1 Part 1 and Part 2 …")

body_children = list(body)

def get_preceding_text(children, tbl_idx, look_back=4):
    """Return text of the nearest paragraph before tbl_idx."""
    for i in range(tbl_idx - 1, max(-1, tbl_idx - look_back - 1), -1):
        child = children[i]
        tag = child.tag.split("}")[-1]
        if tag == "p":
            p = DocxParagraph(child, doc)
            t = para_text(p)
            if t:
                return t
    return ""

# Collect all table elements with their body indices
table_entries = []
for i, child in enumerate(body_children):
    if i < main_body_start_idx:
        continue
    tag = child.tag.split("}")[-1]
    if tag == "tbl":
        prec = get_preceding_text(body_children, i)
        table_entries.append((i, child, prec))

part1_idx = None
part1_elem = None
part2_idx = None
part2_elem = None

for i, elem, prec in table_entries:
    if part1_elem is None and "Part 1" in prec:
        part1_idx = i
        part1_elem = elem
        print(f"  Part 1 table at body index {i}, preceded by: '{prec[:60]}'")
    elif part1_elem is not None and "Part 2" in prec:
        part2_idx = i
        part2_elem = elem
        print(f"  Part 2 table at body index {i}, preceded by: '{prec[:60]}'")
        break

merged = False
if part1_elem is not None and part2_elem is not None:
    # Move all rows from Part 2 (skip header row 0) to Part 1
    part2_rows = list(part2_elem.findall(qn("w:tr")))
    rows_moved = 0
    for row in part2_rows[1:]:  # skip repeated column header
        part1_elem.append(copy.deepcopy(row))
        rows_moved += 1
    print(f"  Moved {rows_moved} data rows from Part 2 → Part 1")

    # Find current positions of part1 and part2 (indices may have shifted, use object identity)
    children_now = list(body)
    p1_pos = next((i for i, c in enumerate(children_now) if c is part1_elem), None)
    p2_pos = next((i for i, c in enumerate(children_now) if c is part2_elem), None)

    if p1_pos is not None and p2_pos is not None:
        # Remove everything from p1_pos+1 to p2_pos (inclusive)
        to_remove = children_now[p1_pos + 1 : p2_pos + 1]
        for elem in to_remove:
            body.remove(elem)
        print(f"  Removed {len(to_remove)} elements (gap + Part 2 table)")
        merged = True

    # Update caption: remove "(Part 1)"
    children_now2 = list(body)
    p1_pos2 = next((i for i, c in enumerate(children_now2) if c is part1_elem), None)
    if p1_pos2 is not None:
        for look in range(p1_pos2 - 1, max(p1_pos2 - 5, -1), -1):
            child = children_now2[look]
            tag = child.tag.split("}")[-1]
            if tag == "p":
                p = DocxParagraph(child, doc)
                txt = para_text(p)
                if "2.1" in txt and "Part" in txt:
                    for run in p.runs:
                        if "(Part 1)" in (run.text or ""):
                            run.text = run.text.replace("(Part 1)", "").strip()
                            print(f"  Updated caption: '{para_text(p)}'")
                    break
else:
    print("  WARNING: Could not locate both Part 1/Part 2 tables — skipping merge")

# ─────────────────────────────────────────────────────────────────────────────
# Step 5: Fix Section 5.7 DFD — remove ONLY the blank spacer between
#          Fig 5.6 and the 5.7 heading, NOT the chapter-level page-break
# ─────────────────────────────────────────────────────────────────────────────
print("\nStep 5: Fixing 5.6 → 5.7 spacing …")

DFD_PAT = re.compile(r"5\.7[\s.]+Data Flow", re.IGNORECASE)
children_now = list(body)
dfd_idx = None
for i, child in enumerate(children_now):
    if i < main_body_start_idx:
        continue
    tag = child.tag.split("}")[-1]
    if tag == "p":
        p = DocxParagraph(child, doc)
        if DFD_PAT.search(para_text(p)):
            dfd_idx = i
            print(f"  5.7 heading at index {i}")
            break

pg_breaks_removed = 0
if dfd_idx is not None:
    # Look back up to 3 positions for empty page-break paragraphs
    for look in range(dfd_idx - 1, max(dfd_idx - 4, main_body_start_idx), -1):
        child = children_now[look]
        tag = child.tag.split("}")[-1]
        if tag != "p":
            break
        p = DocxParagraph(child, doc)
        txt = para_text(p)
        if txt == "" and has_page_break(p):
            # This is a pure spacer page-break — remove inline break,
            # but keep the empty paragraph so section 5.7 stays on same flow
            remove_all_page_breaks(p)
            pg_breaks_removed += 1
            print(f"  Removed inline page-break from empty para at index {look}")
        elif txt == "":
            # Truly empty paragraph with no page break — remove it
            body.remove(child)
            pg_breaks_removed += 1
            print(f"  Removed empty paragraph at index {look}")

print(f"  Page breaks / empty paras removed near 5.7: {pg_breaks_removed}")

# ─────────────────────────────────────────────────────────────────────────────
# Step 6: Save
# ─────────────────────────────────────────────────────────────────────────────
print(f"\nSaving to: {DST}")
doc.save(str(DST))
print("Saved successfully.")
print(f"\nSummary:")
print(f"  bullet_align_fixed:  {bullet_fixed}")
print(f"  distributed_fixed:   {distributed_fixed}")
print(f"  spacing_fixed:       {spacing_fixed}")
print(f"  table_2.1_merged:    {merged}")
print(f"  pg_breaks_near_5.7:  {pg_breaks_removed}")
