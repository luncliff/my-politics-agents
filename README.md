# my-politics-agents

대한민국 지방정치에 참여하려는 시민을 위한
GitHub Copilot CLI + VS Code Chat 기반 다중 에이전트 도구 모음입니다.
`*.go.kr` 자료를 수집·정제해 인용 가능한 문서로 만들고, Google NotebookLM에
공개 노트북으로 동기화하는 흐름을 점진적으로 자동화합니다.

> 1차 시범 데이터 소스는 [law.go.kr] / [legalize-kr] 입니다.
> 다른 사이트는 어댑터(skill + MCP)를 추가하면서 점진적으로 확장합니다.

[law.go.kr]: https://www.law.go.kr/
[legalize-kr]: https://github.com/legalize-kr/legalize-kr

---

## 5단계 시작 (비개발자용)

1. **사전 준비** — Git, Visual Studio Code 설치.
2. **저장소 받기**
   ```
   git clone --recurse-submodules https://github.com/luncliff/my-politics-agents.git
   cd my-politics-agents
   ```
3. **환경 설정 (한 번만)** — 운영체제에 맞춰 한 줄 실행.
   - Windows (PowerShell 7): `pwsh -ExecutionPolicy Bypass -File scripts/setup.ps1`
   - macOS (zsh): `zsh scripts/setup.sh`
   - 스크립트는 무엇을 설치할지 **목록을 먼저 보여주고 동의를 받습니다**. 시스템 전역 변경은 기본 차단입니다.
4. **GitHub 로그인** — `gh auth login`
5. **에이전트 시작** — VS Code에서 `Tasks: Run Task` → `civic: copilot session`

자세한 사용법은 [docs/getting-started.md](docs/getting-started.md)와
[docs/for-non-developers.md](docs/for-non-developers.md)를 보세요.

---

## 무엇을 할 수 있나요?

- 의안·회의록·예산서 PDF/HWP를 Markdown으로 변환하고 출처(URL·해시·시각)를 함께 기록
- 정제된 문서를 NotebookLM 노트북으로 업로드/갱신해 시민이 음성·Q&A로 열람
- 같은 작업을 반복할 때마다 **회고와 스킬·에이전트가 자동으로 누적**되어 다음 사용이 더 빨라집니다

---

## 보안·거버넌스 핵심

- **모든 설정은 워크스페이스(이 폴더) 안에만** 저장합니다. 전역 설정 변경은 항상 묻고 진행합니다.
- 자격증명은 `scripts/auth-purge.{ps1,sh}`로 일괄 정리할 수 있습니다.
- Copilot CLI hooks가 세션마다 정책 배너를 보여주고, 위험 명령은 차단/경고합니다.
- 모든 산출물은 출처를 footer에 명시합니다. PII는 `pii-mask` 스킬 통과를 의무화합니다.

자세한 정책은 [docs/security.md](docs/security.md), [docs/governance.md](docs/governance.md)를 보세요.

---

## 디렉터리

| 경로 | 용도 |
| --- | --- |
| [`agents/`](agents/) | Custom agent 정의 (`*.agent.md`) |
| [`skills/`](skills/) | 재사용 가능한 작업 스킬 (`SKILL.md`) |
| [`.github/prompts/`](.github/prompts/) | 재사용 프롬프트 |
| [`.github/hooks/`](.github/hooks/) | Copilot CLI hooks (Bash + PowerShell) |
| [`.vscode/`](.vscode/) | VS Code 설정·태스크·MCP·toolset |
| [`scripts/`](scripts/) | 환경 설정·인증 정리 |
| [`mcp-servers/`](mcp-servers/) | 워크스페이스 로컬 MCP 서버 |
| [`adapters/`](adapters/) | go.kr 사이트별 수집 어댑터 (JS/Python) |
| [`archive/`](archive/) | 원본(`raw/`) · 정제본(`processed/`) 보관소 |
| [`notebooks/`](notebooks/) | NotebookLM 업로드 매니페스트 |
| [`retrospectives/`](retrospectives/) | 세션 회고 누적 (자동 생성) |
| [`data/legalize-kr/`](data/) | 법령 데이터 git submodule |
| [`docs/`](docs/) | 한국어 문서 |

---

## 라이선스

이 저장소의 모든 코드와 문서는 **CC0 1.0 Universal**(공공도메인 헌정)입니다.
[LICENSE](LICENSE) 참조.

수집된 정부 자료는 별도 라이선스(공공누리 등)를 따릅니다 — 산출물에 출처를 명시합니다.
