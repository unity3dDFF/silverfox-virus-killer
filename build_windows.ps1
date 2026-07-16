[CmdletBinding()]
param(
    [string]$Python = "python",
    [switch]$SkipInstall
)

$ErrorActionPreference = "Stop"
$ProjectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $ProjectRoot

$Version = (& $Python -c "from version import __version__; print(__version__)").Trim()
if ($Version -notmatch '^\d+\.\d+\.\d+$') {
    throw "Invalid application version: $Version"
}
$CliName = "SilverFoxKiller-v$Version-windows-x64"
$GuiName = "SilverFoxKillerGUI-v$Version-windows-x64"
$ChecksumName = "SHA256SUMS-v$Version.txt"

if (-not $SkipInstall) {
    & $Python -m pip install --upgrade pip
    & $Python -m pip install -r requirements-dev.txt
}

& $Python -m unittest discover -s tests -v
if ($LASTEXITCODE -ne 0) { throw "Tests failed" }

Remove-Item -Recurse -Force build, dist -ErrorAction SilentlyContinue
$SpecPath = Join-Path $ProjectRoot "build\specs"
New-Item -ItemType Directory -Force $SpecPath | Out-Null

& $Python -m PyInstaller --noconfirm --clean --onefile `
    --specpath $SpecPath `
    --name $CliName `
    --collect-all psutil `
    main.py
if ($LASTEXITCODE -ne 0) { throw "CLI build failed" }

& $Python -m PyInstaller --noconfirm --clean --onefile --windowed `
    --specpath $SpecPath `
    --name $GuiName `
    --collect-all psutil `
    --hidden-import repair.system_repair `
    gui.py
if ($LASTEXITCODE -ne 0) { throw "GUI build failed" }

$checksums = Join-Path $ProjectRoot "dist\$ChecksumName"
Get-ChildItem "$ProjectRoot\dist\*.exe" | ForEach-Object {
    $hash = (Get-FileHash -Algorithm SHA256 -LiteralPath $_.FullName).Hash.ToLowerInvariant()
    "$hash  $($_.Name)"
} | Set-Content -Encoding ascii $checksums

Write-Host "Windows v$Version build complete: $ProjectRoot\dist" -ForegroundColor Green
