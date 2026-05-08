# my-politics-agents

대한민국 지방정치에 참여하려는 시민을 위한 다중 에이전트 도구 모음.
`*.go.kr` 자료를 수집·정제해 인용 가능한 문서로 만들고, Google NotebookLM에
공개 노트북으로 동기화합니다. GitHub Copilot CLI · VS Code Copilot Chat · Codex CLI에서
같은 워크스페이스 자산(에이전트·스킬·프롬프트·MCP)을 공유합니다.

> 1차 시범 데이터 소스는 [law.go.kr] / [legalize-kr]. 다른 사이트는 어댑터(skill + MCP)로 점진 확장합니다.

[law.go.kr]: https://www.law.go.kr/
[legalize-kr]: https://github.com/legalize-kr/legalize-kr

## What you can do

- 의안·회의록·예산서 PDF/HWP를 Markdown으로 변환하고 출처(URL·해시·시각)를 함께 기록.
- 정제 문서를 NotebookLM 노트북으로 업로드/갱신해 시민이 음성·Q&A로 열람.
- 같은 작업을 반복할수록 회고·스킬·에이전트가 누적되어 다음 사용이 빨라짐.

### File Organization

```
my-politics-agents/
├── agents/                          # Custom agent 정의 (`*.agent.md`)
├── .agents/skills/                  # 재사용 스킬 (`SKILL.md`)
├── .github/
│   ├── prompts/                     # 재사용 프롬프트
│   └── hooks/                       # Copilot CLI hooks
├── .vscode/                         # VS Code 설정·태스크·MCP·toolset
├── scripts/                         # 환경 설정·인증 정리
├── mcp-servers/                     # 워크스페이스 로컬 MCP 서버
├── adapters/                        # go.kr 사이트별 수집 어댑터
├── archive/
│   ├── raw/                         # 원본
│   └── processed/                   # 정제본
├── notebooks/                       # NotebookLM 업로드 매니페스트
├── retrospectives/                  # 세션 회고 누적
├── data/                            # 법령·판례·행정규칙·자치법규 shallow clone
└── docs/                            # 한국어 보조 문서
```

## How To

### Setup

대상: Git/터미널 처음 사용 또는 가볍게 사용 가능한 분. 30분 안에 첫 수집·정제·요약을 마치는 것이 목표입니다.

이 저장소는 여러분의 컴퓨터에서만 동작합니다. 모든 자격증명·캐시·결과물은 로컬에 남고 외부로 자동 전송되지 않습니다. 전역 설치가 필요하면 항상 동의를 먼저 묻습니다.

**1. 사전 준비**

| 항목 | Windows 11 | Windows 10 | macOS |
| --- | --- | --- | --- |
| Git | `winget install Git.Git` | [Git for Windows] | `brew install git` |
| VS Code | `winget install Microsoft.VisualStudioCode` | [VS Code] | `brew install --cask visual-studio-code` |
| PowerShell 7 | `winget install Microsoft.PowerShell` | 동일 | (불필요) |

[Git for Windows]: https://git-scm.com/download/win
[VS Code]: https://code.visualstudio.com/

> Node.js · Python · GitHub CLI · Copilot CLI 등은 다음 단계 스크립트가 안내합니다.

**2. 저장소 받기**

```pwsh
git clone https://github.com/luncliff/my-politics-agents.git
cd my-politics-agents
```

`data/legalize-kr` 등 연관 저장소는 설정 단계에서 shallow clone으로 준비됩니다.

**3. 환경 설정 (한 번만)** — 스크립트는 무엇을 설치할지 보여주고 동의를 받습니다.

```pwsh
# Windows (PowerShell 7)
pwsh -ExecutionPolicy Bypass -File scripts/setup.ps1
```

```zsh
# macOS (zsh)
zsh scripts/setup.sh
```

