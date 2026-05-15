#requires -Version 7.0
<#!
.SYNOPSIS
  Shallow clone legalize-kr repositories into 보관함/.

.PARAMETER DryRun
  Print planned actions only.
#>
param(
  [switch]$DryRun
)

$ErrorActionPreference = 'Stop'
. (Join-Path $PSScriptRoot 'common.ps1')

$repoRoot = Get-RepoRoot
Set-Location $repoRoot

$repos = @(
  @{ Name = 'legalize-kr'; Url = 'https://github.com/legalize-kr/legalize-kr.git' }
  @{ Name = 'precedent-kr'; Url = 'https://github.com/legalize-kr/precedent-kr.git' }
  @{ Name = 'admrule-kr'; Url = 'https://github.com/legalize-kr/admrule-kr.git' }
  @{ Name = 'ordinance-kr'; Url = 'https://github.com/legalize-kr/ordinance-kr.git' }
)
$archiveDir = Join-Path $repoRoot '보관함'

if ($DryRun) {
  foreach ($repo in $repos) {
    $targetDir = Join-Path $archiveDir $repo.Name
    Write-Info "(dry-run) would shallow clone $($repo.Url) into $targetDir"
  }
  return
}

New-Item -ItemType Directory -Path $archiveDir -Force | Out-Null

# ordinance-kr and other repositories contain files with special characters in their names, which causes issues on Windows.
git config --global core.protectNTFS false

foreach ($repo in $repos) {
  $targetDir = Join-Path $archiveDir $repo.Name
  if (Test-Path (Join-Path $targetDir '.git')) {
    Write-Warn2 "already exists: $targetDir"
    continue
  }

  if (Test-Path $targetDir) {
    Write-Warn2 "target exists (not a git repo): $targetDir"
    continue
  }

  git clone --depth 1 $repo.Url $targetDir
  Write-Ok "ready: $targetDir"
}

# back to default value for safety
git config --global core.protectNTFS true
