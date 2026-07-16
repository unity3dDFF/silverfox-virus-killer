[CmdletBinding()]
param(
    [string]$Python = "python",
    [switch]$SkipInstall
)

$ErrorActionPreference = "Stop"
$ProjectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $ProjectRoot

if (-not $SkipInstall) {
    & $Python -m pip install --upgrade pip
    & $Python -m pip install -r requirements-dev.txt
}

& $Python -m unittest discover -s tests -v
if ($LASTEXITCODE -ne 0) { throw "Tests failed" }

Remove-Item -Recurse -Force build, dist -ErrorAction SilentlyContinue

& $Python -m PyInstaller --noconfirm --clean --onefile `
    --name SilverFoxKiller `
    --collect-all psutil `
    main.py
if ($LASTEXITCODE -ne 0) { throw "CLI build failed" }

& $Python -m PyInstaller --noconfirm --clean --onefile --windowed `
    --name SilverFoxKillerGUI `
    --collect-all psutil `
    --hidden-import repair.system_repair `
    gui.py
if ($LASTEXITCODE -ne 0) { throw "GUI build failed" }

$checksums = Join-Path $ProjectRoot "dist\SHA256SUMS.txt"
Get-ChildItem "$ProjectRoot\dist\*.exe" | ForEach-Object {
    $hash = (Get-FileHash -Algorithm SHA256 -LiteralPath $_.FullName).Hash.ToLowerInvariant()
    "$hash  $($_.Name)"
} | Set-Content -Encoding ascii $checksums

Write-Host "Windows build complete: $ProjectRoot\dist" -ForegroundColor Green
