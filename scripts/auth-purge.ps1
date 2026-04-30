#requires -Version 7.0
<#
.SYNOPSIS
  자격증명·세션 정리 (Windows). 각 단계는 동의를 받아 진행합니다.
#>
param(
  [switch]$DryRun
)
$ErrorActionPreference = 'Stop'
. (Join-Path $PSScriptRoot 'lib/common.ps1')

Write-Info "my-politics-agents auth-purge"
Write-Warn2 "이 스크립트는 자격증명을 삭제할 수 있습니다. 각 단계는 별도 확인을 받습니다."

if (Confirm-Action -Question "gh CLI 로그아웃 (github.com)?" -DryRun:$DryRun) {
  if (Test-Have 'gh') { gh auth logout --hostname github.com } else { Write-Warn2 "gh 미설치" }
}

if (Confirm-Action -Question "워크스페이스의 .copilot/credentials* 파일 삭제?" -DryRun:$DryRun) {
  Get-ChildItem -Path ".copilot" -Filter "credentials*" -ErrorAction SilentlyContinue |
    ForEach-Object { Write-Info "remove $($_.FullName)"; Remove-Item $_.FullName -Force }
}

if (Confirm-Action -Question "사용자 홈의 ~/.copilot/credentials* 파일 삭제?" -DryRun:$DryRun) {
  $home_copilot = Join-Path $HOME ".copilot"
  Get-ChildItem -Path $home_copilot -Filter "credentials*" -ErrorAction SilentlyContinue |
    ForEach-Object { Write-Info "remove $($_.FullName)"; Remove-Item $_.FullName -Force }
}

Write-Info "현재 셸의 토큰성 환경변수 (값은 표시하지 않음):"
'GH_TOKEN','GITHUB_TOKEN','OPENAI_API_KEY','ANTHROPIC_API_KEY' | ForEach-Object {
  if (Get-Item -ErrorAction SilentlyContinue "Env:$_") { Write-Host "  set: $_" } else { Write-Host "  unset: $_" }
}

if (Confirm-Action -Question "Windows Credential Manager의 'github' 항목 나열?" -DryRun:$DryRun) {
  cmdkey /list | Select-String -Pattern 'github' -ErrorAction SilentlyContinue
  Write-Warn2 "삭제는 'cmdkey /delete:<TargetName>' 으로 직접 실행하세요."
}

Write-Host ""
Write-Ok "완료. VS Code에서 'Chat: Reset Tool Confirmations'도 한 번 실행하세요."
