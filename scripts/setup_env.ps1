# Proje kökünden çalıştırın:  powershell -ExecutionPolicy Bypass -File scripts\setup_env.ps1
$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
Set-Location $Root

function Find-Python {
    $candidates = @(
        (Join-Path $env:LOCALAPPDATA "Programs\Python\Python312\python.exe"),
        (Join-Path $env:LOCALAPPDATA "Programs\Python\Python311\python.exe"),
        (Join-Path $env:LOCALAPPDATA "Programs\Python\Python310\python.exe")
    )
    foreach ($p in $candidates) {
        if (Test-Path $p) { return $p }
    }
    $pyLauncher = Get-Command py -ErrorAction SilentlyContinue
    if ($pyLauncher) {
        $v = & py -3 -c "import sys; print(sys.executable)" 2>$null
        if ($v) { return $v.Trim() }
    }
    $pythonCmd = Get-Command python -ErrorAction SilentlyContinue
    if ($pythonCmd -and $pythonCmd.Source -notmatch "WindowsApps") {
        return $pythonCmd.Source
    }
    return $null
}

$PythonExe = Find-Python
if (-not $PythonExe) {
    Write-Host "Python bulunamadı. Kurulum için (yönetici PowerShell):" -ForegroundColor Yellow
    Write-Host '  winget install --id Python.Python.3.12 -e --accept-package-agreements' -ForegroundColor Cyan
    Write-Host "Kurulumdan sonra bu terminali kapatıp yeniden açin veya oturumu yenileyin." -ForegroundColor Yellow
    exit 1
}

Write-Host "Python: $PythonExe"
& $PythonExe --version

$VenvDir = Join-Path $Root ".venv"
if (-not (Test-Path $VenvDir)) {
    Write-Host "Sanal ortam olusturuluyor: $VenvDir"
    & $PythonExe -m venv $VenvDir
}

$VenvPython = Join-Path $VenvDir "Scripts\python.exe"
if (-not (Test-Path $VenvPython)) {
    Write-Host "Hata: .venv\Scripts\python.exe yok." -ForegroundColor Red
    exit 1
}

Write-Host "pip guncelleniyor..."
& $VenvPython -m pip install -U pip setuptools wheel

Write-Host "Proje bagimliliklari kuruluyor (editable)..."
& $VenvPython -m pip install -e ".[dev]"

Write-Host ""
Write-Host "Tamam. Aktive etmek icin:" -ForegroundColor Green
Write-Host "  .\.venv\Scripts\Activate.ps1" -ForegroundColor Cyan
Write-Host "Sonra:" -ForegroundColor Green
Write-Host "  metadata-cleaner --help" -ForegroundColor Cyan
Write-Host "  python src\gui_pyside.py" -ForegroundColor Cyan
Write-Host "  python -m pytest tests -v" -ForegroundColor Cyan
