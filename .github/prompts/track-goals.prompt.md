---
description: "세션 목표를 선언하거나 기존 목표 진행 상태를 확인합니다."
---

# 세션 목표 추적

스킬 참조: [track-goals](../../.agents/skills/track-goals/SKILL.md)

## 사용법

```
@workspace /track-goals 성남시 조례안 비교분석 완료
```

인자 없이 호출하면 `.goals/current.md`의 현재 상태를 표시합니다.

## 동작

1. `.goals/current.md`를 읽거나 생성
2. 목표를 하위 단계로 분해 (agent/skill 매핑 포함)
3. 진행 상태를 체크리스트로 표시
