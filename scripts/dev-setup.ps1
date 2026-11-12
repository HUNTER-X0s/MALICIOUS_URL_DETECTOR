# URLSentinel Local Development Setup (Windows PowerShell)

Write-Host "=========================================" -ForegroundColor Cyan
Write-Host "  URLSentinel Secure Development Setup   " -ForegroundColor Cyan
Write-Host "=========================================" -ForegroundColor Cyan

# 1. Verify Docker
if (Get-Command docker -ErrorAction SilentlyContinue) {
    Write-Host "[OK] Docker CLI detected" -ForegroundColor Green
}
else {
    Write-Host "[WARN] Docker not detected in PATH. Ensure Docker Desktop is running for containerized Postgres/Redis." -ForegroundColor Yellow
}

# 2. Check / Setup Python Virtual Environment
if (Test-Path "z:\URLSentinel\.venv") {
    Write-Host "[OK] Python virtual environment located at z:\URLSentinel\.venv" -ForegroundColor Green
}
else {
    Write-Host "Creating Python virtual environment in .venv..." -ForegroundColor Yellow
    python -m venv z:\URLSentinel\.venv
}

# 3. Environment configuration
if (-not (Test-Path "z:\URLSentinel\.env")) {
    Copy-Item "z:\URLSentinel\.env.example" "z:\URLSentinel\.env"
    Write-Host "[OK] Generated .env from .env.example" -ForegroundColor Green
}

Write-Host "`nSetup complete! You can run tests using:" -ForegroundColor Cyan
Write-Host "  z:\URLSentinel\.venv\Scripts\pytest.exe z:\URLSentinel\services\api\tests -v" -ForegroundColor White
Write-Host "Or start containers via:" -ForegroundColor Cyan
Write-Host "  docker-compose up -d postgres redis" -ForegroundColor White