미리 보려면 `-DryRun` / `--dry-run`. 설치 후보: Node 24 LTS, `gh`, `@github/copilot`, [`uv`](https://docs.astral.sh/uv/), (선택) Java 11+, Rancher Desktop.

**4. GitHub CLI 로그인**

```pwsh
gh auth login
```

자격증명 정리는 [docs/security.md](docs/security.md)의 `auth-purge` 참조.

### With Visual Studio Code

권장 진입점입니다.

1. `code .` 으로 워크스페이스 열기.
2. 권장 확장 설치 알림이 뜨면 모두 설치.
3. `Ctrl+Shift+P` → `Tasks: Run Task` 에서 작업 선택.

| Task | 동작 |
| --- | --- |
| `civic: setup` | 환경 설정(또는 변경 후 재실행) |
| `civic: copilot session continue` | Copilot CLI 세션 시작(정책 배너 포함) |
| `civic: notebooklm-sync` | 정제본을 NotebookLM 노트북으로 동기화 |
| `civic: mcp doctor` | 워크스페이스 MCP 서버 상태 점검 |
| `civic: lint prompts/skills` | 프롬프트·스킬 형식 검사 |
| `civic: auth-purge` | 자격증명·로컬 캐시 정리 |
| `civic: fetch nemotron personas (download)` | Nemotron-Personas-Korea parquet 다운로드 |
| `civic: sample nemotron panel (national 600)` | 전국 시민 페르소나 패널 600명 추출 |
| `civic: sample nemotron panel (local from location.txt)` | 지역 시민 페르소나 패널 300명 추출 |

채팅창 자연어 예시:

- "최근 한 달치 OO시의회 본회의 회의록을 받아서 표결 결과 표로 정리해줘"
- "이 조례안의 쟁점을 사실/해석으로 나눠 한 페이지 브리핑으로 만들어줘"
- "/persona-review archive/processed/<문서경로> both 10"

위험한 명령(파일 삭제·외부 호출)은 확인 다이얼로그가 뜹니다. 같은 도메인을 한 번 허용하면 다음부터 자동 승인됩니다.

### With GitHub Copilot CLI

```pwsh
copilot
# 또는 이어서
copilot --continue
```

세션 시작 시 정책 배너가 출력되고, 위험 명령은 차단/경고됩니다. `chat.tools.urls.autoApprove` · `chat.tools.terminal.autoApprove` 화이트리스트는 VS Code와 공유됩니다.

자주 쓰는 호출:

```pwsh
copilot --model=auto --allow-all-urls --add-dir . --prompt "/search-night-care with current location.txt"
```

### With Codex CLI

Codex CLI는 같은 워크스페이스의 `agents/`·`.agents/skills/`·`.github/prompts/`·`.vscode/mcp.json`을 그대로 사용합니다.

1. 저장소 루트에서 Codex 세션을 시작합니다(워크스페이스 트러스트 필수).
2. 첫 응답에서 [AGENTS.md](AGENTS.md)의 규칙(특히 citation·PII·destructive command 가드)을 따르는지 확인합니다.
3. MCP 서버는 `.vscode/mcp.json` 정의를 그대로 사용하므로 Codex 측 자격증명만 별도로 점검합니다.
4. 세션 종료 직전 `retrospective-writer` 스킬을 호출해 회고를 남깁니다.

## Result locations

| 폴더 | 내용 |
| --- | --- |
| `archive/raw/` | 원본 그대로 (수정·삭제 금지) |
| `archive/processed/` | 사람이 읽기 좋은 정제 Markdown |
| `notebooks/<slug>/` | NotebookLM 업로드 묶음 (스키마: [notebooks/README.md](notebooks/README.md)) |
| `retrospectives/` | 매 세션 회고 — 다음 사용 시 참고 |

## Troubleshooting

- **확장 추천이 안 뜸** → `Ctrl+Shift+P` → `Extensions: Show Recommended Extensions`.
- **Task가 안 보임** → 좌상단 폴더가 `my-politics-agents`인지 확인.
- **MCP 서버가 빨간 점** → `civic: mcp doctor` 실행 후 출력 확인.
- **인증 초기화** → `civic: auth-purge` 실행.

## References

- **legalize-kr** — 한국 법령·판례·행정규칙·자치법규를 정형 JSON/Markdown으로 미러링한 오픈 데이터 저장소. `legalize-kr` MCP가 본 저장소의 1차 법령 백엔드입니다. <https://github.com/legalize-kr/legalize-kr>
- **국가법령정보센터 (law.go.kr)** — 대한민국 공식 법령·자치법규·판례 포털. legalize-kr의 1차 출처이자 최종 검증처. <https://www.law.go.kr/>
- **ELIS** — 자치법규정보시스템. 지자체 조례·규칙 1차 검색 진입점. <https://www.elis.go.kr/>
- **Google NotebookLM** — 정제 문서를 음성 개요·Q&A로 공개하는 노트북 서비스. 동기화 흐름은 [notebooks/README.md](notebooks/README.md). <https://notebooklm.google.com/>
- **NotebookLM MCP (PleasePrompto)** — NotebookLM 업로드/갱신을 자동화하는 외부 MCP. 본 저장소는 placeholder 어댑터를 통해 위임 호출. <https://github.com/PleasePrompto/notebooklm-mcp>
- **Nemotron-Personas-Korea** — NVIDIA가 공개한 한국 합성 시민 페르소나 데이터셋(CC BY 4.0). 시민 관점 검토 패널의 기반. <https://huggingface.co/datasets/nvidia/Nemotron-Personas-Korea>
- **Model Context Protocol** — 본 저장소의 모든 MCP 서버가 따르는 프로토콜 사양. <https://modelcontextprotocol.io/>
- **GitHub Copilot CLI** — 워크스페이스에서 동작하는 Copilot 터미널 에이전트. <https://github.com/github/copilot-cli>

## Security · Governance

- 모든 설정은 워크스페이스 안에만 저장. 전역 변경은 항상 묻고 진행. 자세한 내용 [AGENTS.md](AGENTS.md).
- 자격증명은 `scripts/auth-purge.{ps1,sh}`로 일괄 정리.
- Copilot CLI hooks가 정책 배너를 띄우고 위험 명령을 차단/경고.
- 모든 산출물은 출처를 footer에 명시. PII는 `pii-mask` 스킬 통과 의무.

## License

코드와 문서는 **CC0 1.0 Universal**(공공도메인 헌정). [LICENSE](LICENSE) 참조.
수집된 정부 자료는 별도 라이선스(공공누리 등)를 따르며, 산출물에 출처를 명시합니다.
