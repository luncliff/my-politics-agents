# Claude Code Stop hook
# 오늘 날짜의 회고 파일이 없으면 /retro 실행을 안내한다.

$today = Get-Date -Format "yyyy-MM-dd"
$hasRetro = Get-ChildItem "retrospectives" -Filter "$today*.md" -ErrorAction SilentlyContinue

if (-not $hasRetro) {
    Write-Host ""
    Write-Host "[알림] 오늘($today) 세션 회고가 없습니다." -ForegroundColor Yellow
    Write-Host "       /retro 커맨드로 회고를 작성해 주세요." -ForegroundColor Yellow
    Write-Host ""
}
