# 문서/AGENTS.md — Flat documentation set

Scope: `문서/` 하위. 공통 규약은 [/AGENTS.md](../AGENTS.md).

## 구성

- `문서/`는 **flat 구조**를 기본으로 유지한다. `dev/`, `guide/`, `references/` 같은 하위 폴더를 다시 만들지 않는다.
- 대표 문서:
  - [architecture.md](architecture.md) — 디렉터리 맵, agents/skills 목록, 스택.
  - [channels.md](channels.md) — 채널별 설정 (Copilot / Codex / Claude Code).
  - [security.md](security.md) — 보안 모델 · 자격증명.
  - [getting-started.md](getting-started.md), [copilot-cli.md](copilot-cli.md), [vscode-tasks.md](vscode-tasks.md) — 사용자 가이드.
  - [index.md](index.md), [경기도.md](경기도.md), [성남시.md](성남시.md), [성남시-공개데이터.md](성남시-공개데이터.md) — 참조 문서.

## 일반 지침

- 새 문서를 만들기 전에 **기존 `문서/*.md`를 먼저 보충·확장**하는 것을 기본 행동으로 삼는다.
- 새 문서는 기존 파일에 자연스럽게 흡수할 수 없고, 제목·주제·독자가 명확히 분리될 때만 만든다.
- 외부 사실은 출처 링크를 본문에 함께 표기한다.
- 참조 문서의 한글 파일명은 유지할 수 있다. 그 외 문서는 영어 파일명을 기본으로 한다.
- 같은 절차 안내가 두 번 이상 반복되면 새 문서보다 `.agents/skills/` 승격을 먼저 검토한다.
