# Claude Code PreToolUse(Bash) hook
# 파괴적 명령 패턴을 감지하면 exit 2로 차단한다.
# stdin으로 tool input JSON이 들어온다.

$input_json = $env:CLAUDE_TOOL_INPUT
if (-not $input_json) {
    # stdin에서 읽기 시도
    $input_json = [Console]::In.ReadToEnd()
}

try {
    $tool = $input_json | ConvertFrom-Json
    $cmd = $tool.command
} catch {
    exit 0
}

if (-not $cmd) { exit 0 }

$blocked_patterns = @(
    'rm\s+-rf',
    'git\s+push\s+--force',
    'git\s+push\s+-f\s',
    '\bmkfs\b',
    'curl\s*\|',
    'wget\s*\|',
    'dd\s+if='
)

foreach ($pattern in $blocked_patterns) {
    if ($cmd -match $pattern) {
        Write-Error "BLOCKED: 파괴적 명령 감지 ('$pattern'). 사용자 확인 후 실행하세요."
        exit 2
    }
}

exit 0
