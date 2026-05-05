# 보고서 생성 참고문서 (Policy Brief · Technical Writing)

기준: 2026-05 · 대표 출처: UN Editorial Manual, Microsoft Writing Style Guide, Google Technical Writing

## 0) 목적

- 여러 조사 산출물(브리프/매트릭스/로그)을 **검토자용 1장(원페이지)** 보고서로 취합하기 위한 작성 규칙.
- “풍부한 설명” 대신 **짧고 스캔 가능한 구조**(표/불릿/다이어그램)로 사실관계를 전달.
- 사실정보만으로 맥락 파악이 어려운 영역(행정절차·예산구조·R&R)은 **최소한의 보조 프로세스 시각화**로 해소.

## 1) 원페이지 Policy Brief 공통 구조 (OECD·UN 관행 기반)

> 참고: 본 실행 환경에서 `oecd.org`, `oecd-ilibrary.org`가 HTTP 403으로 접근 불가(2026-05-05 확인). OECD 원문 근거는 추후 접근 가능 시 본 문서에 **1차 출처로 보강**한다. 현재는 UN 정책 문서 관행 + 일반적 국제기구 브리프 관행으로 구조를 제시한다.

### 1.1 문서 뼈대(권장)

1. **제목(한 줄)**: 사업/의제 + 지역(또는 범위)
2. **BLUF (Bottom Line Up Front)**: 3~5개 불릿
3. **핵심 사실(Confirmed Facts)**: 표 1개(가능하면 8~12행 이내)
4. **미확인/공백(Open Questions)**: 5~10개 체크리스트
5. **행정 프로세스 시각화(1개)**: Mermaid flowchart 1개
6. **용어 상자(Glossary)**: 6~12개
7. **출처(필수)**: 원문 URL·수집시각·sha256 또는 내부 파일 경로

### 1.2 BLUF 작성 규칙

- **정책판단/평가 금지**: “좋다/나쁘다” 대신 “무엇이 확인되었나/비었나”.
- “~추진”처럼 모호한 표현 대신 **단계/주관/재원/범위/일정** 중 최소 2개를 포함.
- 예시(형식):
  - `확인: {사업명}은 {계획/예산/의회}에 {연도/회기} 기준으로 반영됨 (근거: …)`
  - `미확인: {핵심값} (다음 탐색 경로: …)`

## 2) Technical Writing 핵심 규칙(요약)

### 2.1 문장

- **짧게**(한 문장 한 메시지), **능동태** 우선.
- 전문용어는 첫 등장 시 괄호로 1회만 풀이.
- 수치·기간·기관명은 생략하지 말고 **형식 통일**.

### 2.2 구조(스캔 가능성)

- 표/불릿 우선, 문단은 3~4줄을 넘기지 않는다.
- 헤딩은 “명사형”으로 통일: `현황`, `확인된 사실`, `미확인`, `근거`.
- 동일 범주의 항목은 **MECE**(겹치지 않고 빠짐없게)로 묶는다.

### 2.3 독자 가정

- 독자는 행정절차를 모른다고 가정하고, 다이어그램과 용어 상자로 해결한다.
- 그러나 본문을 길게 늘리지 않는다(본문은 **증거-사실-공백**만).

## 3) 사실정보 처리(검증가능성 중심)

### 3.1 Claim 단위로 쪼개기

- “역 신설 추진” 같은 문장은 최소 다음 4개 클레임으로 분해:
  - (a) 계획 반영 여부
  - (b) 주관기관/협의 주체
  - (c) 단계(사전타당성/기본계획/설계/공사)
  - (d) 일정/재원

### 3.2 판정 레이블(3개만)

- `입증됨`: 공식 원문 2건 이상 **또는** 1건 + 예산/의안/공고 등 교차근거
- `부분 입증`: 공식 원문 1건은 있으나 핵심 필드 공백 존재
- `미확인`: 원문 URL 부재 또는 핵심 필드 실질 공백

### 3.3 증거 표준 필드

표에는 최소 다음 열을 유지:

- `Fact ID`
- `문장(클레임)`
- `판정`
- `현재 단계`
- `주관기관`
- `범위(대상/구간/규모)`
- `일정(기준일 포함)`
- `재원/예산`
- `근거(원문 제목+링크 또는 내부 파일 경로)`

선택 열(맥락 보조):

- `R&R(누가 결정/집행/운영/유지관리?)`
- `운영·유지관리(주체/비용/인력)`

## 4) 범주화(카테고리) 기준

- 1차 축(정책영역): 교통/교육/시설운영/안전/개발
- 2차 축(행정형태): 계획·예산·설계·공사·운영/유지관리
- 3차 축(기관): 시청/의회/도/교육청/국토부·대광위/기타

> 같은 기관·같은 행정형태는 한 덩어리로 처리하면 중복 파일이 줄어든다.

