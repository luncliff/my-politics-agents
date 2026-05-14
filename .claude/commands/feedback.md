# Retrospective 기반 피드백 및 Harness 개선

누적된 retrospective를 분석하여 반복 패턴을 식별하고, 사용자 판단을 받아 skill/hook/참조문서를 갱신한다.

## 입력

- `$ARGUMENTS`: (선택) 분석할 retrospective 수. 생략 시 전체.

## 절차

1. 스킬 [review-feedback](../../.agents/skills/review-feedback/SKILL.md)를 따른다.
2. `retrospectives/*.md`를 읽어 패턴을 식별한다.
3. 식별된 패턴에 대해 사용자에게 구조화된 질문을 던진다.
4. 답변에 따라 harness 변경을 실행한다.
5. 실행 결과를 `.goals/feedback-log.md`에 기록한다.

## 출력

- 식별된 패턴 요약 (표)
- 사용자 질문 (최대 3건)
- 실행된 변경 요약
