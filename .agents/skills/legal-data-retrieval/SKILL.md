---
name: legal-data-retrieval
description: "legalize-kr 저장소 및 공식 소스(law.go.kr)에서 한국 국가 법령(법률·시행령·시행규칙)을 효율적으로 검색·획득·가공한다. Use when: 특정 법률 본문 조회, 시행령/시행규칙 연계 확인, 법령 개정 이력 분석, 법령 메타데이터(MST·시행일) 추출. 지방자치단체 조례·자치법규는 이 스킬 대신 `local-ordinance-processor`를 사용한다."
---

# legal-data-retrieval

한국의 국가 법령(법률·시행령·시행규칙)을 `legalize-kr` GitHub 저장소와 공식 소스에서 획득하고, 분석·인용에 적합한 마크다운으로 정리한다.

## 적용 범위

- ✅ 국가 법령: 법률, 시행령, 시행규칙, 대통령령, 총리령, 부령
- ❌ 지방자치법규·조례 → `local-ordinance-processor` 또는 `gokr-fetch` 사용
- ❌ 회의록·고시 → 각각 `assembly-minutes`, `gokr-fetch` 사용

## 워크플로우

### 1. 법령 유형 식별

요청에서 다음을 명확히 한다:

- 법령명(예: `민법`, `지방자치법`)
- 종류: 법률 / 시행령 / 시행규칙
- 시점: 현행 / 특정 시행일 / 개정 이력

지방자치법규로 판단되면 즉시 중단하고 `local-ordinance-processor`로 위임한다.

### 2. 데이터 획득

**기본 경로 — legalize-kr Raw URL**

```
https://raw.githubusercontent.com/legalize-kr/legalize-kr/master/kr/{법령명}/법률.md
https://raw.githubusercontent.com/legalize-kr/legalize-kr/master/kr/{법령명}/시행령.md
https://raw.githubusercontent.com/legalize-kr/legalize-kr/master/kr/{법령명}/시행규칙.md
```

- 법령명은 **반드시 UTF-8 URL 인코딩**한다(공백·괄호·한자 포함 시 필수).
- 원본은 `archive/raw/<host>/<basename>`으로 보존하고 SHA-256을 기록한다.
- 파일명에 수집일 접두어를 붙이지 않으며, 시간순 정렬은 `.meta.json`의 `collected_at`을 기준으로 한다.
- `gov-archive/archive_fetch`를 우선 사용하면 보존·해시·인용이 자동화된다.

**보조 경로**

1. Raw URL이 404인 경우: `site:github.com/legalize-kr/legalize-kr {법령명}` 검색으로 정확한 폴더명 확인.
2. legalize-kr에 없는 경우: 공식 출처 `https://www.law.go.kr`에서 `gokr-fetch`로 받는다.

### 3. 연계 규정 점검

법률 분석 시 **반드시** 동일 디렉터리에서 다음을 함께 확인한다:

- `시행령.md` (있으면 함께 수집)
- `시행규칙.md` (있으면 함께 수집)
- 부속 별표·서식

세 가지가 일관된 시행일을 가지는지 교차 검증한다.

### 4. 이력 분석 (요청 시)

- 커밋 단위 변경: `site:github.com/legalize-kr/legalize-kr {법령명}` + GitHub commits 페이지.
- 정밀 diff가 필요하면 사용자 승인 후 sparse-checkout으로 해당 디렉터리만 클론:
  ```pwsh
  git clone --filter=blob:none --sparse https://github.com/legalize-kr/legalize-kr.git
  cd legalize-kr; git sparse-checkout set "kr/{법령명}"
  ```
- 저장소는 `archive/raw/legalize-kr/`에만 두고 작업 후 정리.

### 5. 가공·저장

- 원본: `data/raw/laws/<법령명>/<종류>.md` (UTF-8, BOM 없음)
- 가공본: `data/processed/laws/<법령명>/<종류>.md`
- 가공본 상단에 메타데이터 주석을 둔다(grep 가능, 렌더링 시 숨김).

## 마크다운 표준 양식

```markdown
<!--
[요약 설명]
{법령의 목적·적용 범위를 1~3문장 요약}

[법령 메타데이터]
- 법령명: {정식 명칭}
- 종류: {법률|시행령|시행규칙}
- MST: {법령마스터번호, 알면}
- 시행일: {YYYY-MM-DD}
- 공포일/공포번호: {YYYY-MM-DD / 제0000호}
- 소관부처: {부처명}
- 연계: {함께 확인할 시행령/시행규칙}
-->

# {법령 명칭} ({종류})

{원문 텍스트, 「제○조」 헤딩 정리 허용}

## 개정 이력

- {YYYY-MM-DD} {제0000호}: {개정 요지}
  - 출처: {URL} · sha256:{짧은해시}

---
출처: {원본 URL} · 수집 {ISO-8601} · sha256:{짧은해시}
```

## 완료 체크리스트

- [ ] 원본이 `archive/raw/`에 보존되고 SHA-256이 기록되었는가
- [ ] 법령명이 URL 인코딩되어 Raw URL이 정상 응답했는가
- [ ] 법률·시행령·시행규칙 연계가 점검되었는가
- [ ] 메타데이터 주석에 종류·시행일·공포번호가 채워졌는가
- [ ] 가공본이 `data/processed/laws/<법령명>/`에 저장되었는가
- [ ] 출처 footer(URL·수집 시각·해시)가 포함되었는가

## 예시 URL

- 민법: `https://raw.githubusercontent.com/legalize-kr/legalize-kr/master/kr/%EB%AF%BC%EB%B2%95/%EB%B2%95%EB%A5%A0.md`
- 지방자치법: `https://raw.githubusercontent.com/legalize-kr/legalize-kr/master/kr/%EC%A7%80%EB%B0%A9%EC%9E%90%EC%B9%98%EB%B2%95/%EB%B2%95%EB%A5%A0.md`

> 주의: 위 두 번째 예시의 원래 명세에 있던 `체방자치법`은 오타로 추정. `지방자치법`으로 정정.

## 안전·정책

- legalize-kr는 커뮤니티 미러이므로 **법적 효력의 최종 판단은 `law.go.kr` 공식본을 기준**으로 한다. 차이가 발견되면 채팅에 보고한다.
- robots.txt·rate-limit 준수. 동일 파일 반복 다운로드 금지(캐시 활용).
- 법령 본문은 공공누리 4유형(공공저작물)로 간주하되, 가공본 footer에 출처를 항상 명시.
- PII는 일반적으로 없으나, 부칙·별표에 사람 이름이 등장하면 `pii-mask`를 통과시킨다.