## 5) 행정 프로세스 시각화(Mermaid 템플릿)

### 5.1 철도/역·연장/환승센터(일반형)

```mermaid
flowchart LR
  A[정책 구상/공약] --> B[사전검토·수요/대안]
  B --> C[사전타당성]
  C --> D[국가/광역 계획 반영]
  D --> E[재원협의·예산반영]
  E --> F[기본계획]
  F --> G[기본·실시설계]
  G --> H[착공]
  H --> I[준공]
  I --> J[운영·유지관리]

  classDef current fill:#ffe08a,stroke:#333,stroke-width:2px;
  %% 사용 시 현재 단계 노드에 class 적용: class F current;
```

### 5.2 학교 증축/시설 확충(일반형)

```mermaid
flowchart LR
  A[수요진단(학생/학급)] --> B[교육청/지자체 협의]
  B --> C[기본계획·중기계획 반영]
  C --> D[예산 편성]
  D --> E[설계]
  E --> F[공사]
  F --> G[준공]
  G --> H[운영·유지관리]

  classDef current fill:#ffe08a,stroke:#333,stroke-width:2px;
```

### 5.3 “현재 조사 위치” 표기 규칙

- 다이어그램 1개만 싣고, 현재 단계 노드에 `current` 클래스를 적용.
- 다이어그램 아래에 1줄로 적는다:
  - `현재 확인 범위: {C~E 단계 중 E(예산반영)까지 부분 입증}`

## 6) 최종 보고서 템플릿(원페이지)

```markdown
---
title: "<제목>"
created_at: "<ISO-8601>"
scope: "<지역/대상>"
principle: "facts-only / verifiable"
---

# <제목>

## BLUF (3~5)
- 확인: ...
- 확인: ...
- 부분 입증: ...
- 미확인: ...

## 확인된 사실 (표)
| Fact ID | 클레임 | 판정 | 단계 | 주관 | 범위 | 일정 | 재원/예산 | 근거 |
|---|---|---|---|---|---|---|---|---|
| T-01 | ... | 입증됨 | ... | ... | ... | ... | ... | ... |

## 미확인/공백 (다음 조사 입력)
- [ ] ... (다음 탐색: ...)

## 행정 프로세스(현재 위치)
```mermaid
...
```

## 용어
- 예타: ...

---
출처: (아래 ‘Source Log’)
```

## 7) Source Log(한 문서 안에 포함)

- 내부 파일은 `repo-relative path`로, 외부 URL은 `collected_at + sha256`로 남긴다.
- 외부 URL은 가능하면 `archive/raw/...`에 원문 보존 후 인용 메타를 붙인다.

## 8) 이번 문서의 최소 준수 체크리스트

- [ ] BLUF 5개 이하
- [ ] 표 1개(12행 이하 권장)
- [ ] 다이어그램 1개
- [ ] 미확인 10개 이하로 압축(가장 중요한 공백만)
- [ ] 출처/해시/경로 누락 0

---
## 수집 출처(원문 보존)

> 아래는 본 문서 작성에 사용한 1차 출처의 **원문 보존(archive/raw) 메타**이다.
> 라이선스는 각 원문 페이지의 표기를 따른다(본 문서에는 요약/구조만 반영).

### UN Editorial Manual Online
- 보존: `archive/raw/www.un.org/editorial-manual`
```yaml
source_url: "https://www.un.org/dgacm/en/content/editorial-manual"
collected_at: "2026-05-05T06:37:15Z"
content_sha256: "0e5e62f61fc8cbf59f3fa374aa73140d287e13a93e51d6892a1b14ac9a4f166d"
```

### UN Editorial Manual (PDF)
- 보존: `archive/raw/digitallibrary.un.org/United_Nations_Editorial_Manual.pdf`
```yaml
source_url: "https://digitallibrary.un.org/record/134841/files/United_Nations_Editorial_Manual.pdf"
collected_at: "2026-05-05T06:37:35Z"
content_sha256: "dc53b86950d2011e94558e007ab12c8549376cc82f92604844c038b0abf86a20"
```

### Microsoft Writing Style Guide
- 보존: `archive/raw/learn.microsoft.com/welcome`
```yaml
source_url: "https://learn.microsoft.com/en-us/style-guide/welcome/"
collected_at: "2026-05-05T06:36:19Z"
content_sha256: "14051ebcd3b8953c4171766b76b0f41788edc5e68086dafb9d0218a8862cbc1b"
```

### Google Technical Writing
- 보존: `archive/raw/developers.google.com/tech-writing`
```yaml
source_url: "https://developers.google.com/tech-writing"
collected_at: "2026-05-05T06:36:20Z"
content_sha256: "cd95a8e74f6e7774dcc977dc337c8e0c2cb0eba89181cd815c4ebca20a252dfe"
```

