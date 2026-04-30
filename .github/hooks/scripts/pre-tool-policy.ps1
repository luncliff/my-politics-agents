# pre-tool-policy.ps1 — preToolUse 정책 (logging-first, 데모 deny 1개)
$ErrorActionPreference = 'Stop'

$logDir = Join-Path -Path (Get-Location) -ChildPath '.github/hooks/logs'
New-Item -ItemType Directory -Force -Path $logDir | Out-Null

$ts   = (Get-Date).ToUniversalTime().ToString('yyyy-MM-ddTHH:mm:ssZ')
$tool = if ($env:COPILOT_TOOL_NAME) { $env:COPILOT_TOOL_NAME } else { 'unknown' }
$cmd  = $env:COPILOT_TOOL_COMMAND

$entry = @{ ts = $ts; tool = $tool; cmd = $cmd } | ConvertTo-Json -Compress
Add-Content -Path (Join-Path $logDir 'tool-use.jsonl') -Value $entry

if ($env:COPILOT_HOOKS_DENY_DEMO -eq '1' -and $cmd) {
  $danger = @('rm -rf /', 'mkfs', 'dd if=')
  foreach ($p in $danger) {
    if ($cmd -like "*${p}*") {
      [Console]::Error.WriteLine("[hook] denied by policy: $cmd")
      exit 2
    }
  }
}

exit 0
