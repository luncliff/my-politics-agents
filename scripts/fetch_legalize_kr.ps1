#requires -Version 7.0
<#!
.SYNOPSIS
  Shallow clone legalize-kr into data/legalize-kr.

.PARAMETER DryRun
  Print planned actions only.
#>
param(
  [switch]$DryRun
)

$ErrorActionPreference = 'Stop'
. (Join-Path $PSScriptRoot 'lib/common.ps1')

$repoRoot = Get-RepoRoot
Set-Location $repoRoot

$repoUrl = 'https://github.com/legalize-kr/legalize-kr.git'
$dataDir = Join-Path $repoRoot 'data'
$targetDir = Join-Path $dataDir 'legalize-kr'

if ($DryRun) {
  Write-Info "(dry-run) would shallow clone $repoUrl into $targetDir"
  return
}

New-Item -ItemType Directory -Path $dataDir -Force | Out-Null

if (Test-Path (Join-Path $targetDir '.git')) {
  Write-Warn2 "already exists: $targetDir"
  return
}

if (Test-Path $targetDir) {
  Write-Warn2 "target exists (not a git repo): $targetDir"
  return
}

git clone --depth 1 $repoUrl $targetDir

Write-Ok "legalize-kr ready at $targetDir"
