---
date: 2026-05-11
slug: legalize-kr-lookup-priority
duration_min: 45
---

## 시도한 것
- legalize-kr 관련 로컬 클론, MCP, web 조회 우선순위를 공통 규약과 에이전트/스킬에 반영했다.
- `legal-data-retrieval` 스킬 참조 지점을 찾아 정리했다.
- Codex CLI 설정에 `legalize-kr` MCP 서버를 추가했다.

## 성공한 것
- `AGENTS.md`에 Local clone -> MCP -> Web 규칙과 조례 지역 스코프를 명시했다.
- `lawyer-agent`, `ordinance-reviewer`, `ordinance-processor`, `researcher-kr-website`, `assembly-minutes`에 새 절차를 반영했다.
- `legal-data-retrieval` 스킬을 저장소에서 제거하고 참조를 정리했다.

## 막힌 것 / 다음에 해결
- PowerShell 출력에서 상대 경로 표기가 불안정해 grep 기반 검증으로 보완했다.
- `mcp-servers/gov-archive/TODO.md`에는 이번 커밋과 무관한 기존 변경이 있어 제외했다.

## 새로 알게 된 사이트·포맷·정책
- 법률 데이터 조회는 `data/*-kr` 로컬 클론을 1순위로 보고, 부족할 때만 `legalize-kr` MCP와 web으로 내려가는 규칙이 필요하다.
- 조례 조회는 `location.txt` 기반 지역 제한을 문서 수준에서 강제해야 한다.

## 자동화 후보
- skill: legal data lookup 검증용 검색/정합성 체크 스킬
- hook: staged 변경 중 정책상 제외 파일 감지 훅

## 출처·PII 점검 결과
- 외부 출처 신규 수집 없음
- PII 누락 없음