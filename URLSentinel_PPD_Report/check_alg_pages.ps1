$word = New-Object -ComObject Word.Application
$word.Visible = $false
try {
    $doc = $word.Documents.Open('z:\URLSentinel\URLSentinel_PPD_Report\test_single_space.docx')
    $pdfPath = 'z:\URLSentinel\URLSentinel_PPD_Report\test_single_space.pdf'
    $doc.SaveAs([ref]$pdfPath, [ref]17)
    $pageCount = $doc.ComputeStatistics(2)
    Write-Host ("Total pages: " + $pageCount)
    for ($i = 1; $i -le $doc.Paragraphs.Count; $i++) {
        $p = $doc.Paragraphs.Item($i)
        $txt = $p.Range.Text.Trim()
        if ($txt -match 'Table 2\.1|6\.2|6\.3|6\.4|6\.5|Algorithm|Fig\. 6\.3|Fig\. 6\.4') {
            $page = $p.Range.Information(3)
            $len = [Math]::Min(80, $txt.Length)
            Write-Host ("Page " + $page + ": " + $txt.Substring(0, $len))
        }
    }
} finally {
    if ($doc) { $doc.Close([ref]$false) }
    $word.Quit()
}
