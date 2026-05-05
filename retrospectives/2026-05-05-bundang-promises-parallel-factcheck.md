---
date: 2026-05-05
slug: bundang-promises-parallel-factcheck
duration_min: 16
---

## 시도한 것
- `공약검토-대장동/백현동/운중동/판교동.md`의 `다음 단계 제안` 추가 확인 항목을 공통 fact 축으로 재구성했다.
- 지역별 공식자료 조사, 의회 근거 수집, 예산 보강, 교통 단계 검증, 약점 보강, 축별 병합을 병렬 subagent로 운영했다.
- 최종적으로 축별 병합본을 `final-fact-matrix.md`와 `source-log.md`로 통합했다.

## 성공한 것
- `archive/processed/promise-factcheck/` 아래에 지역별 브리프, 교차검증 브리프, 축별 병합본, 최종 매트릭스, source log를 남겼다.
- 조사 기준을 공식 원문 우선, facts only, `입증됨/부분 입증/미확인` 3단계로 통일했다.
- `plan.md`를 문서별 계획에서 공통 조사축 계획으로 재정렬했다.

## 막힌 것 / 다음에 해결
- 일부 subagent가 파일 저장 대신 초안만 반환해 수동 저장본을 보정했다.
- `T-06`, `T-07`, `F-04`, `S-05`, `D-03`은 공식 원문이 부족해 미확인으로 남았다.
- 다음에는 최종 병합 전 `archive/raw` 보존과 SHA-256 메타 생성까지 자동 연결해야 한다.

## 새로 알게 된 사이트·포맷·정책
- 성남시 철도사업 현황 페이지가 교통축 기본 진입점으로 유용했다.
- 성남교육지원청/학교 공지 URL이 학교 과밀·증축 확인의 핵심 원문이었다.
- 이 환경에서는 background agent가 파일 저장을 실패할 수 있어 후속 존재 확인이 필요했다.

## 자동화 후보
- skill: 축별 병합 결과를 자동으로 `final-fact-matrix.md`와 `source-log.md`로 합치는 팩트체크 통합 skill
- agent: 성남시 예산서·의회 의안·교통사업 단계 문서를 묶어 판정까지 해주는 분당 공약 팩트체크 agent
- task: agent 반환 파일 미저장 시 자동으로 초안을 저장본으로 고정하는 post-process task
- hook: `archive/processed/promise-factcheck/**` 생성 시 raw 보존 여부와 source-log 누락을 검사하는 hook

## 출처·PII 점검 결과
- PII 노출 확인 없음.
- 최종 산출물은 공식 원문 URL 중심으로 정리했다.
- raw 보존·SHA-256 메타는 이번 세션에서 일괄 완료하지 못했고 후속 자동화 후보로 남겼다.
