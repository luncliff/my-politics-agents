# gov-archive TODO

## 목표

- `gov-archive`를 정부 도메인 전용 서버에서 점진 확장형 아카이브 서버로 운영한다.
- 1순위 도메인은 `*.go.kr`, `*.or.kr`로 유지하고, 이후 `*.kr` 및 지방정부/지방의회 공식 사이트까지 확장한다.
- 파일명에는 수집 날짜를 강제하지 않고, 시간 추적은 sidecar metadata로 일원화한다.

## 저장 규칙 (확정)

- 저장 경로: `archive/raw/<host>/<basename>`
- 날짜 접두어: 사용하지 않음
- 원본 URL basename에 날짜/시각이 포함되어 있으면 그대로 재사용
- 시간순 추적 기준: `archive/raw/<host>/<basename>.meta.json`의 `collected_at`

## JSON 중심 운영 가이드

- 대용량 원문(PDF/XLSX/DOCX/HWP 등)은 Git 추적에서 제외 가능
- 최소 추적 단위는 `.meta.json` (필수 필드: `source_url`, `collected_at`, `sha256`, `content_type`)
- 문서 목록/정렬/감사 추적은 파일명이 아니라 `collected_at`으로 수행

## 도메인 확장 로드맵

1. Phase 1 (현재 우선)
- `*.go.kr`, `*.or.kr` 기본 지원
- 지방정부/지방의회 공식 사이트 우선 수집

2. Phase 2 (점진 확장)
- `*.kr` 도메인 일반 공공기관 사이트 지원
- 도메인별 신뢰도/승인 정책 문서화

3. Phase 3 (비정부 도메인 확장)
- 정책상 허용된 외부 도메인 지원
- robots/rate-limit/출처 검증 체크리스트 강화

## 구현 TODO

- [x] `archive_fetch` 파일명 날짜 접두어 제거
- [x] `archive_fetch` 회귀 테스트 추가 (날짜 접두어 미사용 검증)
- [x] `AGENTS.md` 아카이브 명명 규칙 갱신
- [x] `gokr-fetch` 스킬 규칙 갱신
- [x] `researcher-kr-website` 에이전트 저장 규칙 갱신
- [x] `collect-site` 프롬프트 저장 규칙 갱신
- [x] 관련 스킬(`local-ordinance-processor`, `legal-data-retrieval`) 저장 규칙 갱신
- [x] `.gitignore`에서 `.meta.json` 추적 가능하도록 조정
- [ ] `archive_cite`가 원본 파일 없이 `.meta.json`만으로도 동작하도록 옵션 확장
- [ ] `.meta.json` 기준 시간순 인덱스 생성 스크립트 추가 (`archive/processed/...`)
- [ ] 도메인 정책(우선/확장/예외)을 `docs/`에 별도 표준 문서로 분리
