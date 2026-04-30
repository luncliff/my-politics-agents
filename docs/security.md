---
description: 보안 모델, 워크스페이스-로컬 원칙, 자격증명 정리
---

# 보안

## 1. 위협 모델 요약

| 위협 | 우리의 대응 |
| --- | --- |
| 토큰·키 누출 | `.env`/`*.token`/`.copilot/credentials*` gitignore + gitleaks CI |
| 프롬프트 인젝션(외부 페이지) | URL **post-approval** 활성화(`approveResponse: false`) |
| 의도치 않은 전역 변경 | 스크립트·hooks가 글로벌 변경을 모두 동의로 게이트 |
| 파괴적 명령 무인 실행 | `Bypass/Autopilot/yolo` 비활성, hooks `preToolUse`에서 차단 |
| 외부 도메인 임의 호출 | (preview) `chat.agent.networkFilter` + 도메인 화이트리스트 |
| 산출물에 PII 포함 | `pii-mask` 스킬을 산출 전 단계 의무화 |

## 2. 워크스페이스-로컬 원칙

| 항목 | 위치 | 전역은? |
| --- | --- | --- |
| Copilot CLI 설정 | `.copilot/` (워크스페이스) | `~/.copilot/`은 묻고만 사용 |
| MCP 서버 정의 | `.vscode/mcp.json` | 글로벌 `mcp.json` 수정 금지 |
| 프롬프트·스킬·에이전트 | `.github/prompts/`, `skills/`, `agents/` | 사용자 prompts 폴더 사용은 옵션 |
| Node 패키지 | repo `node_modules/` | `npm i -g`는 setup만, 동의 필요 |
| Python 환경 | `.venv/` (uv) | `uv tool install --global`은 옵트인 |
| Git 설정 | `.git/config` | `git config --global`은 묻고만 |

`scripts/setup.*`은 위 정책을 강제합니다. `--dry-run`으로 사전 확인할 수 있습니다.

## 3. URL 자동 승인

`.vscode/settings.json`의 `chat.tools.urls.autoApprove`는 도메인별로
**요청 자동 승인**과 **응답 자동 승인**을 분리해 둡니다.

- `*.go.kr/*` 등 정부 도메인: **요청만 자동, 응답은 매번 사람이 확인** (사용자 생성 콘텐츠로 인한 prompt injection 방어)
- `docs.github.com`, `code.visualstudio.com` 등 신뢰 가능한 OSS 문서: 양쪽 자동
- 명시적 차단(`pastebin.com`, `*.ngrok.io` 등): `false`

전체 초기화는 `Chat: Reset Tool Confirmations` 명령. 개별 검토는 `Chat: Manage Tool Approval`.

## 4. 자격증명 정리 (auth-purge)

다음을 안내·삭제할 수 있습니다(각 단계 동의 필요):

- `gh auth logout --hostname github.com`
- `~/.copilot/credentials*` 및 워크스페이스 `.copilot/credentials*`
- `GH_TOKEN`, `GITHUB_TOKEN`, `OPENAI_API_KEY` 등 셸 프로파일 점검(출력만)
- Windows Credential Manager 항목 나열·삭제 옵션
- macOS `security` 키체인의 `github.com` 항목 나열·삭제 옵션
- NotebookLM MCP 토큰/세션 파일 위치 표시 옵션
- `Chat: Reset Tool Confirmations` 권장(IDE에서 한 번 더 실행)

실행:

```pwsh
pwsh -File scripts/auth-purge.ps1
```

```zsh
zsh scripts/auth-purge.sh
```

비대화형 실행은 의도적으로 막아 두었습니다.

## 5. Copilot CLI hooks

`.github/hooks/copilot-cli-policy.json`이 다음 훅을 등록합니다.

- `sessionStart` — 정책 배너 출력
- `userPromptSubmitted` — 메타데이터(타임스탬프·cwd)만 `.github/hooks/logs/audit.jsonl`에 기록 (gitignore)
- `preToolUse` — 위험 명령 차단/경고 + 데모 deny 1개 (`COPILOT_HOOKS_DENY_DEMO`)

기본 정책은 **logging-first**입니다. 운영 환경에서는 `pre-tool-policy.{sh,ps1}`의
주석을 따라 deny 패턴을 단계적으로 강화하세요.

## 6. 신고

보안 결함을 발견하면 issue 대신 메일로 알려주세요(README 상단 owner 참조).
