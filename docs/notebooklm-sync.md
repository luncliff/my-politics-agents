---
description: NotebookLM 동기화 흐름과 매니페스트 작성
---

# NotebookLM 동기화

## 흐름

```
processed/*.md  ──►  notebooks/<slug>/manifest.yml
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

1. `archive/processed/` 아래에서 노트북에 올릴 문서를 선정합니다.
2. `notebooks/<slug>/manifest.yml`로 묶음을 정의합니다.
3. `civic: notebooklm-sync` Task 또는 `notebooklm-publisher` 에이전트로 동기화.
4. 변경분만 업로드되며, 결과는 회고에 기록됩니다.

## manifest.yml 스펙

상세 필드는 [reference/manifest-schema.md](reference/manifest-schema.md)를 참조하세요.
최소 예시:

```yaml
notebook_id: ""               # 최초 업로드 시 비워두면 publisher가 채움
title: "OO시 2026 본예산 분석"
update_policy: replace        # replace | append
visibility: public            # public | unlisted | private
sources:
  - path: archive/processed/budget/2026-overview.md
    citation: https://www.oo.go.kr/budget/2026
  - path: archive/processed/budget/2026-debates.md
```

## 권장 운영

- 노트북 1개 = 주제 1개. 폭이 넓어지면 분리합니다.
- `update_policy: replace`가 기본. `append`는 시리즈 글에만 사용합니다.
- 비공개로 시작 → 사실 검증 후 공개로 전환을 권장합니다.

## MCP 서버

이 저장소의 1차 커밋 시점에는 `notebooklm-bridge` 서버가 placeholder입니다.
실 업로드는 [PleasePrompto/notebooklm-mcp]를 직접 등록하거나, 후속 단계에서 자체 래퍼를 추가합니다.

[PleasePrompto/notebooklm-mcp]: https://github.com/PleasePrompto/notebooklm-mcp
