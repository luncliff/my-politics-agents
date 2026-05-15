# Claude Code SessionStart hook
# 세션 시작 시 지역 정보와 데이터 클론 상태를 출력한다.

$loc = if (Test-Path "location.txt") {
    (Get-Content "location.txt" -Raw).Trim()
} else {
    "(location.txt 없음 — 작업 지역을 설정하세요)"
}

$clones = @(
    "보관함/legalize-kr",
    "보관함/ordinance-kr",
    "보관함/precedent-kr",
    "보관함/admrule-kr"
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

# feedback-log에서 마지막 처리 날짜를 확인해 미처리 retro 수를 계산
$feedbackLog = ".goals/feedback-log.md"
$lastFeedback = $null
if (Test-Path $feedbackLog) {
    $dates = Select-String -Path $feedbackLog -Pattern "^## (\d{4}-\d{2}-\d{2})" | ForEach-Object { $_.Matches[0].Groups[1].Value }
    if ($dates) { $lastFeedback = ($dates | Sort-Object -Descending)[0] }
}
$unprocessed = if ($lastFeedback) {
    (Get-ChildItem "retrospectives" -Filter "*.md" | Where-Object {
        $_.Name -match "^(\d{4}-\d{2}-\d{2})" -and $Matches[1] -gt $lastFeedback
    }).Count
} else { $retroCount }

if ($unprocessed -ge 3) {
    Write-Host "피드백 : 미처리 회고 ${unprocessed}건 — /feedback 실행 권장" -ForegroundColor Magenta
}

# 잔여 목표 표시
if (Test-Path ".goals/current.md") {
    $pending = (Select-String -Path ".goals/current.md" -Pattern "^- \[ \]" -ErrorAction SilentlyContinue).Count
    if ($pending -gt 0) {
        Write-Host "목표   : 잔여 ${pending}건 — /goal 로 확인" -ForegroundColor Green
    }
}

Write-Host "슬래시 커맨드: /health /brief /retro /collect /persona-review" -ForegroundColor DarkGray
Write-Host "=================================" -ForegroundColor Cyan
Write-Host ""
