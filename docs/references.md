---
description: LLM-friendly reference index for Gyeonggi and Seongnam research context
scope: gyeonggi-seongnam
last_updated: 2026-05-01
source_documents:
  - docs/references-경기도.md
  - docs/references-성남시.md
  - docs/research-seongnam-open-data.md
---

# Reference Index

이 문서는 LLM이 빠르게 읽고 재사용할 수 있도록 경기도·성남시·판교 관련 context를 구조화한 기본 Reference입니다.

## 1. Scope

| Key | Value |
| --- | --- |
| Primary region | 경기도 / 성남시 |
| Secondary focus | 판교 생활권 |
| Main use cases | 정책 조사, 의정 조사, 공개데이터 수집, 오버레이 후보 선정 |
| Canonical context files | `docs/references-경기도.md`, `docs/references-성남시.md`, `docs/research-seongnam-open-data.md` |

## 2. Source Priority

LLM은 아래 우선순위로 자료를 탐색한다.

| Priority | Source type | Why |
| --- | --- | --- |
| 1 | 대한민국 공식 전자정부 누리집 | 공식성, 안정성, 재현성 |
| 2 | 성남시청 공식 홈페이지 | 현지 행정 문서와 게시판 자료 보강 |
| 3 | 광역·산하기관 공식 포털 | 경기도, 경기도의회, 경기연구원 등 보조 근거 |

## 3. Canonical Entry Points

### 3.1 Governance and law

| Topic | Primary entry points |
| --- | --- |
| 국가 법령 | 국가법령정보센터, 법제처 AI 법령검색 |
| 자치법규 | ELIS, 성남시 자치법규, 경기도 자치법규 |
| 의정자료 | 성남시의회, 경기도의회 |

### 3.2 Statistics and finance

| Topic | Primary entry points |
| --- | --- |
| 통계 | 성남통계, KOSIS, 경기통계 |
| 재정·결산 | 성남시 재정정보, 지방재정365, 부서별공개자료실 |
| 연구자료 | 성남시 맞춤형 정책연구, PRISM, 경기연구원, 성남시정연구원 |

### 3.3 Public data and local portals

| Topic | Primary entry points |
| --- | --- |
| 공공데이터 | data.go.kr, 경기데이터드림 |
| 시청 공개정보 | 사전 정보공표, 재정정보, 부서별공개자료실 |
| 생활정책 포털 | 성남 청년포털, 교육 관련 경기교육 포털 |

## 4. Decision Rules

LLM은 아래 규칙에 따라 자료원을 선택한다.

| If the task is about... | Prefer... | Avoid / Note |
| --- | --- | --- |
| 법률, 시행령, 시행규칙 | law.go.kr, `legal-data-retrieval` | 조례와 혼동하지 말 것 |
| 조례, 시 규칙, 자치법규 | ELIS, 광역의회 및 지방의회 의안검색, law.go.kr | ELIS로 최신 목록 확인 → 의회로 최신 입법 동향 확인 → law.go.kr로 최종 본문 검증 |
| 성남시 통계 | 성남통계, KOSIS | 블로그·2차 가공자료 우선 사용 금지 |
| 성남시 예산·결산·기금 | 성남시 재정정보, 지방재정365 | 게시판 자료는 보조 근거로 사용 |
| 좌표 기반 시설 데이터 | data.go.kr OpenAPI 또는 파일데이터 | 서비스키 필요 여부 확인 |
| 현안별 내부 행정자료 | 성남시 부서별공개자료실 | 정형 API가 아니므로 수동 검토 가능성 높음 |

## 4. Ordinance Reorganization Rules

- 성남시 조례는 행정 부서 구조보다 **주제별(Semantic)** 구조를 기본 저장 구조로 사용한다.
- 분류 기준은 조례 제목과 제1조 목적이며, 최종적으로는 `local-ordinance-processor`의 6개 카테고리(`일반행정`, `보건복지`, `교통안전`, `산업경제`, `도시환경`, `교육문화`) 중 하나를 선택한다.
- 최신 수집의 1차 출발점은 ELIS이고, 2차 검증은 성남시의회 의안검색, 3차 검증은 law.go.kr이다.
- 저장 시 원문은 `archive/raw/`에 먼저 보존하고, Markdown 변환본은 주제별 폴더에 `<지자체>-<카테고리>-<조례명>.md` 형태로 누적한다.
- 메타데이터는 최소 `시행일`, `소관부서`, `공포번호`, `원본 URL`, `수집 시각`, `sha256`을 포함한다.

## 5. Open Data Summary

### 5.1 Highest-priority map-ready datasets

| Dataset | Type | Access | Geometry readiness | Primary use |
| --- | --- | --- | --- | --- |
| 교통단속 카메라 | OpenAPI | 서비스키 필요 | High | 교통 단속 인프라 지도 |
| 교통약자 보호구역 | OpenAPI | 서비스키 필요 | High | 스쿨존·보행안전 지도 |
| 보행자 전용도로 | OpenAPI | 서비스키 필요 | Medium | 보행 인프라 지도 |
| 옐로우 카펫 | OpenAPI + CSV | 서비스키 또는 파일 다운로드 | High | 통학 안전 레이어 |
| 버스정류장 현황 | CSV | 바로 다운로드 가능 | High | 생활권 대중교통 레이어 |
| 신분당선 역위치 | CSV | 바로 다운로드 가능 | High | 판교 광역교통 레이어 |
| 성남사랑상품권 가맹점현황 | OpenAPI | 서비스키 필요 | Medium | 생활경제 분포 분석 |

