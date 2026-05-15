# Prompt·Agent·Tool 종합 진단

저장소의 prompt, agent definition, skill, MCP 설정, 문서 조직을 교차 점검하여 불일치·누락·중복을 보고한다.

## 입력

- `$ARGUMENTS`: (선택) 점검 범위. `all` | `agents` | `skills` | `tools` | `docs`. 기본: `all`.

## 절차

1. 스킬 [diagnose-prompts](../../.agents/skills/diagnose-prompts/SKILL.md)를 따른다.
2. 점검 대상 파일을 모두 읽는다.
3. 6개 카테고리별 점검을 수행한다.
4. 결과를 요약 표 + 상세 목록으로 출력한다.

## 출력

- 요약 표 (통과/경고/오류 건수)
- 오류 목록 (즉시 수정 필요)
- 경고 목록 (검토 권장)
- 제안 목록 (선택적 개선)

## 참고

- 읽기 전용. 파일을 수정하지 않는다.
- AGENTS.md 변경이 필요한 경우 제안 텍스트만 출력한다.
