# my-politics-agents

대한민국 지방정치에 참여하려는 시민을 위한 다중 에이전트 도구 모음.

- 자료를 수집·정제해 인용 가능한 문서로 만들기(자산화)
- GitHub Copilot CLI · VS Code Copilot Chat · Codex CLI · Claude Code에서 같은 자산을 공유
- Google NotebookLM 연동으로 음성·Q&A 열람

## Quick Start

```pwsh
git clone https://github.com/luncliff/my-politics-agents.git
cd my-politics-agents
pwsh -ExecutionPolicy Bypass -File scripts/setup.ps1   # Windows
code .                                                  # VS Code 열기
```

상세 안내: [docs/guide/getting-started.md](docs/guide/getting-started.md)

## Result Locations

| 폴더 | 내용 |
| --- | --- |
| `archive/raw/` | 원본 그대로 (수정·삭제 금지) |
| `archive/processed/` | 사람이 읽기 좋은 정제 Markdown |
| `notebooks/<slug>/` | NotebookLM 업로드 묶음 |
| `retrospectives/` | 매 세션 회고 — 다음 사용 시 참고 |

## Documentation

| 대상 | 문서 |
| --- | --- |
| 시민 사용자 | [docs/guide/](docs/guide/) |
| Agent 규칙 | [AGENTS.md](AGENTS.md) |
| Maintainer | [docs/dev/](docs/dev/) |
| 참조 자료 | [docs/references/](docs/references/) |

## License

코드와 문서는 **CC0 1.0 Universal**(공공도메인 헌정). [LICENSE](LICENSE) 참조.
수집된 정부 자료는 별도 라이선스(공공누리 등)를 따르며, 산출물에 출처를 명시합니다.
