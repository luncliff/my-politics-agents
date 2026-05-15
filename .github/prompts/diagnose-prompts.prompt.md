---
description: "저장소 전체의 prompt, agent, tool 설정을 종합 점검하여 불일치를 보고합니다."
model: GPT-5.4 (copilot)
---

# Prompt·Agent·Tool 종합 진단

스킬 참조: [diagnose-prompts](../../.agents/skills/diagnose-prompts/SKILL.md)

## 사용법

```
@workspace /diagnose-prompts
@workspace /diagnose-prompts agents
```

인자: `all` | `agents` | `skills` | `tools` | `docs` (기본: `all`)

## 동작

1. 점검 대상 파일을 모두 읽기
2. Naming, Agent 정합성, Skill 참조, Tool/MCP, 문서 조직, Output 규칙 점검
3. 요약 표 + 오류/경고/제안 출력
4. 읽기 전용 — 파일 수정 없음
