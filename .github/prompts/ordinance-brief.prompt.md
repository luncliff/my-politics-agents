---
description: 조례안 한 페이지 브리핑 작성
mode: agent
tools: ["gov-archive/archive_search", "gov-archive/archive_cite", "filesystem"]
---

# 조례 브리핑 (ordinance-brief)

목표: 지정된 조례안(또는 개정안)을 **한 페이지 브리핑**으로 정리한다.

## 입력

- `source_path` 또는 `source_url`: 대상 조례안 (필수)
- `comparison`: 현행 조례 경로/URL (선택)

## 산출물 섹션

1. 한 줄 요약 (목적 + 영향 대상)
2. 핵심 변경점 (현행 ↔ 개정안 표)
3. 예상 효과 / 부작용 (사실 + 추정 분리)
4. 비용·재원 (있는 경우만)
5. 절차 일정 (입법예고 / 상임위 / 본회의)
6. 출처 (원본 URL, 입안자, 회의록 링크)

저장 경로: `archive/processed/ordinances/<slug>.md`
