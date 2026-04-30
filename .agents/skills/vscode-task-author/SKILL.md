---
name: vscode-task-author
description: 새 워크플로를 .vscode/tasks.json의 Task로 추가하는 작업.
applyTo: [".vscode/tasks.json"]
tools: ["filesystem"]
model: ""
---

# vscode-task-author

## 목적

자주 반복되는 명령은 채팅 명령 대신 **VS Code Task**로 노출한다.

## 절차

1. 새 Task의 목적·입력·출력을 한 줄씩 정리.
2. `windows`/`linux`/`osx` 분기 명령을 모두 작성.
3. 라벨 prefix는 `civic:`로 통일.
4. `presentation`/`problemMatcher`를 명시(없으면 빈 배열).
5. README와 `docs/for-non-developers.md`의 Task 표에 한 줄 추가.

## 안전

- 파괴적 명령(`rm -rf`, `git push --force`)은 Task로 만들지 않는다.
- 자격증명을 인자로 받는 Task는 만들지 않는다(환경변수 사용).
