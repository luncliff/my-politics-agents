# 조례·법령 한 페이지 브리핑

대상 조례 또는 법령을 한 페이지 브리핑으로 정리한다.

## 입력

`$ARGUMENTS` — 조례명 또는 법령명. 예: `성남시 버스 운송사업 지원 조례`

## 절차

1. `location.txt`를 읽어 현재 작업 지역을 확인한다.
2. `lawyer` 또는 `ordinance` 서브에이전트에 위임해 법률 데이터 조회 우선순위에 따라 본문을 수집한다:
   - Tier 1: `보관함/ordinance-kr/{광역}/{기초}/` 또는 `보관함/legalize-kr/`
   - Tier 2: `legalize-kr` MCP (`ordinances_get`, `laws_get`)
   - Tier 3: `elis.go.kr`, `law.go.kr`
3. 수집한 본문을 다음 형식으로 요약한다.
4. `보관함/결과/<YYYY-MM-DD> <조례명> 브리핑.md`에 저장한다.

## 출력 형식

```markdown
---
title: "<조례명> 브리핑"
source_url: "<원본 URL>"
collected_at: "<ISO-8601>"
content_sha256: "<해시>"
license: "KOGL Type 1"
pii_masked: true
---

## 핵심 요약 (3줄 이내)

## 주요 조항

| 조문 | 핵심 내용 |
|------|-----------|

## 개정 이력 (최근 3건)

## 상위 법령 연계

## 해석 유의 사항

---
출처: <URL> · 수집 <ISO-8601> · sha256:<단축해시>
```
