# Harness 개선 (improve-harness)

누적 retrospective(`회고/*.md`)를 분석해 반복 패턴을 식별하고 사용자 답변에 따라 skill/agent/hook/참조문서를 갱신한다.

스킬 참조: [improve-harness](../../.agents/skills/improve-harness/SKILL.md)

## 입력

`$ARGUMENTS` — 분석할 retrospective 수(생략 시 전체).

## 절차

1. `회고/*.md`에서 반복 패턴 식별.
2. 사용자에게 구조화된 질문(최대 3건) 제시.
3. 답변에 따라:
   - skill stub 생성 또는 갱신
   - references 갱신
   - hook 추가 후보 제안
4. `AGENTS.md`는 직접 수정하지 않고 제안만 출력한다.

## 주의

- 사용자가 `/improve-harness`를 명시적으로 요청한 경우에만 실행한다.
- 자동 트리거 금지.
