# Changelog

이 프로젝트의 모든 주목할 만한 변경 사항을 기록합니다.
형식은 [Keep a Changelog](https://keepachangelog.com/ko/1.1.0/)를 따릅니다.

## [Unreleased]

### Added
- 1차 저장소 골격 (Phase 1)
  - 한국어 문서 8종 (`README`, `AGENTS.md`, `문서/*`)
  - VS Code 설정·태스크·MCP·toolset
  - Copilot CLI hooks (logging-first, Bash + PowerShell)
  - Custom agents 2종 (assembly-minutes, ordinance-reviewer)
  - Skills 6종 (gokr-fetch, hwp-to-text, pdf-extract, pii-mask, vscode-task-author, retrospective-writer)
  - 환경 설정·자격증명 정리 스크립트 (Win/macOS)
  - `gov-archive` MCP 서버 (Python/uv/FastMCP, stdio) — `archive_fetch`, `archive_search`, `archive_cite`
  - `보관함/legalize-kr`, `precedent-kr`, `admrule-kr`, `ordinance-kr` shallow clone (git)
  - GitHub Actions: YAML frontmatter lint, gitleaks

### Changed
- `gov-archive` MCP 서버에 문서 변환 기능을 내장하고 `archive_convert` 도구를 추가
- `archive_fetch`가 HTML 페이지 내 HWP/HWPX/DOCX/PDF 링크를 자동 수집하도록 확장

### Removed
- 스킬 `hwp-to-text`, `pdf-extract` 제거 (기능을 `gov-archive`로 통합)
