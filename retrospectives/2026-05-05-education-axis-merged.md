---
date: 2026-05-05
slug: education-axis-merged
duration_min: 12
---

## 시도한 것
- `bundang-promises` 하위 기존 브리프와 매트릭스를 먼저 읽어 E-01~E-04의 공식 근거 범위를 재확인했다.
- 누락 경로로 보인 `cross-budget-fact-brief.md`를 다시 찾아 실제 저장본을 확인했다.
- 교육·보육 축만 분리해 facts only 표와 `남은 공백` 섹션을 새 파일로 병합했다.

## 성공한 것
- `archive/processed/promise-factcheck/education-axis-merged.md`를 저장했다.
- E-01, E-02, E-04는 기존 공식 URL 기반으로 `부분 입증`으로 정리했다.
- E-03은 공식 수요·공간·역할분담 문서 부재를 근거로 `미확인`으로 고정했다.

## 막힌 것 / 다음에 해결
- 학교별 학생 수요·학급 수요·과밀 기준 수치는 공식 URL이 있는 문서로 확보되지 않았다.
- 급식실·체육관 증축의 세부 공사범위와 공사 중 수업 운영 계획 문서는 확보되지 않았다.
- 판교초 특수학급 설치의 수요·공간계획·교육청-시 역할분담 문서는 여전히 미확인이다.

## 새로 알게 된 사이트·포맷·정책
- `pangyodaejang-e.goesn.kr`, `pangyodaejang-m.goesn.kr` 학교 공지 형식이 교육시설 증축 근거의 직접 원문으로 쓰이고 있었다.
- `cross-budget-fact-brief.md`는 예산 세부표보다 “개별 예산항목 미확인” 공백 확인용 최소 브리프 역할을 한다.
- 이번 병합 규칙은 추정치 금지, 공식 URL 없는 수치 금지, 판정값 3종(`입증됨/부분 입증/미확인`) 고정이었다.

## 자동화 후보
- skill: 특정 fact ID 묶음을 기존 브리프들에서 자동 병합해 축별 facts only 표를 생성하는 merger skill
- agent: 교육·보육 fact ID만 추적해 학교 공지·교육청 문서·시 보도자료를 교차 판정하는 reviewer agent
- task: 지정 fact ID 목록의 공식 URL 유무와 공백 항목을 자동 점검하는 validation task
- hook: 새 축 병합 파일 저장 시 retrospective 초안 파일명을 자동 제안하는 종료 hook

## 출처·PII 점검 결과
- 출처 누락 0건. 기존 조사 결과에 있던 공식 URL만 사용했다.
- PII 노출 0건. 개인식별정보가 포함된 원문은 이번 산출물에 반영하지 않았다.
