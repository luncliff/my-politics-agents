# Claude Code SessionStart hook
# 세션 시작 시 지역 정보와 데이터 클론 상태를 출력한다.

$loc = if (Test-Path "location.txt") {
    (Get-Content "location.txt" -Raw).Trim()
} else {
    "(location.txt 없음 — 작업 지역을 설정하세요)"
}

$clones = @(
    "data/legalize-kr",
    "data/ordinance-kr",
    "data/precedent-kr",
    "data/admrule-kr"
)

Write-Host ""
Write-Host "=== politics-agents 세션 시작 ===" -ForegroundColor Cyan
Write-Host "지역  : $loc" -ForegroundColor Yellow
Write-Host "데이터 클론 상태:"
foreach ($c in $clones) {
    $ok = Test-Path "$c/.git"
    $icon = if ($ok) { "✅" } else { "❌" }
    $hint = if (-not $ok) { "  ← civic: fetch legalize-kr repos 실행 필요" } else { "" }
    Write-Host "  $icon $c$hint"
}

$retroCount = (Get-ChildItem "retrospectives" -Filter "*.md" -ErrorAction SilentlyContinue).Count
Write-Host "회고   : retrospectives/ 내 $retroCount 건"
Write-Host "슬래시 커맨드: /health /brief /retro /collect /persona-review" -ForegroundColor DarkGray
Write-Host "=================================" -ForegroundColor Cyan
Write-Host ""
