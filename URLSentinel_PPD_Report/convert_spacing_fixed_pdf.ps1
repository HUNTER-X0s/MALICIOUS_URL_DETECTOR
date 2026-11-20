$word = New-Object -ComObject Word.Application
$word.Visible = $false
$word.DisplayAlerts = 0

$docPath = "z:\URLSentinel\URLSentinel_PPD_Report\URLSentinel_PPD_Report_SPACING_FIXED.docx"
$pdfPath = "z:\URLSentinel\URLSentinel_PPD_Report\URLSentinel_PPD_Report_SPACING_FIXED.pdf"

$doc = $word.Documents.Open($docPath, $false, $false)
$doc.SaveAs([ref]$pdfPath, [ref]17)
$doc.Close($false)
$word.Quit()

Write-Host "PDF saved to: $pdfPath"
