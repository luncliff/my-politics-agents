---
name: review-feedback
description: retrospective 누적물을 분석해 반복 패턴을 식별하고, 사용자에게 구조화된 질문을 던진 뒤, 답변에 따라 skill/agent/hook/참조문서를 갱신.
---

# review-feedback

회고/ 에 누적된 회고를 읽고, 반복되는 패턴(막힌 것, 자동화 후보, 새 발견)을 식별한 뒤, 사용자의 판단을 받아 harness를 개선한다.

## 입력

- `$ARGUMENTS`: (선택) 분석할 retrospective 수. 생략 시 전체.

## 절차

### 1. 회고 수집

`회고/*.md`를 읽어 다음을 추출:
- `## 막힌 것` 항목 전체
- `## 자동화 후보` 항목 전체
- `## 새로 알게 된 사이트·포맷·정책` 항목 전체
- `## 성공한 것` 중 반복 성공 패턴

### 2. 패턴 식별

추출된 항목을 교차 비교하여:

| 패턴 유형 | 조건 | 제안 행동 |
|---|---|---|
| 반복 차단 | 같은 "막힌 것"이 2회 이상 | skill 또는 hook 생성 제안 |
| 미구현 자동화 후보 | "자동화 후보"에 등록 후 아직 구현 안 됨 | 우선순위 질문 |
| 반복 사이트 발견 | 같은 사이트가 2회 이상 "새로 알게 된" | 문서/ 기존 참조 문서 보강 제안 |
| 반복 성공 패턴 | 같은 접근법이 효과적으로 2회 이상 사용됨 | skill 규칙 강화 또는 AGENTS.md 규칙 후보 제시 |

### 3. 사용자 질문

식별된 패턴을 우선순위순으로 정리하고, 각각에 대해 구조화된 질문:
- "X가 N회 반복됩니다. 자동화할까요? [skill / hook / 보류]"
- "Y 사이트를 references에 추가할까요? [추가 / 보류]"
- "Z 규칙을 기존 스킬에 반영할까요? [반영 / 보류]"

한 번에 3개 이하의 질문만 던진다. 나머지는 다음 실행으로 이월.

### 4. 답변 기반 실행

사용자 답변에 따라:

| 답변 | 실행 |
|---|---|
| skill 생성 | `.agents/skills/<verb-noun>/SKILL.md` stub 작성 |
| hook 생성 | 대상 채널의 설정 파일에 hook 추가 (Claude: `.claude/settings.json`, Copilot: `.github/hooks/`) |
| references 추가 | `문서/` 기존 참조 문서에 항목 append |
| 스킬 규칙 강화 | 해당 `.agents/skills/<name>/SKILL.md`에 규칙 추가 |
| AGENTS.md 규칙 후보 | **직접 수정하지 않음** — 제안 텍스트를 출력하고 사용자가 별도 확인 후 반영 |
| 보류 | 기록만 남기고 다음 실행까지 이월 |

### 5. 실행 기록

처리 결과를 `.goals/feedback-log.md`에 append:

```markdown
## YYYY-MM-DD

- 패턴: <설명>
- 결정: <사용자 선택>
- 실행: <수행한 변경 요약>
```

## 제약

- AGENTS.md를 직접 수정하지 않는다. 제안만 출력.
- 생성하는 skill stub의 이름은 `verb-noun` 규칙을 따른다.
- 생성하는 agent stub의 이름은 역할 noun을 따른다.
- 채널별 설정 파일만 해당 채널 폴더에서 수정한다:
  - Claude Code: `.claude/`
  - GitHub Copilot: `.github/`
  - Codex CLI: `.codex/`
  - VS Code: `.vscode/`
- 한 번 실행에 최대 3건의 변경만 수행. 나머지는 이월.
- PII가 포함된 retrospective 내용은 feedback-log에 옮기지 않는다.

## 트리거 권장

SessionStart hook에서 미처리 retrospective 수를 세어, 3건 이상 누적 시 `/feedback` 실행을 배너에 표시.
