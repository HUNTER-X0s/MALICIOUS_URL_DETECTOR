"""
fix_spacing_layout_v3.py
========================
Conservative post-processing of URLSentinel_PPD_Report_FINAL.docx.

Fixes:
  1. Bullet paragraphs: add explicit jc=left override (they inherit JUSTIFY from Normal style)
  2. Distributed alignment → fix to left/justify
  3. Excessive paragraph spacing trim
  4. Table 2.1 Part 1 / Part 2 → merge into one continuous table
  5. Remove empty page-break spacer between Fig 5.6 and 5.7 DFD heading

Preserves:
  - ALL preliminary pages (indices 0 to main_body_start_idx - 1) UNCHANGED
  - Chapter-level page-breaks (preserve TOC alignment)
  - Font, margins, content
"""

import copy
import re
import sys
from pathlib import Path
from docx import Document
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.text.paragraph import Paragraph as DocxParagraph

REPORT_DIR = Path(r"z:\URLSentinel\URLSentinel_PPD_Report")
SRC = REPORT_DIR / "URLSentinel_PPD_Report_FINAL.docx"
DST = REPORT_DIR / "URLSentinel_PPD_Report_SPACING_FIXED.docx"

def para_text(p):
    return "".join(r.text or "" for r in p.runs).strip()

def is_bullet(p):
    txt = para_text(p)
    if txt.startswith(("•", "–", "▪", "✓", "○", "●")):
        return True
    pPr = p._p.find(qn("w:pPr"))
    if pPr is not None and pPr.find(qn("w:numPr")) is not None:
        return True
    return False

def is_heading_style(p):
    if p.style and p.style.name:
        if "heading" in p.style.name.lower():
            return True
    pPr = p._p.find(qn("w:pPr"))
    if pPr is not None:
        pStyle = pPr.find(qn("w:pStyle"))
        if pStyle is not None and "heading" in pStyle.get(qn("w:val"), "").lower():
            return True
    return False

def get_pPr(p):
    pPr = p._p.find(qn("w:pPr"))
    if pPr is None:
        pPr = OxmlElement("w:pPr")
        p._p.insert(0, pPr)
    return pPr

def set_jc(p, val):
    """Set explicit paragraph jc (alignment) value."""
    pPr = get_pPr(p)
    jc = pPr.find(qn("w:jc"))
    if jc is None:
        jc = OxmlElement("w:jc")
        pPr.append(jc)
    jc.set(qn("w:val"), val)

def has_page_break(p):
    for br in p._p.iter(qn("w:br")):
        if br.get(qn("w:type")) == "page":
            return True
    return False

def remove_page_break_elements(p):
    for br in list(p._p.iter(qn("w:br"))):
        if br.get(qn("w:type")) == "page":
            parent = br.getparent()
            parent.remove(br)

# ─────────────────────────────────────────────────────────────────────────────
print("Loading …")
doc = Document(str(SRC))
body = doc.element.body

INTRO_PAT = re.compile(r"^1[\.\s]+INTRODUCTION", re.IGNORECASE)
main_body_start_idx = None
for idx, child in enumerate(body):
    tag = child.tag.split("}")[-1]
    if tag == "p":
        p = DocxParagraph(child, doc)
        if INTRO_PAT.match(para_text(p)):
            main_body_start_idx = idx
            print(f"  Main body start: child index {idx}")
            break

if main_body_start_idx is None:
    sys.exit("ERROR: Could not locate '1. INTRODUCTION'")

# ─────────────────────────────────────────────────────────────────────────────
# Step 1: Bullet alignment → explicit LEFT override
# ─────────────────────────────────────────────────────────────────────────────
print("\nStep 1: fixing bullet alignment (explicit jc=left) …")
bullet_fixed = 0

for idx, child in enumerate(list(body)):
    if idx < main_body_start_idx:
        continue
    tag = child.tag.split("}")[-1]
    if tag != "p":
        continue
    p = DocxParagraph(child, doc)
    if is_bullet(p) and not is_heading_style(p):
        # Check current paragraph-level jc (not inherited)
        pPr = p._p.find(qn("w:pPr"))
        cur_jc = None
        if pPr is not None:
            jc_el = pPr.find(qn("w:jc"))
            if jc_el is not None:
                cur_jc = jc_el.get(qn("w:val"), "")
        # If no explicit jc (inherits JUSTIFY from Normal), or is justify/distribute → force left
        if cur_jc is None or cur_jc in ("both", "distribute"):
            set_jc(p, "left")
            bullet_fixed += 1

print(f"  Fixed: {bullet_fixed}")

# ─────────────────────────────────────────────────────────────────────────────
# Step 2: Distributed → fix
# ─────────────────────────────────────────────────────────────────────────────
print("\nStep 2: fixing distributed alignment …")
distributed_fixed = 0

for idx, child in enumerate(list(body)):
    if idx < main_body_start_idx:
        continue
    tag = child.tag.split("}")[-1]
    if tag != "p":
        continue
    p = DocxParagraph(child, doc)
    pPr = p._p.find(qn("w:pPr"))
    if pPr is not None:
        jc_el = pPr.find(qn("w:jc"))
        if jc_el is not None and jc_el.get(qn("w:val"), "") == "distribute":
            new_val = "left" if is_bullet(p) else "both"
            jc_el.set(qn("w:val"), new_val)
            distributed_fixed += 1

