---
description: NotebookLM 노트북 묶음 생성·동기화
tools: ["filesystem"]
---

# 노트북 출판 (publish-notebook)

목표: `archive/processed/...`의 정제본을 골라 `notebooks/<slug>/manifest.yml`을 만들고,
`notebooklm-sync` 스킬로 NotebookLM에 업로드한다.

## 입력

- `slug`: 노트북 식별자 (필수)
- `title`: 노트북 제목 (필수)
- `sources`: 포함할 정제본 경로 목록 (필수)
- `visibility`: public | unlisted | private (선택, 기본: private)

## 절차

1. 각 source의 frontmatter `source_url`이 인용 메타와 일치하는지 검증.
2. `notebooks/<slug>/manifest.yml` 생성 (스펙: docs/reference/manifest-schema.md).
3. `notebooklm-sync` 스킬 호출.
4. 결과(notebook_id, 업로드 결과)를 manifest에 다시 기록.
5. 회고에 변경 요약 1줄 추가 후보를 남긴다.
