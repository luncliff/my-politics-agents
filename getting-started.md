---
description: 비개발자를 위한 5단계 시작 가이드
---

# 시작하기

> 대상: Git/터미널 처음 사용 또는 가볍게 사용 가능한 분.
> 목표: 30분 안에 첫 수집·정제·요약을 마치는 것.

## 0. 미리 알아둘 것

- 이 저장소는 **여러분의 컴퓨터에서만** 동작합니다. 모든 자격증명·캐시·결과물은 여러분의 컴퓨터에 남고, 외부에 자동 전송되지 않습니다.
- "전역 설치"가 필요한 경우 **항상 동의를 먼저 묻습니다**. 동의 없이 시스템 설정을 바꾸지 않습니다.

---

## 1. 사전 준비

| 항목 | Windows 11 | Windows 10 | macOS |
| --- | --- | --- | --- |
| Git | `winget install Git.Git` | [Git for Windows] 설치 | `brew install git` |
| VS Code | `winget install Microsoft.VisualStudioCode` | [VS Code] 설치 | `brew install --cask visual-studio-code` |
| PowerShell 7 | `winget install Microsoft.PowerShell` | 동일 | (불필요) |
| zsh | (불필요) | (불필요) | macOS 기본 포함 |

[Git for Windows]: https://git-scm.com/download/win
[VS Code]: https://code.visualstudio.com/

> Node.js·Python·GitHub CLI·Copilot CLI 등 나머지는 다음 단계의 설정 스크립트가 알아서 안내합니다.

---

## 2. 저장소 받기

```pwsh
git clone --recurse-submodules https://github.com/luncliff/my-politics-agents.git
cd my-politics-agents
```

`--recurse-submodules`는 `data/legalize-kr` 같은 서브모듈을 함께 받기 위해서입니다.
이미 받았다면 다음 명령으로 보완할 수 있습니다.

```pwsh
git submodule update --init --recursive
```

---

## 3. 환경 설정

운영체제에 맞춰 한 줄만 실행하세요. 스크립트는 **무엇을 설치할지 보여주고 동의를 받습니다**.

### Windows (PowerShell 7)

```pwsh
pwsh -ExecutionPolicy Bypass -File scripts/setup.ps1
```

### macOS (zsh)

```zsh
zsh scripts/setup.sh
```

미리 무엇을 할지만 보고 싶다면:

```pwsh
pwsh -File scripts/setup.ps1 -DryRun
```

```zsh
zsh scripts/setup.sh --dry-run
```

설치되는 것(필요한 경우만):

- Node.js 24 LTS, GitHub CLI(`gh`), GitHub Copilot CLI(`@github/copilot`)
- [`uv`](https://docs.astral.sh/uv/) (Python 패키지·환경 관리)
- (선택) Java 11+ — PDF 추출(opendataloader-pdf) 사용 시
- (선택) Rancher Desktop — 컨테이너 기반 MCP 사용 시

---

## 4. GitHub 로그인

```pwsh
gh auth login
```

브라우저가 열리고 GitHub 인증이 끝나면 됩니다.
나중에 자격증명을 정리하려면 [docs/security.md](security.md)의 `auth-purge`를 참고하세요.

---

## 5. 에이전트 시작

### A. VS Code에서 (권장)

1. `code .`로 워크스페이스를 엽니다.
2. 권장 확장 설치 알림이 뜨면 **모두 설치**.
3. `Ctrl+Shift+P` → `Tasks: Run Task` → `civic: copilot session` 실행.
4. 정책 배너가 보이면 준비 완료입니다. 채팅 또는 터미널에서 다음을 시도해 보세요.
   - "민법 시행령 최근 개정 핵심을 한 페이지로 요약해줘"
   - "이번 달 OO시의회 회의록을 받아서 쟁점을 정리해줘"

### B. 터미널에서 직접

```pwsh
copilot
```

세션이 시작되면 정책 배너가 출력되고, 위험 명령은 차단/경고됩니다.

---

## 자주 묻는 질문

- **인터넷 접속이 차단된 환경입니다.** — 외부 자료가 필요한 도구는 동작하지 않습니다. 로컬 archive만 사용하는 작업(요약·재정리)은 가능합니다.
- **결과물이 어디에 저장되나요?** — 원본은 `archive/raw/`, 정제본은 `archive/processed/`, NotebookLM에 보낼 묶음은 `notebooks/<slug>/`에 저장됩니다.
- **회고가 자동으로 만들어진다는데?** — 세션 종료 직전에 `retrospective-writer` 스킬이 `retrospectives/`에 한 파일을 만듭니다. 다음 사용에서 이전 회고를 참고합니다.

---

## 다음 읽기

- [for-non-developers.md](for-non-developers.md) — VS Code 메뉴 위주의 사용법
- [security.md](security.md) — 자격증명·전역 변경 정책
- [governance.md](governance.md) — 출처·라이선스·PII 규칙
