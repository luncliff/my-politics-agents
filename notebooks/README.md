# notebooks/

NotebookLM 업로드 묶음을 슬러그별로 둡니다.

```
notebooks/
  <slug>/
    manifest.yml      # 아래 스키마
    cover.md          # (선택) 노트북 표지/소개
```

예시: [`_example/manifest.yml`](_example/manifest.yml).

## 동기화 흐름

```
archive/processed/*.md  ──►  notebooks/<slug>/manifest.yml
                          │
                          ▼
              notebooklm-publisher.agent
                          │
                  notebooklm MCP (업로드/갱신)
                          │
                          ▼
                  공개 NotebookLM 노트북
                  (Audio Overview / Q&A)
```

1. `archive/processed/` 아래에서 노트북에 올릴 문서를 선정한다.
2. `notebooks/<slug>/manifest.yml`로 묶음을 정의한다.
3. `civic: notebooklm-sync` Task 또는 `notebooklm-publisher` 에이전트로 동기화한다.
4. 변경분만 업로드되며, 결과는 회고에 기록된다.

## 운영 규칙

- 노트북 1개 = 주제 1개. 폭이 넓어지면 분리한다.
- `update_policy: replace`가 기본. `append`는 시리즈 글에만 사용한다.
- 비공개로 시작 → 사실 검증 후 공개로 전환을 권장한다.

## manifest.yml 스키마

### 필수 필드

| 필드 | 타입 | 설명 |
| --- | --- | --- |
| `title` | string | 노트북 제목 |
| `sources` | array | 업로드할 소스 목록 (1개 이상) |
| `sources[].path` | string (workspace-relative) | 업로드할 파일 경로 (`archive/processed/...` 권장) |

### 선택 필드

| 필드 | 타입 | 기본값 | 설명 |
| --- | --- | --- | --- |
| `notebook_id` | string | (없음) | 최초 업로드 후 publisher가 채워줍니다 |
| `update_policy` | enum | `replace` | `replace` \| `append` |
| `visibility` | enum | `private` | `public` \| `unlisted` \| `private` |
| `language` | string | `ko` | BCP-47 (`ko`, `en` 등) |
| `tags` | string[] | `[]` | 분류용 |
| `sources[].citation` | string (URL) | (없음) | 원본 출처 — 정제본 frontmatter `source_url`과 일치해야 함 |
| `sources[].title` | string | 파일 제목에서 유추 | 노트북에 보일 제목 |
| `sources[].pinned` | boolean | `false` | 노트북 상단 고정 여부 |

### 예시

```yaml
notebook_id: ""
title: "OO시 2026 본예산 분석"
update_policy: replace
visibility: public
language: ko
tags: [예산, OO시, 2026]

sources:
  - path: archive/processed/budget/2026-overview.md
    citation: https://www.oo.go.kr/budget/2026
    title: "2026 본예산 개요"
    pinned: true
  - path: archive/processed/budget/2026-debates.md
    citation: https://www.oo.go.kr/council/minutes/2026-budget
    title: "예산 심의 회의록 요약"
```

### 검증 규칙

- `sources[].path`는 워크스페이스 안이어야 하고, 실제로 존재해야 한다.
- `sources[].citation`은 HTTPS URL이어야 한다.
- 정제본 Markdown frontmatter `source_url`과 manifest `citation`이 일치해야 한다(불일치 시 동기화 차단).
- `update_policy: replace`인 경우 노트북의 기존 소스는 모두 새 목록으로 대체된다.

## MCP 서버

저장소의 `notebooklm-bridge` 서버는 placeholder입니다.
실 업로드는 [PleasePrompto/notebooklm-mcp]를 직접 등록하거나 후속 단계에서 자체 래퍼를 추가합니다.

[PleasePrompto/notebooklm-mcp]: https://github.com/PleasePrompto/notebooklm-mcp
