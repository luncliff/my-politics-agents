# log-prompt.ps1 — userPromptSubmitted 로그 (메타데이터만)
$ErrorActionPreference = 'Stop'

$logDir = Join-Path -Path (Get-Location) -ChildPath '.github/hooks/logs'
New-Item -ItemType Directory -Force -Path $logDir | Out-Null

$ts  = (Get-Date).ToUniversalTime().ToString('yyyy-MM-ddTHH:mm:ssZ')
$cwd = (Get-Location).Path
$len = [int]($env:COPILOT_PROMPT_LENGTH | ForEach-Object { if ($_) { $_ } else { 0 } })

$entry = @{ ts = $ts; cwd = $cwd; prompt_len = $len } | ConvertTo-Json -Compress
Add-Content -Path (Join-Path $logDir 'audit.jsonl') -Value $entry
exit 0
