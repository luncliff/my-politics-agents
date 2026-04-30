---
name: retrospective-writer
description: 세션 종료 시 retrospectives/YYYY-MM-DD-<slug>.md 작성.
---

# retrospective-writer

## 절차

1. 세션 동안의 시도/성공/실패를 한 줄씩 추출.
2. 새로 만난 사이트·포맷·정책을 정리.
3. 자동화 후보(skill / agent / task / hook)를 분류.
4. 출처·PII 점검 결과를 사실 그대로 기록(누락 N건 / 조치).
5. `retrospectives/YYYY-MM-DD-<slug>.md`로 저장.

## 템플릿

```markdown
---
date: YYYY-MM-DD
slug: <slug>
duration_min: <대략>
---

## 시도한 것
## 성공한 것
## 막힌 것 / 다음에 해결
## 새로 알게 된 사이트·포맷·정책
## 자동화 후보
- skill: ...
- agent: ...
- task: ...
- hook: ...
## 출처·PII 점검 결과
```

## 시간이 부족할 때

최소한 **"다음에 자동화할 후보"** 한 줄만이라도 남긴다.
