# 시작하기

대상: Git/터미널 처음 사용 또는 가볍게 사용 가능한 분. 30분 안에 첫 수집·정제·요약을 마치는 것이 목표입니다.

이 저장소는 여러분의 컴퓨터에서만 동작합니다. 모든 자격증명·캐시·결과물은 로컬에 남고 외부로 자동 전송되지 않습니다. 전역 설치가 필요하면 항상 동의를 먼저 묻습니다.

## 1. 사전 준비

| 항목 | Windows 11 | Windows 10 | macOS |
| --- | --- | --- | --- |
| Git | `winget install Git.Git` | [Git for Windows] | `brew install git` |
| VS Code | `winget install Microsoft.VisualStudioCode` | [VS Code] | `brew install --cask visual-studio-code` |
| PowerShell 7 | `winget install Microsoft.PowerShell` | 동일 | (불필요) |

[Git for Windows]: https://git-scm.com/download/win
[VS Code]: https://code.visualstudio.com/

> Node.js · Python · GitHub CLI · Copilot CLI 등은 다음 단계 스크립트가 안내합니다.

## 2. 저장소 받기

```pwsh
git clone https://github.com/luncliff/politics-agents.git
cd politics-agents
```

`보관함/legalize-kr` 등 연관 저장소는 설정 단계에서 shallow clone으로 준비됩니다.

## 3. 환경 설정 (한 번만)

스크립트는 무엇을 설치할지 보여주고 동의를 받습니다.

```pwsh
# Windows (PowerShell 7)
pwsh -ExecutionPolicy Bypass -File scripts/setup.ps1
```

```zsh
# macOS (zsh)
zsh scripts/setup.sh
```

미리 보려면 `-DryRun` / `--dry-run`. 설치 후보: Node 24 LTS, `gh`, `@github/copilot`, [`uv`](https://docs.astral.sh/uv/), (선택) Java 11+, Rancher Desktop.

## 4. GitHub CLI 로그인

```pwsh
gh auth login
```

자격증명 정리는 [문서/security.md](../security.md)의 `auth-purge` 참조.

## 5. 다음 단계

- VS Code에서 사용: [vscode-tasks.md](vscode-tasks.md)
- Copilot CLI / Codex CLI: [copilot-cli.md](copilot-cli.md)

## Troubleshooting

- **확장 추천이 안 뜸** → `Ctrl+Shift+P` → `Extensions: Show Recommended Extensions`.
- **Task가 안 보임** → 좌상단 폴더가 `politics-agents`인지 확인.
- **MCP 서버가 빨간 점** → `civic: mcp doctor` 실행 후 출력 확인.
- **인증 초기화** → `civic: auth-purge` 실행.
