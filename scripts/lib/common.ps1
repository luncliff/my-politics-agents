# scripts/lib/common.ps1 — PowerShell 공용 헬퍼
$ErrorActionPreference = 'Stop'

function Write-Info  { param([string]$m) Write-Host "[info] $m" -ForegroundColor Cyan }
function Write-Warn2 { param([string]$m) Write-Host "[warn] $m" -ForegroundColor Yellow }
function Write-Err   { param([string]$m) Write-Host "[err ] $m" -ForegroundColor Red }
function Write-Ok    { param([string]$m) Write-Host "[ok  ] $m" -ForegroundColor Green }

function Test-Have { param([string]$cmd) [bool](Get-Command $cmd -ErrorAction SilentlyContinue) }

function Confirm-Action {
  param(
    [Parameter(Mandatory = $true)][string]$Question,
    [bool]$DryRun = $false,
    [bool]$AssumeYes = $false
  )
  if ($DryRun)    { Write-Info "(dry-run) would ask: $Question"; return $false }
  if ($AssumeYes) { Write-Info "(-Yes) auto-accept: $Question"; return $true }
  $ans = Read-Host "$Question [y/N]"
  return ($ans -match '^(y|Y|yes|YES)$')
}

function Get-RepoRoot {
  try { (git rev-parse --show-toplevel) 2>$null } catch { (Get-Location).Path }
}
