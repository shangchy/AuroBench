# One-click deploy script: ollama + models + eval scripts
# Usage: double-click setup.bat, or run: powershell -ExecutionPolicy Bypass -File setup.ps1

$ErrorActionPreference = "Stop"

$models = @(
    "qwen2.5:1.5b",
    "qwen2.5:3b",
    "deepseek-r1:1.5b",
    "qwen2.5:7b",
    "llama3.2:3b",
    "gemma2:2b"
)

$modelDir = "D:\ollama\models"

function Write-Step($msg) {
    Write-Host ""
    Write-Host "=== $msg ===" -ForegroundColor Cyan
}

function Test-Command($cmd) {
    return [bool](Get-Command $cmd -ErrorAction SilentlyContinue)
}

function Refresh-Path {
    $env:Path = [System.Environment]::GetEnvironmentVariable("Path", "Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path", "User")
}

Write-Step "1/7 Detect hardware"
$gpu = Get-CimInstance win32_VideoController -ErrorAction SilentlyContinue | Where-Object { $_.Name -match "NVIDIA|AMD|Arc" }
if ($gpu) {
    Write-Host "GPU detected: $($gpu.Name) - ollama will use GPU acceleration" -ForegroundColor Green
} else {
    Write-Host "No discrete GPU detected - CPU inference (7B models will be slow)" -ForegroundColor Yellow
}

Write-Step "2/7 Check/install Ollama"
if (Test-Command ollama) {
    Write-Host "Ollama already installed: $(ollama --version)"
} elseif (Test-Command winget) {
    Write-Host "Installing Ollama via winget ..."
    winget install --id Ollama.Ollama -e --accept-source-agreements --accept-package-agreements
    Refresh-Path
    if (-not (Test-Command ollama)) {
        $ollamaPath = Join-Path $env:LOCALAPPDATA "Programs\Ollama\ollama.exe"
        if (Test-Path $ollamaPath) { $env:Path += ";$(Split-Path $ollamaPath)" }
    }
} else {
    throw "Neither ollama nor winget found. Install Ollama manually from https://ollama.com/download"
}
if (-not (Test-Command ollama)) { throw "Ollama install failed" }

Write-Step "3/7 Configure model directory (D: drive)"
if (-not (Test-Path $modelDir)) { New-Item -ItemType Directory -Path $modelDir -Force | Out-Null }
[System.Environment]::SetEnvironmentVariable("OLLAMA_MODELS", $modelDir, "User")
$env:OLLAMA_MODELS = $modelDir
Write-Host "Models will be stored at: $modelDir" -ForegroundColor Green
Write-Host "C: drive is not used for model storage." -ForegroundColor Green

Write-Step "4/7 Start Ollama service"
$ready = $false
try { ollama list *> $null; $ready = $true } catch {}
if (-not $ready) {
    Write-Host "Starting 'ollama serve' in background ..."
    Start-Process ollama -ArgumentList "serve" -WindowStyle Hidden
    for ($i = 0; $i -lt 30; $i++) {
        Start-Sleep -Seconds 2
        try { ollama list *> $null; $ready = $true; break } catch {}
    }
    if (-not $ready) { throw "Ollama service failed to start" }
}
Write-Host "Ollama service is ready" -ForegroundColor Green

Write-Step "5/7 Pull models"
$installed = ollama list
foreach ($m in $models) {
    if ($installed -match [regex]::Escape($m)) {
        Write-Host "  skip (already present): $m" -ForegroundColor Gray
    } else {
        Write-Host "  pulling: $m" -ForegroundColor Yellow
        ollama pull $m
        if ($LASTEXITCODE -ne 0) { Write-Host "  pull FAILED: $m" -ForegroundColor Red }
    }
}

Write-Step "6/7 Install Python dependencies"
if (-not (Test-Command python)) {
    throw "Python not found. Install Python 3.10+ and add it to PATH first."
}
python -m pip install --quiet requests
Write-Host "Dependency installed: requests"

Write-Step "7/7 Deploy eval scripts"
$evalSrc = Join-Path $PSScriptRoot "..\scripts\eval"
$evalDst = Join-Path $env:USERPROFILE "llm-eval"
if (Test-Path $evalSrc) {
    if (Test-Path $evalDst) { Remove-Item $evalDst -Recurse -Force }
    New-Item -ItemType Directory -Path $evalDst -Force | Out-Null
    Copy-Item (Join-Path $evalSrc "*") $evalDst -Recurse -Force
    Write-Host "Eval scripts deployed to: $evalDst" -ForegroundColor Green
} else {
    Write-Host "WARNING: eval scripts not found at $evalSrc" -ForegroundColor Yellow
    Write-Host "Copy scripts\eval next to setup.ps1 before distributing." -ForegroundColor Yellow
}

Write-Step "DONE"
Write-Host ""
Write-Host "To run the evaluation:" -ForegroundColor Cyan
Write-Host "  cd $env:USERPROFILE\llm-eval"
Write-Host "  python main.py"
Write-Host ""
Write-Host "Installed models:" -ForegroundColor Cyan
ollama list
