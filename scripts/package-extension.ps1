# URLSentinel Browser Extension Packaging Script
# Packages the Manifest V3 extension for Chrome Web Store submission

$ErrorActionPreference = "Stop"

$ProjectRoot = Resolve-Path "$PSScriptRoot\.."
$ExtensionDir = Join-Path $ProjectRoot "apps\extension"
$DistDir = Join-Path $ProjectRoot "dist"
$ZipOutput = Join-Path $DistDir "urlsentinel-extension-v1.0.0.zip"

Write-Host "==> Packaging URLSentinel Browser Extension (MV3)..." -ForegroundColor Cyan

if (-not (Test-Path $DistDir)) {
    New-Item -ItemType Directory -Path $DistDir -Force | Out-Null
}

if (Test-Path $ZipOutput) {
    Remove-Item $ZipOutput -Force
}

# Verify required files exist
$RequiredFiles = @("manifest.json", "background.js", "popup.html", "popup.css", "popup.js", "warning.html", "warning.css", "warning.js")
foreach ($file in $RequiredFiles) {
    $filePath = Join-Path $ExtensionDir $file
    if (-not (Test-Path $filePath)) {
        Write-Error "Missing required file: $filePath"
    }
}

Compress-Archive -Path "$ExtensionDir\*" -DestinationPath $ZipOutput -Force

$ZipSize = (Get-Item $ZipOutput).Length / 1KB
Write-Host "==> Extension package successfully created: $ZipOutput ($([math]::Round($ZipSize, 1)) KB)" -ForegroundColor Green

