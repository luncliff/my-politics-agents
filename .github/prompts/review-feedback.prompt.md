---
description: "누적 retrospective를 분석해 harness 개선 제안을 생성합니다."
---

# 피드백 리뷰 및 Harness 개선

스킬 참조: [review-feedback](../../.agents/skills/review-feedback/SKILL.md)

## 사용법

```
@workspace /review-feedback
@workspace /review-feedback 3
```

인자는 분석할 retrospective 수 (생략 시 전체).

## 동작

1. `retrospectives/*.md`에서 반복 패턴 식별
2. 사용자에게 구조화된 질문 (최대 3건)
3. 답변에 따라 skill stub 생성, references 갱신, hook 추가
4. AGENTS.md는 직접 수정하지 않고 제안만 출력
