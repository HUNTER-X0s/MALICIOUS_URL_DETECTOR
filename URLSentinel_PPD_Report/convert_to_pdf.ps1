
$word = New-Object -ComObject Word.Application
$word.Visible = $false
try {
    $doc = $word.Documents.Open('z:\URLSentinel\URLSentinel_PPD_Report\URLSentinel_PPD_Report.docx')
    $doc.SaveAs('z:\URLSentinel\URLSentinel_PPD_Report\URLSentinel_PPD_Report.pdf', 17)
    $doc.Close()
    Write-Host "PDF Compilation Succeeded! Target: z:\URLSentinel\URLSentinel_PPD_Report\URLSentinel_PPD_Report.pdf"
} catch {
    Write-Host "Word COM Error: $_"
    exit 1
} finally {
    $word.Quit()
}
