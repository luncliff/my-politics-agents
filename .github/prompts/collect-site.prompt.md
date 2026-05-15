---
description: 웹사이트 자료를 수집하고 보관함/다운로드에 보존
tools: [read, search, web/fetch, browser, ms-vscode.vscode-websearchforcopilot/websearch]
---

# 사이트 수집 (collect-site)

목표: 지정된 URL(들)에서 자료를 가져와 `보관함/다운로드/<host>/`에
원본+해시로 보존하고, 인용 메타를 `보관함/결과/<slug>/source.md`에 남긴다.

파일명에는 수집일 접두어를 붙이지 않으며, 시간순 정렬은 `.meta.json`의 `collected_at`으로 처리한다.

## 입력

- `urls`: 수집할 URL 목록 (필수)
- `topic`: 산출물 묶음 식별자(슬러그) (선택, 기본: 호스트명)
- `note`: 수집 의도 한 줄 (선택)

## 절차

1. 각 URL이 워크스페이스 정책상 허용 도메인인지 확인 (모르면 사용자에게 확인).
2. HTML 웹페이지 본문을 받아 `보관함/다운로드/...`에 저장.
3. 저장 경로와 sidecar `.meta.json`의 `collected_at`을 함께 기록.
4. 동일 URL의 기존 해시와 비교해 변경 여부 보고.
5. 각 항목의 인용 메타 생성.

## 출력

- 저장 경로 목록
- `collected_at` 목록
- 변경/신규/동일 표시
- 다음 단계로 추천하는 스킬·에이전트
