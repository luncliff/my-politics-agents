---
description: 시스템 개요와 데이터 흐름
---

# 아키텍처

```
┌─────────────────────────────────────────────────────────┐
│  Copilot CLI  (orchestrator + planner + retrospective)  │
│  VS Code Copilot Chat (동일 자산 공유)                   │
└──────────┬───────────────────────────┬──────────────────┘
           │                           │
   ┌───────▼────────┐         ┌────────▼────────┐
   │ agents/*.md    │         │ skills/*/SKILL  │
   │ (페르소나)      │◄────────┤ (재사용 작업)   │
   └───────┬────────┘         └────────┬────────┘
           │                           │
   ┌───────▼───────────────────────────▼────────┐
   │  MCP Servers (mcp-servers/)                │
   │  • gov-archive (Python · stdio · 동작 중)  │
   │  • hwp-toolkit / pdf-loader / nblm-bridge  │
   │    (placeholder, 후속 단계)                │
   └───────┬────────────────────────────────────┘
           │
   ┌───────▼────────┐   ┌───────────────┐   ┌──────────────┐
   │ archive/raw/   │──►│ archive/      │──►│ NotebookLM   │
   │ (원본 보존)     │   │ processed/    │   │ (공개 노트북)│
   └────────────────┘   └───────────────┘   └──────────────┘
```

## 컴포넌트

### Copilot CLI · VS Code Chat

- 두 환경이 **같은 워크스페이스 파일**(agents/skills/prompts)을 공유합니다.
- VS Code의 `chat.tools.urls.autoApprove`, `chat.tools.terminal.autoApprove`,
  `Tool Sets`, `Plan agent` 같은 IDE 특화 기능은 IDE에서만 활용하되,
  정책 가드(`hooks/`)는 두 환경 모두에 적용됩니다.

### MCP Servers

- 워크스페이스 내부에 두어 외부 의존을 줄입니다.
- 1차 대상은 **`gov-archive`** — 외부 URL을 받아 `archive/raw/`에 원본+해시로 저장하고,
  로컬 검색·인용 메타 생성 도구를 제공합니다(모두 `readOnlyHint`).
- 후속 서버(HWP/PDF/NotebookLM)는 [docs/mcp-servers.md](mcp-servers.md) 참조.

### 데이터 흐름

1. **Collect** — 어댑터(`adapters/*`) 또는 MCP 도구가 외부 자원을 가져옴.
2. **Archive** — `archive/raw/<host>/<YYYY-MM-DD>/` 아래에 불변 보존.
3. **Process** — `pii-mask`, `hwp-to-text`, `pdf-extract` 등 스킬을 거쳐 Markdown 정제.
4. **Publish** — `notebooks/<slug>/manifest.yml`을 만들고 NotebookLM에 동기화.
5. **Retrospect** — 세션 종료 시 `retrospective-writer`가 회고를 누적.

## 디렉터리 책임

| 경로 | 한 줄 책임 |
| --- | --- |
| `agents/` | 도메인 페르소나(예: 회의록 요약가) |
| `skills/` | 한 가지 일을 잘하는 재사용 작업 단위 |
| `.github/prompts/` | 자주 쓰는 프롬프트 템플릿 |
| `.github/hooks/` | Copilot CLI 정책·로깅 |
| `.vscode/` | IDE 설정·Task·MCP·Toolset |
| `scripts/` | 환경 설정·자격증명 정리 |
| `mcp-servers/` | 워크스페이스 로컬 MCP |
| `adapters/` | 사이트별 수집·정규화 코드(JS/Py) |
| `archive/` | 원본/정제본 |
| `notebooks/` | NotebookLM 업로드 묶음 |
| `retrospectives/` | 세션 회고 누적 |
| `data/legalize-kr/` | 법령 데이터 submodule |

## 의존성 정책

- **Node 24 LTS**, **Python 3.12+** (uv).
- 외부 도구 중 **opendataloader-pdf**(JVM 11+)와 **rhwp**(WASM)는 사용 시점에만 설치 안내.
- 컨테이너 필요 도구는 Rancher Desktop을 권장(필수 아님).
