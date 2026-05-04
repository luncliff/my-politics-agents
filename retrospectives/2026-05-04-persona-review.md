---
date: 2026-05-04
slug: persona-review
duration_min: 35
---

## 시도한 것
- 분당뉴스 기사 기반의 지역주민 관점 persona review를 시작하고, local panel 생성 경로를 먼저 검증했다.
- Nemotron sampler가 raw parquet 지역 필드명을 잘못 가정하는 문제를 찾아 `sido`/`sigungu`를 `province`/`district`로 교체했다.
- `location.txt`의 광역명과 기초지역 파싱을 raw 데이터 표기에 맞게 정규화했다.

## 성공한 것
- `성남시 분당구-100.jsonl` local panel 생성에 성공했다.
- 기사에 대한 local panel 10명 반응과 종합 리뷰를 `archive/processed/persona-reviews/`에 저장했다.
- raw parquet 스키마 기준으로 sampler와 문서 표기를 일치시켰다.

## 막힌 것 / 다음에 해결
- 첫 local sampling은 `경기도` vs `경기`, `분당구` vs `성남시 분당구` 불일치로 빈 pool이 발생했다.
- 두 번째 subagent 호출이 잘못된 UUID를 반환해 재호출로 복구했다.
- 다음에는 persona review workflow에서 샘플 추출과 서브에이전트 호출을 반자동 스크립트로 묶는 편이 안전하다.

## 새로 알게 된 사이트·포맷·정책
- Nemotron raw parquet는 `province`, `district` 컬럼을 사용하며 값은 `경기-성남시 분당구`처럼 축약·접두 결합 형식일 수 있다.
- local sampling은 `location.txt`의 한국어 행정구역명을 raw 표기와 맞추는 정규화 단계가 필요하다.

## 자동화 후보
- skill: persona-perspective-review에서 local panel 샘플 추출, 5명 묶음 subagent 호출, 분포 집계를 자동화
- agent: civic-persona-panel 응답에서 요청 UUID 강제 검증과 재시도 로직 추가
- task: local panel 생성 후 기사 URL을 받아 review 초안을 만드는 task
- hook: nemotron sampler에서 raw schema 검증 시 `sido`/`sigungu` 사용 흔적을 경고

## 출처·PII 점검 결과
- 출처 누락 0건. 리뷰 파일에 기사 URL과 dataset 출처·면책을 포함했다.
- PII 삽입 0건. 합성 페르소나에 추가 개인정보를 넣지 않았다.