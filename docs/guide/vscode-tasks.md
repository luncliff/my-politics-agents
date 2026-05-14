# VS Code에서 사용하기

권장 진입점입니다.

## 시작

1. `code .` 으로 워크스페이스 열기.
2. 권장 확장 설치 알림이 뜨면 모두 설치.
3. `Ctrl+Shift+P` → `Tasks: Run Task` 에서 작업 선택.

## 사용 가능한 Task

| Task | 동작 |
| --- | --- |
| `civic: setup` | 환경 설정(또는 변경 후 재실행) |
| `civic: copilot session continue` | Copilot CLI 세션 시작(정책 배너 포함) |
| `civic: notebooklm login` | NotebookLM 브라우저 로그인/세션 갱신 |
| `civic: notebooklm doctor` | NotebookLM CLI/MCP 상태 점검 |
| `civic: notebooklm notebook list` | 연결된 NotebookLM 노트북 목록 조회 |
| `civic: mcp doctor` | 워크스페이스 MCP 서버 상태 점검 |
| `civic: lint prompts/skills` | 프롬프트·스킬 형식 검사 |
| `civic: auth-purge` | 자격증명·로컬 캐시 정리 |
| `civic: fetch nemotron personas (download)` | Nemotron-Personas-Korea parquet 다운로드 |
| `civic: sample nemotron panel (national 600)` | 전국 시민 페르소나 패널 600명 추출 |
| `civic: sample nemotron panel (local from location.txt)` | 지역 시민 페르소나 패널 300명 추출 |

## 채팅창 자연어 예시

- "최근 한 달치 OO시의회 본회의 회의록을 받아서 표결 결과 표로 정리해줘"
- "이 조례안의 쟁점을 사실/해석으로 나눠 한 페이지 브리핑으로 만들어줘"
- "/persona-review archive/processed/<문서경로> both 10"

위험한 명령(파일 삭제·외부 호출)은 확인 다이얼로그가 뜹니다. 같은 도메인을 한 번 허용하면 다음부터 자동 승인됩니다.
