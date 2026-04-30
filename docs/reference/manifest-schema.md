---
description: notebooks/<slug>/manifest.yml 스키마
---

# manifest.yml 스키마

NotebookLM 노트북 1개에 대응하는 업로드 묶음의 정의입니다.

## 필수 필드

| 필드 | 타입 | 설명 |
| --- | --- | --- |
| `title` | string | 노트북 제목 |
| `sources` | array | 업로드할 소스 목록 (1개 이상) |
| `sources[].path` | string (workspace-relative) | 업로드할 파일 경로 (`archive/processed/...` 권장) |

## 선택 필드

| 필드 | 타입 | 기본값 | 설명 |
| --- | --- | --- | --- |
| `notebook_id` | string | (없음) | 최초 업로드 후 publisher가 채워줍니다 |
| `update_policy` | enum | `replace` | `replace` \| `append` |
| `visibility` | enum | `private` | `public` \| `unlisted` \| `private` |
| `language` | string | `ko` | BCP-47 (`ko`, `en` 등) |
| `tags` | string[] | `[]` | 분류용 |
| `sources[].citation` | string (URL) | (없음) | 원본 출처 — 정제본의 frontmatter `source_url`과 일치해야 함 |
| `sources[].title` | string | 파일 제목에서 유추 | 노트북에 보일 제목 |
| `sources[].pinned` | boolean | `false` | 노트북 상단 고정 여부 |

## 예시

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

## 검증 규칙

- `sources[].path`는 **워크스페이스 안**이어야 하고, 실제로 존재해야 합니다.
- `sources[].citation`은 HTTPS URL이어야 합니다.
- 정제본 Markdown의 frontmatter `source_url`과 manifest의 `citation`이 일치해야 합니다(불일치 시 동기화 차단).
- `update_policy: replace`인 경우 노트북의 기존 소스는 모두 새 목록으로 대체됩니다.
