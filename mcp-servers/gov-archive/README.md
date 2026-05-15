# gov-archive MCP server

워크스페이스 로컬 MCP 서버. 외부 자료를 받아 `보관함/다운로드/`에 보존하고, 인용 메타와 로컬 검색 도구를 제공합니다.

## 도구

| 도구 | 입력 | 동작 | 어노테이션 |
| --- | --- | --- | --- |
| `archive_fetch` | `url`, `note?`, `auto_convert?` | URL 본문 저장 + HTML 페이지의 HWP/HWPX/DOCX/PDF 링크 자동 다운로드 시도 | `readOnlyHint: true` |
| `archive_search` | `query`, `scope?` (`raw`\|`processed`\|`all`) | 로컬 보관함 텍스트 grep | `readOnlyHint: true` |
| `archive_cite` | `path` | 인용 메타 Markdown | `readOnlyHint: true` |
| `archive_convert` | `path` | HWP/HWPX/DOCX/PDF를 Markdown으로 변환해 `보관함/결과/` 저장 | `readOnlyHint: true` |

### 저장 규칙

- 파일 저장 경로: `보관함/다운로드/<host>/<basename>`
- Struts `.do` URL이라도 HTML 응답이면 `.html` 확장자로 저장
- 파일명에는 수집일 접두어를 자동으로 붙이지 않음
- 시간순 추적 기준: 같은 파일의 `.meta.json` 안 `collected_at` (ISO-8601)
- URL basename에 이미 날짜/시각이 있으면 원문 파일명을 그대로 재사용

### 변환 규칙

- 지원 확장자: `.hwp`, `.hwpx`, `.docx`, `.pdf`
- `archive_fetch(..., auto_convert=false)`로 자동 변환 비활성화 가능
- PDF 변환은 `opendataloader-pdf` 설치 시 우선 사용, 미설치 시 `pypdf` fallback
- `opendataloader-pdf` 사용 시 Java 11+ 필요

### 도메인 지원 방향

- 1순위: `*.go.kr`, `*.or.kr`
- 2순위: `*.kr` 및 지방정부/지방의회 공식 웹사이트
- 그 외 도메인: 정책 범위에서 점진적 확장

## 실행

```pwsh
uv run --directory mcp-servers/gov-archive gov-archive
```

VS Code/Copilot CLI는 `.vscode/mcp.json`을 통해 자동으로 stdio 연결합니다.

## 안전

- 모든 쓰기는 워크스페이스 루트의 `보관함/다운로드/` 안으로 제한 (경로 트래버설 차단).
- robots.txt 준수, 1초당 동일 호스트 1요청.
- 로깅은 `stderr`로만 (stdout은 JSON-RPC 채널).
