---
description: 회의록을 사실/표결/쟁점으로 정리
tools: ["gov-archive/archive_search", "gov-archive/archive_cite", read, edit, search]
---

# 회의록 요약 (summarize-minutes)

목표: `archive/raw/...` 또는 사용자가 지정한 회의록(PDF/HWP/HTML 텍스트)을
**사실 카드** + **표결 표** + **쟁점 요약**으로 정리한다.

## 입력

- `source_path`: 정리 대상 파일/폴더 (필수)
- `audience`: 일반시민 | 보좌진 | 연구자 (선택, 기본: 일반시민)

## 절차

1. PII는 `pii-mask` 스킬로 선처리.
2. 회의 일자, 안건, 발언자(직책 단위), 표결 결과를 추출.
3. 사실 카드(인용 + 출처 링크)와 해석을 분리해 작성.
4. `archive/processed/minutes/<YYYY-MM-DD>-<slug>.md`로 저장.

## 출력 형식

```markdown
---
title: "<회의 제목> (YYYY-MM-DD)"
source_url: ...
collected_at: ...
content_sha256: ...
license: 공공누리 1유형
pii_masked: true
---

## 사실 카드
- ...

## 표결
| 안건 | 찬 | 반 | 기권 | 결과 |

## 쟁점 요약
- ...

## 해석 (작성자 추정)
- ...

---
출처: <원본 URL> · 수집 ...
```
