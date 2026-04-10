<#
.SYNOPSIS
    Deploy binjaXfrida to the Binary Ninja plugins directory and
    restart Binary Ninja.

.DESCRIPTION
    Copies the plugin files from the development directory into
    the user plugins folder, overwriting any existing version,
    then restarts Binary Ninja so the changes take effect.

    The script aborts on any error; every destructive or I/O step
    is followed by a validation check.
#>

param(
    [string]$BinjaPluginsDir = "$env:APPDATA\Binary Ninja\plugins",
    [switch]$NoRestart
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

function Abort([string]$Message) {
    Write-Host "[install] FATAL: $Message" -ForegroundColor Red
    exit 1
}

# --- Resolve paths ---
$ScriptDir = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Definition)
$PluginName = "binjaXfrida"
$TargetDir = Join-Path $BinjaPluginsDir $PluginName

Write-Host "[install] Source:  $ScriptDir" -ForegroundColor Cyan
Write-Host "[install] Target:  $TargetDir" -ForegroundColor Cyan

# --- Validate source directory ---
if (-not (Test-Path $ScriptDir)) {
    Abort "Source directory does not exist: $ScriptDir"
}

# --- Validate plugins parent directory ---
if (-not (Test-Path $BinjaPluginsDir)) {
    Abort "Binary Ninja plugins directory does not exist: $BinjaPluginsDir"
}

# --- Validate required source items exist before doing anything ---
$items = @(
    "__init__.py",
    "log.py",
    "plugin.json",
    "LICENSE",
    "core",
    "actions",
    "ui",
    "templates"
)

foreach ($item in $items) {
    $src = Join-Path $ScriptDir $item
    if (-not (Test-Path $src)) {
        Abort "Required item '$item' not found at: $src"
    }
}
Write-Host "[install] All required source items verified." -ForegroundColor Green

# --- Clean previous install ---
if (Test-Path $TargetDir) {
    Write-Host "[install] Removing existing plugin folder..." -ForegroundColor Yellow
    Remove-Item -Recurse -Force $TargetDir

    if (Test-Path $TargetDir) {
        Abort "Failed to remove existing plugin folder: $TargetDir"
    }
    Write-Host "[install] Existing folder removed." -ForegroundColor Green
} else {
    Write-Host "[install] No existing plugin folder found (clean install)." -ForegroundColor Green
}

# --- Create fresh target directory ---
New-Item -ItemType Directory -Path $TargetDir -Force | Out-Null

if (-not (Test-Path $TargetDir)) {
    Abort "Failed to create target directory: $TargetDir"
}

$contents = @(Get-ChildItem -Path $TargetDir -Force)
if ($contents.Count -ne 0) {
    Abort "Target directory is not empty after creation: $TargetDir"
}
Write-Host "[install] Target directory created and verified empty." -ForegroundColor Green

# --- Copy items ---
foreach ($item in $items) {
    $src = Join-Path $ScriptDir $item
    $dst = Join-Path $TargetDir $item

    if (Test-Path $src -PathType Container) {
        Copy-Item -Recurse -Force $src $dst
    } else {
        Copy-Item -Force $src $dst
    }

    if (-not (Test-Path $dst)) {
        Abort "Failed to copy '$item' to: $dst"
    }
    Write-Host "[install] Copied $item" -ForegroundColor Green
}

# --- Remove __pycache__ directories from the copy ---
Get-ChildItem -Path $TargetDir -Recurse -Directory -Filter "__pycache__" |
    ForEach-Object {
        Write-Host "[install] Removing __pycache__: $($_.FullName)" -ForegroundColor Yellow
        Remove-Item -Recurse -Force $_.FullName

        if (Test-Path $_.FullName) {
            Abort "Failed to remove __pycache__: $($_.FullName)"
        }
    }

Write-Host "[install] Plugin deployed successfully!" -ForegroundColor Green

# --- Restart Binary Ninja ---
if ($NoRestart) {
    Write-Host "[install] Skipping Binary Ninja restart (-NoRestart)." -ForegroundColor Yellow
    return
}

$bnProcess = Get-Process -Name "binaryninja" -ErrorAction SilentlyContinue
if ($bnProcess) {
    Write-Host "[install] Stopping Binary Ninja (PID: $($bnProcess.Id))..." -ForegroundColor Yellow
    $bnProcess | Stop-Process -Force
    Start-Sleep -Seconds 2

    $stillRunning = Get-Process -Name "binaryninja" -ErrorAction SilentlyContinue
    if ($stillRunning) {
        Abort "Failed to stop Binary Ninja (PID: $($stillRunning.Id))."
    }
    Write-Host "[install] Binary Ninja stopped." -ForegroundColor Green
} else {
    Write-Host "[install] Binary Ninja is not running." -ForegroundColor Yellow
}

$searchPaths = @(
    "$env:LOCALAPPDATA\Programs\Vector35\BinaryNinja",
    "C:\Program Files\Vector35\BinaryNinja",
    "C:\Program Files (x86)\Vector35\BinaryNinja"
)

$bnExe = $null
foreach ($dir in $searchPaths) {
    if (Test-Path $dir) {
        $bnExe = Get-ChildItem $dir -Filter "binaryninja.exe" -Recurse -ErrorAction SilentlyContinue |
            Select-Object -First 1
        if ($bnExe) { break }
    }
}

if (-not $bnExe) {
    $bnExe = Get-Command "binaryninja" -ErrorAction SilentlyContinue
}

if ($bnExe) {
    $exePath = if ($bnExe -is [System.IO.FileInfo]) { $bnExe.FullName } else { $bnExe.Source }
    Write-Host "[install] Starting Binary Ninja: $exePath" -ForegroundColor Cyan
    Start-Process $exePath
} else {
    Write-Host "[install] Could not locate binaryninja.exe. Please start it manually." -ForegroundColor Yellow
}