### 5.2 Secondary map-support datasets

| Dataset | Type | Extra processing needed | Main note |
| --- | --- | --- | --- |
| 전국초등학교통학구역표준데이터 | CSV/XML/JSON | High | 성남교육지원청 기준 필터링 필요 |
| 보행자 우선도로 후보지 | OpenAPI | Medium | 정책 후보 구간 해석 필요 |
| 험프형 횡단보도 설치현황 | CSV | Medium | 주소 좌표화 필요 |
| 교통신호기 시설물현황 | CSV | Medium | 위치 정규화 필요 |
| 버스노선 현황 | CSV | Medium | 선형 데이터 아님 |
| 버스정보안내단말기 현황 | CSV | Low | 정류장 데이터와 결합 가치 높음 |
| 공항버스 시간표 | XLSX | Medium | 정류장 경로 정리 필요 |

### 5.3 Aggregate or analytical datasets

| Dataset | Unit | Best use |
| --- | --- | --- |
| 인구및세대 현황 | 동 단위 | 인구 구조 비교, choropleth |
| 차량등록 차종별 통계현황 | 법정동/구 단위 | 교통 수요 간접 지표 |
| 벤처기업현황 | 기업 단위 | 산업 구조 분석 |
| 공동주택현황 | 단지 단위 | 주거 밀도·생활권 분석 |
| 지식산업센터 현황 | 시설 단위 | 산업 입지 분석 |
| 판교테크노밸리 입주기업현황 | 단지/기업군 단위 | 판교 산업 생태계 분석 |

## 6. Topic-to-Source Map

| Topic | Best starting points | Typical outputs |
| --- | --- | --- |
| 도시계획 | 성남시 도시계획조례, 성남시청, 공공발주사업 공개 | 조례 요약, 사업 자료 목록 |
| 재정 | 성남시 재정정보, 지방재정365, 부서별공개자료실 | 예산서, 결산서, 집행 현황 |
| 청년정책 | 성남 청년포털, 온통청년, 부서별공개자료실 | 시행계획, 사업 요약 |
| 교육정책 | 경기도교육청, 경기교육연구원, 통학구역 표준데이터 | 학구 분석, 교육 통계 |
| 교통 | data.go.kr, 성남시 자동차 통계, 철도 데이터 | 지도 레이어, 교통 지표 |
| 산업·경제 | 성남 지역경제 통계, 벤처기업현황, 판교테크노밸리 데이터 | 산업 입지 요약, 기업 분포 |
| 의회·감사 | 성남시의회, 경기도의회 | 회의록, 의안, 상임위 자료 |
| 선거·공약 | NEC 선거통계, 정책·공약마당 | 선거 통계, 공약 자료 |

## 7. Working Notes for Agents and Skills

### 7.1 When to use this file

- 성남시 또는 판교 관련 주제를 처음 받았을 때
- 어느 포털에서 먼저 조사해야 할지 정해야 할 때
- 지도 오버레이 후보와 통계형 자료를 구분해야 할 때
- Skill이나 Agent가 도메인 entry point를 빠르게 찾아야 할 때

### 7.2 Suggested follow-up docs

| Need | Read next |
| --- | --- |
| 경기도 링크 모음 | `docs/references-경기도.md` |
| 성남시 링크 모음 | `docs/references-성남시.md` |
| 데이터셋별 활용 판단 | `docs/references-성남시-공개데이터.md` |
| NotebookLM 업로드 규칙 | `docs/manifest-schema.md` |
| 저장소 구조와 역할 | `docs/architecture.md` |
| 정책·보안 원칙 | `docs/governance.md`, `docs/security.md` |

## 8. Known Constraints

| Constraint | Impact |
| --- | --- |
| OpenAPI 다수는 서비스키 필요 | 자동 수집 전 승인·인증 확인 필요 |
| 부서별공개자료실은 게시판형 | 크롤링보다 수동 검토 또는 별도 수집 로직이 적합 |
| 차량등록 통계는 법정동 기준 | 행정동 경계와 직접 매핑 시 변환 필요 |
| 벤처기업 주소는 인증 시점 기준 가능성 | 최신 위치 분석에는 검증 필요 |
| 우회전 사각지대 데이터는 요청형 제공 | 즉시 자동화 대상이 아님 |

## 9. Immediate Research Priorities

1. 교통약자 보호구역, 옐로우 카펫, 보행자 전용도로, 보행자 우선도로 후보지의 응답 스키마 확인.
2. 통학구역 표준데이터를 성남교육지원청 기준으로 필터링하는 절차 정리.
3. 버스정류장, 버스노선, BIT, 신분당선, 경강선의 결합 모델 설계.
4. 공동주택, 지식산업센터, 판교테크노밸리 입주기업현황을 생활권 분석 지표로 재정리.
5. 성남시청 사전 정보공표와 재정정보 메뉴를 추가 점검.

## 10. Maintenance Rule

- 새로운 경기도/성남시 context 문서가 생기면 이 파일의 `source_documents`와 해당 섹션만 갱신한다.
- 세부 링크 카탈로그는 `docs/references-경기도.md`, `docs/references-성남시.md`에 유지하고, 이 파일에는 의사결정에 필요한 요약만 둔다.
- 데이터셋 세부 메모는 `docs/research-seongnam-open-data.md`에 유지하고, 이 파일에는 우선순위와 활용 판단만 둔다.