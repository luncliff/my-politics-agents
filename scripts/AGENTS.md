# scripts/AGENTS.md — Setup · fetch · hooks

Scope: `scripts/` 하위 자동화. 공통 규약은 [/AGENTS.md](../AGENTS.md).

## 구성

- `setup.{ps1,sh}` — 워크스페이스 초기화. 공통 헬퍼는 `common.{ps1,sh}`.
- `auth-purge.{ps1,sh}` — 자격증명 정리.
- `fetch_legalize_kr.{ps1,sh}` — `보관함/{legalize,precedent,admrule,ordinance}-kr/` shallow clone.
- `fetch_nemotron_personas.ps1` — 합성 페르소나 데이터 다운로드.
- `session-start.ps1`, `session-stop.ps1` — Claude Code 세션 훅.
- `pre-tool-bash.ps1` — Bash 명령 사전 점검 훅.
- `run-markdownlint.js` / `markdownlint.config.js` — 저장소 Markdown 린트(warning-only).
- `pre-commit` — commit 시 staged Markdown 자동 린트.
- `lint_frontmatter.py` — `.prompt.md` / `.instructions.md` / `SKILL.md` YAML frontmatter 린트.

## 추가 기준

- 새 스크립트는 PowerShell·Bash 양쪽을 함께 제공한다 (헬퍼는 `common.*`에 모은다).
- 기본은 `-DryRun`(또는 `--dry-run`) 모드. 파괴적 동작은 사용자 확인 플래그를 요구한다.
- 글로벌 설치(`npm i -g`, `git config --global` 등)는 절대 수행하지 않고, 사용자에게 안내만 한다.
