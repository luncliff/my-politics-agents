# Changelog

이 프로젝트의 모든 주목할 만한 변경 사항을 기록합니다.
형식은 [Keep a Changelog](https://keepachangelog.com/ko/1.1.0/)를 따릅니다.

## [Unreleased]

### Added
- 1차 저장소 골격 (Phase 1)
  - 한국어 문서 8종 (`README`, `AGENTS.md`, `docs/*`)
  - VS Code 설정·태스크·MCP·toolset
  - Copilot CLI hooks (logging-first, Bash + PowerShell)
  - Custom agents 3종 (assembly-minutes, ordinance-reviewer, notebooklm-publisher)
  - Skills 7종 (gokr-fetch, hwp-to-text, pdf-extract, pii-mask, notebooklm-sync, vscode-task-author, retrospective-writer)
  - 환경 설정·자격증명 정리 스크립트 (Win/macOS)
  - `gov-archive` MCP 서버 (Python/uv/FastMCP, stdio) — `archive_fetch`, `archive_search`, `archive_cite`
  - `data/legalize-kr` git submodule
  - GitHub Actions: YAML frontmatter lint, gitleaks
