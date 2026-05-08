#requires -Version 7.0
<#!
.SYNOPSIS
  Shallow clone legalize-kr repositories into data/.

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

$repos = @(
  @{ Name = 'legalize-kr'; Url = 'https://github.com/legalize-kr/legalize-kr.git' }
  @{ Name = 'precedent-kr'; Url = 'https://github.com/legalize-kr/precedent-kr.git' }
  @{ Name = 'admrule-kr'; Url = 'https://github.com/legalize-kr/admrule-kr.git' }
  @{ Name = 'ordinance-kr'; Url = 'https://github.com/legalize-kr/ordinance-kr.git' }
)
$dataDir = Join-Path $repoRoot 'data'

if ($DryRun) {
  foreach ($repo in $repos) {
    $targetDir = Join-Path $dataDir $repo.Name
    Write-Info "(dry-run) would shallow clone $($repo.Url) into $targetDir"
  }
  return
}

New-Item -ItemType Directory -Path $dataDir -Force | Out-Null

foreach ($repo in $repos) {
  $targetDir = Join-Path $dataDir $repo.Name
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
