---
description: 합성 시민 페르소나 패널로 정책·계획 초안을 시점별로 검토
argument-hint: "<대상 문서 경로|붙여넣은 초안> [national|local|both] [N]"
tools: [read, search, edit, agent]
---

# /persona-review

`persona-perspective-review` 스킬을 호출해, 입력 문서를 Nemotron-Personas-Korea 기반
패널에 적용한 시민 시점 시뮬레이션과 종합 리뷰를 만든다.

## 인자

1. **대상**: 파일 경로 또는 붙여넣은 초안 (필수)
2. **패널**: `national` | `local` | `both` (기본 `both`)
3. **N**: 패널당 페르소나 수 (기본 `10`)

## 사전 조건

다음 산출물이 있어야 한다. 없으면 안내 후 종료한다.

- `archive/processed/nemotron-personas/panels/national-*.jsonl`
- `archive/processed/nemotron-personas/panels/<sigungu>-*.jsonl` (지역 패널 사용 시)

준비 명령:

```pwsh
# 1) 원본 parquet (~2GB) 다운로드
uv run python -m nemotron_personas.fetch
# 2) 전국 패널
uv run python -m nemotron_personas.sampler --panel national --size 300
# 3) 지역 패널 (location.txt 기반)
uv run python -m nemotron_personas.sampler --panel local --size 100
```

## 절차

1. `civic-persona-panel` 에이전트(또는 `persona-perspective-review` 스킬)를 호출한다.
2. 결정적 시드(기본 20260504)로 N명 추출, 서브에이전트로 4 항목 응답 생성.
3. 산출물 저장:
   - 종합: `archive/processed/persona-reviews/<YYYY-MM-DD>-<slug>.md`
   - raw: 같은 폴더의 `responses/<YYYY-MM-DD>-<slug>.jsonl`

## 출력 footer (필수)

```
출처: NVIDIA Nemotron-Personas-Korea (CC BY 4.0)
       https://huggingface.co/datasets/nvidia/Nemotron-Personas-Korea
면책: 본 리뷰의 페르소나 응답은 합성 데이터에 기반한 시뮬레이션이며,
       실존 시민의 견해를 대표하지 않습니다.
```
