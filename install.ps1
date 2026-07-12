# Aether - Sovereign Edge AI + Computer Use installer (Windows / PowerShell)
#
# One-line install (PowerShell):
#   irm https://raw.githubusercontent.com/fivepanelhat/Aether/main/install.ps1 | iex
#
# Or from a clone:
#   powershell -ExecutionPolicy Bypass -File .\install.ps1
#
# Creates an isolated virtualenv, installs Aether with the computer-use extras,
# exposes the `aether` command, and checks for a local Ollama runtime. Aether
# runs entirely on-device - no screenshots or keystrokes leave the machine.

$ErrorActionPreference = "Stop"

$RepoUrl    = if ($env:AETHER_REPO_URL) { $env:AETHER_REPO_URL } else { "https://github.com/fivepanelhat/Aether.git" }
$InstallDir = if ($env:AETHER_HOME)     { $env:AETHER_HOME }     else { Join-Path $env:USERPROFILE ".aether-app" }
$VenvDir    = Join-Path $InstallDir "venv"
$BinDir     = Join-Path $env:USERPROFILE ".local\bin"

function Info($m) { Write-Host "[aether] $m" -ForegroundColor Cyan }
function Warn($m) { Write-Host "[aether] $m" -ForegroundColor Yellow }
function Fail($m) { Write-Host "[aether] $m" -ForegroundColor Red; exit 1 }

# ---- 1. Python ----
$PythonBin = $null
foreach ($cand in @("python", "python3", "py")) {
    if (Get-Command $cand -ErrorAction SilentlyContinue) { $PythonBin = $cand; break }
}
if (-not $PythonBin) { Fail "Python 3.10+ is required but was not found. Install from https://python.org and re-run." }
$PyVer = & $PythonBin -c "import sys; print('%d.%d' % sys.version_info[:2])"
Info "Using Python $PyVer ($PythonBin)"

# ---- 2. Source: clone or in-place ----
if ((Test-Path "pyproject.toml") -and (Select-String -Path "pyproject.toml" -Pattern 'name = "aether"' -Quiet)) {
    $SrcDir = (Get-Location).Path
    Info "Installing from current checkout: $SrcDir"
} else {
    if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
        Fail "git is required to fetch Aether. Install git or run this script from a clone."
    }
    New-Item -ItemType Directory -Force -Path $InstallDir | Out-Null
    $SrcDir = Join-Path $InstallDir "src"
    if (Test-Path (Join-Path $SrcDir ".git")) {
        Info "Updating existing checkout in $SrcDir"
        git -C $SrcDir pull --ff-only 2>$null
    } else {
        Info "Cloning $RepoUrl"
        git clone --depth 1 $RepoUrl $SrcDir
    }
}

# ---- 3. Virtualenv ----
Info "Creating virtualenv at $VenvDir"
& $PythonBin -m venv $VenvDir
$VenvPython = Join-Path $VenvDir "Scripts\python.exe"
$VenvAether = Join-Path $VenvDir "Scripts\aether.exe"
& $VenvPython -m pip install --upgrade pip | Out-Null

# ---- 4. Install with computer-use extras ----
Info "Installing aether[computer] (edge AI + desktop control)"
& $VenvPython -m pip install "$SrcDir[computer]"

# ---- 5. Bundle skills ----
Info "Installing bundled skills"
try { & $VenvAether init --user-only } catch { Warn "Skill install skipped (non-fatal)." }

# ---- 6. Launcher on PATH ----
New-Item -ItemType Directory -Force -Path $BinDir | Out-Null
$Shim = Join-Path $BinDir "aether.cmd"
"@echo off`r`n`"$VenvAether`" %*" | Set-Content -Encoding ASCII $Shim
Info "Installed launcher: $Shim"
$userPath = [Environment]::GetEnvironmentVariable("Path", "User")
if ($userPath -notlike "*$BinDir*") {
    [Environment]::SetEnvironmentVariable("Path", "$BinDir;$userPath", "User")
    Warn "Added $BinDir to your user PATH. Open a new terminal for it to take effect."
}

# ---- 7. Ollama check (edge AI runtime) ----
if (Get-Command ollama -ErrorAction SilentlyContinue) {
    Info "Ollama detected."
} else {
    Warn "Ollama not found. Install the local model runtime from https://ollama.com"
    Warn "Then pull models:  ollama pull qwen2.5-coder:7b ;  ollama pull qwen2.5-vl:7b"
}

Write-Host ""
Info "Done. Verify your setup with:"
Write-Host "    aether doctor"
Write-Host ""
Info "Try computer use:"
Write-Host "    aether computer run `"Open Notepad and type kia ora`""
Write-Host "    aether computer shot screen.png        # deterministic, no model needed"
