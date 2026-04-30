---
description: 세션 종료 시 회고 작성
mode: agent
tools: ["filesystem"]
---

# 회고 작성 (session-retrospective)

목표: 이번 세션을 `retrospectives/YYYY-MM-DD-<slug>.md`로 남긴다.

## 입력

- `slug`: 회고 식별자 (선택, 기본: 주제 기반 자동 생성)

## 산출물 템플릿

```markdown
---
date: YYYY-MM-DD
slug: <slug>
duration_min: <대략>
---

## 시도한 것
- ...

## 성공한 것
- ...

## 막힌 것 / 다음에 해결
- ...

## 새로 알게 된 사이트·포맷·정책
- ...

## 자동화 후보
- skill: ...
- agent: ...
- task: ...
- hook: ...

## 출처·PII 점검 결과
- 누락 0건 / N건 (조치: ...)
```
