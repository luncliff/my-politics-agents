---
description: 웹사이트 자료를 수집하고 archive/raw에 보존
tools: [read, search, web/fetch, browser, gov-archive/archive_cite, gov-archive/archive_fetch, ms-vscode.vscode-websearchforcopilot/websearch]
---

# 사이트 수집 (collect-site)

목표: 지정된 URL(들)에서 자료를 가져와 `archive/raw/<host>/`에
원본+해시로 보존하고, 인용 메타를 `archive/processed/<slug>/source.md`에 남긴다.

파일명에는 수집일 접두어를 붙이지 않으며, 시간순 정렬은 `.meta.json`의 `collected_at`으로 처리한다.

## 입력

- `urls`: 수집할 URL 목록 (필수)
- `topic`: 산출물 묶음 식별자(슬러그) (선택, 기본: 호스트명)
- `note`: 수집 의도 한 줄 (선택)

## 절차

1. 각 URL이 워크스페이스 정책상 허용 도메인인지 확인 (모르면 사용자에게 확인).
2. `gov-archive/archive_fetch`로 본문을 받아 `archive/raw/...`에 저장.
3. 저장 경로와 sidecar `.meta.json`의 `collected_at`을 함께 기록.
4. 동일 URL의 기존 해시와 비교해 변경 여부 보고.
5. `gov-archive/archive_cite`로 각 항목의 인용 메타 생성.
6. `archive/processed/<topic>/source.md`에 인용 메타와 다음 작업(예: `summarize-minutes`,
   `ordinance-brief`) 후보를 적어 둔다.

## 출력

- 저장 경로 목록
- `collected_at` 목록
- 변경/신규/동일 표시
- 다음 단계로 추천하는 스킬·에이전트
