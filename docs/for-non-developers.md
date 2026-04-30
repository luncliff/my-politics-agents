---
description: VS Code 메뉴와 Task 위주의 사용법 (코드 작성 없이)
# 비개발자를 위한 사용 가이드

이 문서는 **터미널 명령을 거의 입력하지 않고**, VS Code의 메뉴·버튼만으로
이 도구를 사용하는 방법을 설명합니다.

## 화면 구성 한눈에

| 위치 | 무엇 |
| --- | --- |
| 왼쪽 사이드바 위쪽 | 폴더 트리(탐색기) |
| 왼쪽 사이드바 채팅 아이콘 | Copilot Chat — 자연어로 지시 |
| 아래쪽 패널 | **터미널** / **문제** / **출력** |
| `Ctrl+Shift+P` | 명령 팔레트 — 모든 기능 검색 |

## Task로 자주 하는 일 한 번에 실행

1. `Ctrl+Shift+P` → `Tasks: Run Task` 입력 → Enter.
2. 목록 중 하나를 고릅니다.

| Task | 무엇을 하나요 |
| --- | --- |
| `civic: setup` | 처음 환경 설정 (또는 변경 후 재실행) |
| `civic: copilot session` | Copilot CLI 세션 시작 (정책 배너 포함) |
| `civic: collect <site>` | 사이트를 골라 자료를 수집 |
| `civic: process` | 원본을 읽기 좋은 Markdown으로 정제 |
| `civic: notebooklm-sync` | 정제본을 NotebookLM 노트북으로 동기화 |
| `civic: mcp doctor` | 워크스페이스 MCP 서버 상태 점검 |
| `civic: lint prompts/skills` | 프롬프트·스킬 형식 검사 |
| `civic: auth-purge` | 자격증명·로컬 캐시 정리 |

> 처음 실행 시 사이트·기간 등 입력값을 묻습니다. 화면 위쪽 입력창에서 고르면 됩니다.

## Copilot Chat에서 자연어로 지시

채팅창에 다음처럼 입력해 보세요.

- "최근 한 달치 OO시의회 본회의 회의록을 받아서 표결 결과 표로 정리해줘"
- "이 조례안의 쟁점을 사실/해석으로 나눠 한 페이지 브리핑으로 만들어줘"
- "이 주제로 NotebookLM 노트북에 올릴 매니페스트 초안을 만들어줘"

작업 도중 위험한 명령(파일 삭제, 외부 사이트 호출 등)이 필요하면 **확인 다이얼로그**가 뜹니다.
내용을 읽고 *Allow* 또는 *Deny*를 누르세요. 같은 도메인에 대해 한 번 동의하면 다음부터 자동 승인됩니다.

## 결과물 확인

| 폴더 | 내용 |
| --- | --- |
| `archive/raw/` | 원본 그대로 (수정·삭제 금지) |
| `archive/processed/` | 사람이 읽기 좋은 정제 Markdown |
| `notebooks/<slug>/` | NotebookLM 업로드 묶음(매니페스트 + 본문) |
| `retrospectives/` | 매 세션의 회고 — 다음 사용 시 참고됨 |

## 잘 안 될 때

- **확장 추천이 안 떠요.** — `Ctrl+Shift+P` → `Extensions: Show Recommended Extensions`.
- **Task가 보이지 않아요.** — 워크스페이스 폴더가 맞는지 확인. 좌상단 폴더 이름이 `my-politics-agents`이어야 합니다.
- **MCP 서버가 빨간 점입니다.** — `civic: mcp doctor` Task 실행 → 출력 창에서 메시지 확인.
- **자격증명을 처음부터 다시 하고 싶어요.** — `civic: auth-purge` Task 실행.

추가로 [security.md](security.md)와 [governance.md](governance.md)도 가볍게 훑어 두면 안전합니다.