print(f"  Fixed: {distributed_fixed}")

# ─────────────────────────────────────────────────────────────────────────────
# Step 3: Trim excessive para spacing
# ─────────────────────────────────────────────────────────────────────────────
print("\nStep 3: trimming excessive spacing …")
spacing_fixed = 0

for idx, child in enumerate(list(body)):
    if idx < main_body_start_idx:
        continue
    tag = child.tag.split("}")[-1]
    if tag != "p":
        continue
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
            if before > 240:
                sp.set(qn("w:before"), "0")
                changed = True
            if after > 160:
                sp.set(qn("w:after"), "80")
                changed = True
            if changed:
                spacing_fixed += 1

print(f"  Fixed: {spacing_fixed}")

# ─────────────────────────────────────────────────────────────────────────────
# Step 4: Merge Table 2.1 Part 1 and Part 2
# ─────────────────────────────────────────────────────────────────────────────
print("\nStep 4: merging Table 2.1 …")

def get_preceding_text(children_list, tbl_idx, look_back=4):
    for i in range(tbl_idx - 1, max(-1, tbl_idx - look_back - 1), -1):
        child = children_list[i]
        tag = child.tag.split("}")[-1]
        if tag == "p":
            p = DocxParagraph(child, doc)
            t = para_text(p)
            if t:
                return t
    return ""

body_children = list(body)
table_entries = []
for i, child in enumerate(body_children):
    if i < main_body_start_idx:
        continue
    tag = child.tag.split("}")[-1]
    if tag == "tbl":
        prec = get_preceding_text(body_children, i)
        table_entries.append((i, child, prec))

part1_idx, part1_elem = None, None
part2_idx, part2_elem = None, None

for i, elem, prec in table_entries:
    if part1_elem is None and "Part 1" in prec:
        part1_idx, part1_elem = i, elem
        print(f"  Part 1 at body index {i}: '{prec[:60]}'")
    elif part1_elem is not None and "Part 2" in prec:
        part2_idx, part2_elem = i, elem
        print(f"  Part 2 at body index {i}: '{prec[:60]}'")
        break

merged = False
if part1_elem is not None and part2_elem is not None:
    part2_rows = list(part2_elem.findall(qn("w:tr")))
    rows_moved = 0
    for row in part2_rows[1:]:  # skip repeated header
        part1_elem.append(copy.deepcopy(row))
        rows_moved += 1
    print(f"  Moved {rows_moved} rows")

    children_now = list(body)
    p1_pos = next((i for i, c in enumerate(children_now) if c is part1_elem), None)
    p2_pos = next((i for i, c in enumerate(children_now) if c is part2_elem), None)

    if p1_pos is not None and p2_pos is not None:
        to_remove = children_now[p1_pos + 1 : p2_pos + 1]
        for elem in to_remove:
            body.remove(elem)
        print(f"  Removed {len(to_remove)} elements between tables")
        merged = True

    # Update caption
    children_now2 = list(body)
    p1_pos2 = next((i for i, c in enumerate(children_now2) if c is part1_elem), None)
    if p1_pos2:
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
                    print(f"  Caption updated: '{para_text(p)}'")
                    break
else:
    print("  Could not locate Part1/Part2 tables — skipping")

# ─────────────────────────────────────────────────────────────────────────────
# Step 5: Fix 5.6 → 5.7 spacing
# ─────────────────────────────────────────────────────────────────────────────
print("\nStep 5: Fixing 5.6 → 5.7 (DFD) spacing …")

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
    for look in range(dfd_idx - 1, max(dfd_idx - 5, main_body_start_idx), -1):
        child = children_now[look]
        tag = child.tag.split("}")[-1]
        if tag == "tbl":
            break  # stop at the Fig 5.6 table
        if tag == "p":
            p = DocxParagraph(child, doc)
            txt = para_text(p)
            # Only remove if it's a pure blank spacer with a page-break
            if txt == "" and has_page_break(p):
                remove_page_break_elements(p)
                pg_breaks_removed += 1
                print(f"  Removed page-break from blank para at index {look}")
            elif txt == "":
                body.remove(child)
                pg_breaks_removed += 1
                print(f"  Removed blank para at index {look}")

print(f"  Removed: {pg_breaks_removed} elements")

# ─────────────────────────────────────────────────────────────────────────────
# Save
# ─────────────────────────────────────────────────────────────────────────────
print(f"\nSaving to: {DST}")
doc.save(str(DST))
print("Done.")
print(f"\n=== SUMMARY ===")
print(f"  bullet_align_fixed:  {bullet_fixed}")
print(f"  distributed_fixed:   {distributed_fixed}")
print(f"  spacing_trimmed:     {spacing_fixed}")
print(f"  table_2.1_merged:    {merged}")
print(f"  dfd_fix_items:       {pg_breaks_removed}")
