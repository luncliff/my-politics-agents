# persona-perspective-review · 산출물 템플릿

```markdown
---
title: "<대상 문서 제목> — 시민 페르소나 패널 검토"
target_path: "<원문 경로 또는 URL>"
panel: "<national|local|both>"
panel_size: <N>
seed: <정수>
generated_at: "<ISO-8601>"
dataset: "nvidia/Nemotron-Personas-Korea"
license: "CC BY 4.0"
synthetic: true
---

# 1. 평가 대상 요지

- 한 줄 요약:
- 핵심 변경/주장 3가지:

# 2. 패널 구성

| 구분 | 인원 | 비고 |
| --- | --- | --- |
| 전국(stratified) | … | sido × sex × age_bucket |
| 지역(<sigungu>) | … | location.txt 기반 |

연령대·성별·시도 분포 표(요약):

| 연령대 | M | F | 계 |
| --- | --- | --- | --- |
| 19-29 | … | … | … |
| 30-39 | … | … | … |
| … | | | |

# 3. 시점별 응답 요약

각 페르소나 응답 raw는 `responses/<같은-slug>.jsonl` 참조.

## 3.1 클러스터별 주요 반응

- **20·30대 수도권 사무직**:
- **40·50대 비수도권 자영업**:
- **60대+ 단독가구**:
- **<지역> 거주 부모(자녀 동거)**:

## 3.2 공통 우려 Top 3

1.
2.
3.

## 3.3 공통 지지 Top 3

1.
2.
3.

# 4. 분포

| 입장 | 인원 | 비율 |
| --- | --- | --- |
| 지지 | | |
| 중립 | | |
| 반대 | | |

# 5. 누락된 관점

- 19세 미만 청소년 (데이터셋 제외)
- 외국인 거주민 (데이터셋 제외)
- (그 외 도메인별 누락 식별):

# 6. 정치적 중립 점검

- 특정 정당·후보 옹호 표현 검출: (없음/있음 — 인용)
- 차별·혐오 표현 검출: (없음/있음 — 인용)
- 조치: (재생성/응답 제거/면책 강화)

# 7. 다음 단계 제안 (객관 사실 기반)

- 추가 확인 필요한 사실:
- 보완 패널(예: 청년만 N명, 농촌 시·군 N명):

---
출처: NVIDIA Nemotron-Personas-Korea (CC BY 4.0) · <https://huggingface.co/datasets/nvidia/Nemotron-Personas-Korea>
패널: <panel> · 시드: <seed> · 추출 <YYYY-MM-DDTHH:MM:SSZ>
면책: 본 리뷰의 페르소나 응답은 합성 데이터에 기반한 시뮬레이션이며,
       실존 시민의 견해를 대표하지 않습니다.
```
