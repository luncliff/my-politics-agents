#requires -Version 7.0
<#
.SYNOPSIS
  my-politics-agents 환경 설정 (Windows / PowerShell 7).

.DESCRIPTION
  필요한 도구를 점검 → 설치 계획을 보여주고 → 동의를 받은 뒤 설치합니다.
  시스템 전역 변경은 항상 동의를 묻고 진행합니다.

.PARAMETER DryRun
  실제 설치 없이 어떤 작업이 일어날지만 출력.

.PARAMETER Yes
  모든 확인에 yes로 응답 (CI 등 비대화 환경 한정. 기본은 사용 금지).
#>
param(
  [switch]$DryRun,
  [switch]$Yes
)

$ErrorActionPreference = 'Stop'
. (Join-Path $PSScriptRoot 'lib/common.ps1')

$repoRoot = Get-RepoRoot
Set-Location $repoRoot
Write-Info "repo: $repoRoot"

# 1) detect
$status = [ordered]@{}
$status['git']      = Test-Have 'git'
$status['node']     = Test-Have 'node'
$status['gh']       = Test-Have 'gh'
$status['copilot']  = Test-Have 'copilot'
$status['uv']       = Test-Have 'uv'
$status['pwsh']     = Test-Have 'pwsh'
$status['java']     = Test-Have 'java'
$status['winget']   = Test-Have 'winget'
$status['choco']    = Test-Have 'choco'

Write-Host ""
Write-Info "현재 도구 상태:"
$status.GetEnumerator() | ForEach-Object {
  $mark = if ($_.Value) { 'OK ' } else { 'MISS' }
  Write-Host ("  [{0}] {1}" -f $mark, $_.Key)
}

# 2) plan
$plan = @()
if (-not $status['node'])    { $plan += 'Node.js LTS (winget: OpenJS.NodeJS.LTS)' }
if (-not $status['gh'])      { $plan += 'GitHub CLI (winget: GitHub.cli)' }
if (-not $status['uv'])      { $plan += 'uv (winget: astral-sh.uv)' }
if (-not $status['copilot']) { $plan += 'Copilot CLI (npm i -g @github/copilot)' }

Write-Host ""
if ($plan.Count -eq 0) {
  Write-Ok "추가 설치가 필요한 도구가 없습니다."
} else {
  Write-Info "다음 항목을 설치하려고 합니다:"
  $plan | ForEach-Object { Write-Host "  - $_" }
}

# 3) consent + install
$installer = if ($status['winget']) { 'winget' } elseif ($status['choco']) { 'choco' } else { $null }
if ($plan.Count -gt 0 -and -not $installer) {
  Write-Warn2 "winget/choco 둘 다 없어 자동 설치를 건너뜁니다. 위 항목을 수동으로 설치하세요."
}

function Invoke-Step {
  param([string]$desc, [scriptblock]$action)
  if (Confirm-Action -Question "실행할까요? $desc" -DryRun:$DryRun -AssumeYes:$Yes) {
    & $action
    Write-Ok $desc
  } else {
    Write-Warn2 "skip: $desc"
  }
}

if ($installer -and -not $status['node']) {
  Invoke-Step "Node.js LTS 설치 ($installer)" {
    if ($installer -eq 'winget') { winget install -e --id OpenJS.NodeJS.LTS --silent }
    else { choco install -y nodejs-lts }
  }
}
if ($installer -and -not $status['gh']) {
  Invoke-Step "GitHub CLI 설치 ($installer)" {
    if ($installer -eq 'winget') { winget install -e --id GitHub.cli --silent }
    else { choco install -y gh }
  }
}
if ($installer -and -not $status['uv']) {
  Invoke-Step "uv 설치 ($installer)" {
    if ($installer -eq 'winget') { winget install -e --id astral-sh.uv --silent }
    else { choco install -y uv }
  }
}
if (-not $status['copilot']) {
  Invoke-Step "Copilot CLI 전역 설치 (npm i -g @github/copilot)" {
    npm install -g '@github/copilot'
  }
}

# 4) workspace local setup
Invoke-Step "git submodule update --init --recursive" {
  git submodule update --init --recursive
}

if (Test-Path "mcp-servers/gov-archive/pyproject.toml") {
  Invoke-Step "uv sync (mcp-servers/gov-archive)" {
    Push-Location "mcp-servers/gov-archive"
    try { uv sync } finally { Pop-Location }
  }
}

if (-not (Test-Path ".env")) {
  Invoke-Step ".env.example → .env 복사 (값은 직접 채우세요)" {
    Copy-Item ".env.example" ".env"
  }
}

# 5) verify
Write-Host ""
Write-Info "검증:"
foreach ($k in @('git','node','gh','uv','copilot')) {
  if (Test-Have $k) { Write-Ok "$k OK" } else { Write-Warn2 "$k 누락" }
}

Write-Host ""
Write-Ok "setup 완료. 다음 단계:"
Write-Host "  1) gh auth login"
Write-Host "  2) Tasks: Run Task → 'civic: copilot session'"
