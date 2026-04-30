# .github/copilot-instructions.md — VS Code Chat 특이사항

이 파일은 VS Code Copilot Chat가 자동으로 읽는 워크스페이스 지시서입니다.
**공통 규약은 [/AGENTS.md](../AGENTS.md)에 있습니다.** 여기서는 IDE 한정 사항만 정리합니다.

## 도구 사용

- 외부 URL 호출은 `chat.tools.urls.autoApprove`의 화이트리스트만. `*.go.kr/*`은
  요청은 자동, 응답은 사람 검토(prompt-injection 방지).
- 터미널은 `chat.tools.terminal.autoApprove`에 등록된 read-only 패턴만 무인 실행.
  (`git status`, `git diff`, `gh repo view --json` 등)
- 128개 도구 한도에 닿을 것 같으면 `.vscode/toolsets.jsonc`의 묶음을 채팅에서 토글.

## Plan-first 권장

- 5단계 이상의 변경이거나 외부 도메인이 새로 등장하면 **Plan agent**로 시작.
- 계획에 다음을 포함: 영향 디렉터리, 새로 호출할 도구·도메인, 회고에 기록할 항목.

## 채팅 동작 원칙

1. 한국어로 답하고, 코드/식별자는 영어 그대로.
2. 외부 자료를 인용할 때는 **본문에 출처 링크를 같이** 적는다.
3. PII가 포함될 가능성이 있는 텍스트는 `pii-mask` 스킬을 거친 결과만 채팅에 표시.
4. 산출물은 항상 `archive/processed/...` 또는 `notebooks/<slug>/...`에 저장하고, 채팅엔 **요약 + 경로** 표시.

## 파일별 우선순위

| 위치 | 우선도 |
| --- | --- |
| `.github/instructions/*.instructions.md` (있다면) | 높음 (`applyTo` 매칭) |
| `agents/*.agent.md` | 모드 활성 시 높음 |
| `.github/copilot-instructions.md` (이 파일) | 보통 |
| `/AGENTS.md` | 기본 |

## 새 도구·도메인이 필요할 때

1. 공급자/주소/필요한 권한을 사용자에게 알리고 승인을 받는다.
2. `.vscode/settings.json`에 자동 승인 항목을 PR로 추가한다.
3. 새 어댑터/스킬이 필요하면 `agents/`·`skills/`·`mcp-servers/` 중 적절한 곳에 정의한다.

## 회고 의무

세션 종료 직전 `retrospective-writer` 스킬을 호출해 `retrospectives/`에 기록한다.
시간이 부족하면 적어도 "다음에 자동화할 후보" 한 줄만이라도 남긴다.
