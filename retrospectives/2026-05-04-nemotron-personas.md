# 2026-05-04 — Nemotron-Personas-Korea 시민 패널 도입

## 무엇을 시도했는가

NVIDIA Nemotron-Personas-Korea(CC BY 4.0)를 워크스페이스 로컬에 보존하고, 합성 페르소나 패널을 활용한 정책·계획 사전 검토 기능을 저장소에 추가.

## 무엇이 성공했는가

- `adapters/py/nemotron_personas/`에 fetch + sampler 어댑터(uv 프로젝트) 추가.
  - parquet 옆에 `.meta.json` sidecar(sha256·source_url·license=CC BY 4.0·attribution).
  - stratified sampler(sido × sex × age_bucket, 셀당 최소 1명 floor) + location.txt 자동 인식 지역 패널.
- `.gitignore`에 parquet 제외 규칙 + processed jsonl·md 화이트리스트.
- `.vscode/tasks.json`에 4개 task 추가(dry-run, download, national, local).
- `.agents/skills/persona-perspective-review/` (SKILL + review-template) 신설.
- `.github/agents/civic-persona-panel.agent.md` 신설(party-advisor·researcher-kr-website 위임).
- `.github/prompts/persona-review.prompt.md` 슬래시 커맨드.
- `docs/references-nemotron-personas.md` 정책·인용·한계 정리.

## 무엇이 막혔는가 / 미완

- 실제 다운로드는 사용자 승인 후 실행해야 함(약 2 GB). 본 세션에서는 코드만.
- 패널 jsonl 생성·시뮬레이션 검증은 데이터 다운로드 후 수동 검증 필요.
- `/persona-review` 실사용 요청 검토 시 `archive/processed/nemotron-personas/panels/` 아래 `national-300.jsonl`, `분당구-100.jsonl` 부재로 실행 중단.
- `scripts/lint_frontmatter.py`가 `agents/*.agent.md`·`skills/*/SKILL.md` 루트 경로만 검사 → 본 저장소 실제 위치(`.github/agents/`, `.agents/skills/`)와 불일치. 별도 회고 항목.

## 새로 알게 된 사실

- 데이터셋 구성: 26 필드, 1M rows, 17 시도 × 252 시군구, 19세+ 성인만, 이름 필드는 동명이인 다수(가장 흔한 풀네임 "김영숙").
- gender(sex와 구분) 통계는 한국 공공데이터에 없어 데이터셋에 미반영.
- HuggingFace `hf_hub_download`은 local_dir 지정 시 repo 경로 그대로 mirror됨.

## 다음에 자동화할 후보

1. **lint_frontmatter.py 경로 보강**: `.agents/skills/*/SKILL.md`, `.github/agents/*.agent.md`도 검사하도록 TARGETS 갱신.
2. **persona-review 자동 실행 task**: `civic: persona review <doc>` 형식의 파라미터 task.
3. **패널 분포 검증 스크립트**: 산출 jsonl이 시도 17개·연령대 7개를 모두 덮는지 자동 assert.
4. **카드 임베딩 인덱스**: 검토 대상과 의미적으로 가까운 페르소나만 우선 추출(현재는 무작위 stratified).
