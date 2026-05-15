# 세션 목표 추적 (track-goals)

세션 목표를 선언하거나 기존 목표 진행 상태를 확인한다.

스킬 참조: [track-goals](../../.agents/skills/track-goals/SKILL.md)

## 입력

`$ARGUMENTS` — 새 목표 텍스트(선택). 생략하면 `.goals/current.md`의 현재 상태를 표시한다.

## 절차

1. `.goals/current.md`를 읽거나 신규 생성한다.
2. 목표를 하위 단계로 분해(가능한 경우 agent/skill 매핑 포함).
3. 진행 상태를 체크리스트로 표시한다.
4. 세션 종료 시 미완료 항목은 다음 세션 연결점으로 기록한다.
