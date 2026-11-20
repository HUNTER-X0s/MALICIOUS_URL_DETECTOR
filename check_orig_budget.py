import pypdf

r_orig = pypdf.PdfReader(r'z:\URLSentinel\URLSentinel_PPD_Report\URLSentinel_PPD_Report_FINAL_BACKUP.pdf')
# wait, what was the original 44 page pdf before any changes?
# Let's check URLSentinel_PPD_Report.pdf or URLSentinel_PPD_Report_FINAL.pdf
r_final = pypdf.PdfReader(r'z:\URLSentinel\URLSentinel_PPD_Report\URLSentinel_PPD_Report_FINAL.pdf')
print("URLSentinel_PPD_Report_FINAL.pdf total pages:", len(r_final.pages))

chapters = [
    "1. INTRODUCTION",
    "2. LITERATURE REVIEW",
    "3. SYSTEM ANALYSIS",
    "4. METHODOLOGY",
    "5. SYSTEM DESIGN",
    "6. IMPLEMENTATION",
    "7. TESTING",
    "8. CHALLENGES",
    "9. RESULT AND ANALYSIS",
    "10. CONCLUSION",
    "REFERENCES"
]

print("\n--- Chapters in URLSentinel_PPD_Report_FINAL.pdf ---")
for ch in chapters:
    found = [i+1 for i, p in enumerate(r_final.pages) if ch in p.extract_text()]
    print(f"{ch:25s} -> {found}")
