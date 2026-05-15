# 보관함/AGENTS.md — Originals, results, legal-data lookup

Scope: `보관함/` 하위. 공통 규약은 [/AGENTS.md](../AGENTS.md).

## 구성

- `보관함/다운로드/<host>/` — 외부에서 받은 **원본 (불변)**. 수정·삭제 금지. 시간순서는 `.meta.json`의 `collected_at`으로 추적.
- `보관함/결과/` — 처리·정리된 한국어 산출물 (Markdown). 기본은 **flat 구조**.
- `보관함/양식/` — 재사용 양식·템플릿.
- `보관함/{legalize,precedent,admrule,ordinance}-kr/` — 법령·판례·행정규칙·조례 로컬 클론 (`scripts/fetch_legalize_kr.*`로 생성).

## 파일명 규칙

- `보관함/결과/`, `보관함/양식/`, `data/processed/`, `notebooks/`, `회고/` 등 사용자용 한국어 산출물은 **한글 파일명**.
- `보관함/결과/`는 `<YYYY-MM> <한글 파일명>.md` 형태를 기본으로 한다.
- `보관함/다운로드/` 의 host·머신 식별 경로는 원어 그대로 유지 (예외).
- 코드·메타·로그·도구 설정은 영어 파일명.

## 폴더 구조 규칙

- `보관함/결과/`는 **flat**이 기본. dataset/panel/legal-review/timeline 등 명시적 규칙이 요구할 때만 하위 폴더 사용.
- 다른 산출물 트리도 명시 규칙이 있을 때만 하위 폴더 사용.

## 처리된 Markdown 형식

```markdown
---
title: "<title>"
source_url: "<original URL>"
collected_at: "<ISO-8601>"
content_sha256: "<hash>"
license: "KOGL Type 1"
pii_masked: true
---
# <title>

본문 …

---
출처: <original URL> · 수집 <ISO-8601> · sha256:<short hash>
```

## 법령·판례·자치법규 조회 우선순위

법령·판례·행정규칙·조례 검색 시 다음 순서를 따른다. **첫 번째로 충분한 결과를 주는 단계에서 멈춘다.**

| Tier | Source | Covers |
| --- | --- | --- |
| 1 — Local clone | `보관함/legalize-kr/kr/{법령명}/` | 법률·시행령·시행규칙 |
|  | `보관함/precedent-kr/{사건종류}/{법원등급}/` | 판례 |
|  | `보관함/admrule-kr/{기관경로}/{종류}/` | 행정규칙 (고시·훈령) |
|  | `보관함/ordinance-kr/{광역}/{기초}/{종류}/` | 자치법규 |
| 2 — `legalize-kr` MCP | MCP 도구 (`laws_*`, `precedents_*`, `admrules_*`, `ordinances_*`) | 위와 동일 범위 |
| 3 — Web | `law.go.kr`, `elis.go.kr`, 법원 사이트, 웹 검색 | 1·2가 부족할 때 공식 출처 |

### Bootstrap — `보관함/*-kr/` 누락 시

`보관함/*-kr/.git`이 없으면:

1. 사용자에게 클론이 비어있음을 알린다.
2. 다음 중 하나를 안내한다:
   - VS Code Task: `civic: fetch legalize-kr repos (shallow clone)`
   - PowerShell: `pwsh -ExecutionPolicy Bypass -File scripts/fetch_legalize_kr.ps1`
   - Bash: `bash scripts/fetch_legalize_kr.sh`
3. 클론 완료 전에는 Tier 2 (MCP) 또는 Tier 3 (Web)으로 폴백.

### 자치법규 지역 범위

`보관함/ordinance-kr/` 또는 MCP `ordinances_*` 조회 시:

- MUST 먼저 `location.txt`를 읽어 대상 광역·기초를 결정한다.
- MUST `보관함/ordinance-kr/{광역}/{기초}/` 경로로 검색 범위를 제한한다.
- 사용자가 명시적으로 다른 지역을 지정하지 않는 한 다른 지역의 조례를 참조하지 않는다.

## 금지

- `보관함/다운로드/` 파일을 수정·삭제하지 않는다.
- 원본은 개인 검토용이며 외부 공유 금지.
