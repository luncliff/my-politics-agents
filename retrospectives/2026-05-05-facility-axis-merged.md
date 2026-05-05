---
date: 2026-05-05
slug: facility-axis-merged
duration_min: 20
---

## 시도한 것
- 분당 공약 팩트체크 병합 대상 F-01~F-06와 로컬 달빛도서관 관련 저장본을 우선 재확인했다.
- 지역별 official fact brief, 교차 의회 브리프, 예산 브리프, 약점 보강 브리프를 교차 대조했다.
- 달빛어린이병원·달빛도서관의 별도 공식 저장본 존재 여부를 저장소 전체에서 검색했다.

## 성공한 것
- `archive/processed/promise-factcheck/facility-axis-merged.md`에 facts only 표와 `남은 공백` 섹션을 저장했다.
- F-01, F-02, F-03, F-05는 기존 공식 브리프 기준으로 `부분 입증` 범위까지 병합했다.
- F-04는 예산 교차검증 브리프의 예산 단서만 반영하고 추정 없이 `부분 입증`으로 정리했다.

## 막힌 것 / 다음에 해결
- `cross-budget-fact-brief.md`는 최소 저장본만 있어 F-04 원문 URL을 회수하지 못했다.
- 달빛어린이병원 관련 공식 저장본이나 archive/raw 근거를 찾지 못해 별도 로컬 행은 달빛도서관 중심으로만 남겼다.
- F-06은 백현동 추가 경로당의 직접 계획 문서를 끝내 확보하지 못했다.

## 새로 알게 된 사이트·포맷·정책
- 같은 축 병합 파일이 이미 `education-axis-merged.md`, `safety-axis-merged.md` 형식으로 존재했다.
- `cross-budget-fact-brief.md`는 상세 원문이 아니라 회수된 핵심만 남긴 최소 저장본이었다.
- 판교권 로컬 달빛도서관 검토 저장본은 `archive/processed/persona-reviews/2026-05-04-ebundangnews-12561-local-library.md`에 있었다.

## 자동화 후보
- skill: F축 병합 시 `fact-matrix`와 지역별 brief에서 지정 fact ID만 자동 추출해 표 초안을 만드는 병합 skill
- agent: 달빛어린이병원·스마트도서관처럼 로컬 기사와 공식 근거를 분리 수집하는 생활인프라 검증 agent
- task: `cross-budget-fact-brief.md`의 최소 저장본에서 원문 URL 누락 항목을 자동 재탐색하는 예산 보강 task
- hook: 새 `*-axis-merged.md` 저장 직후 필수 컬럼·판정값·`남은 공백` 존재 여부를 검사하는 hook

## 출처·PII 점검 결과
- 출처 누락 1건: F-04는 기존 저장본 자체에 원문 URL이 없어 공식 URL 칸을 비워 두고 근거 파일만 남겼다.
- PII 누락 0건: 개인식별정보가 포함된 내용은 이번 산출물에 없었다.
