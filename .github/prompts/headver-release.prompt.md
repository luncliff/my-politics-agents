---
description: "로컬 maintainer 배포 시 HeadVer로 버전을 계산해 파일 버전을 갱신하고 commit, tag, push까지 수행합니다."
argument-hint: "<head> <build> [suffix] [commit message]"
tools: [execute, read, edit, search]
agent: agent
---

# HeadVer 배포

목표: 현재 로컬 환경에서 HeadVer 버전을 계산하고, 저장소의 패키지 버전을 동기화한 뒤 `commit -> git tag -> git push`를 안전하게 끝낸다.

## 입력

- `head` (필수): HeadVer의 첫 번째 숫자
- `build` (필수): HeadVer의 마지막 숫자
- `suffix` (선택): `+suffix` 메타 정보
- `commit message` (선택): 생략 시 `release: <version>` 사용

## 사용 예시

```text
@workspace /headver-release 0 12
@workspace /headver-release 1 3 rc.1
@workspace /headver-release 1 3 rc.1 "release: 1.2620.3+rc.1"
```

## 작업 규칙

1. 현재 branch, remote, worktree 상태를 먼저 확인한다.
2. 이번 배포와 무관한 변경이 있으면 자동 포함하지 말고, 어떤 파일이 막는지 짧게 설명하고 중단한다.
3. 버전 문자열은 반드시 [scripts/headver.ps1](../../scripts/headver.ps1)을 실행해서 계산한다. 직접 손으로 조합하지 않는다.
4. 계산된 버전은 아래 파일에 같은 값으로 반영한다.
   - [package.json](../../package.json)
   - [pyproject.toml](../../pyproject.toml)
   - [package-lock.json](../../package-lock.json) 이 있으면 top-level version도 함께 맞춘다.
5. 수정 후에는 값이 모두 같은지 다시 확인한다.
6. validation은 값 일치 확인과 touched file 범위의 `git diff --check`를 우선 사용한다.
7. `git add`는 이번 배포에 필요한 파일만 포함한다.
8. commit message가 없으면 `release: <version>`으로 commit 한다.
9. tag 이름은 계산된 HeadVer 문자열과 정확히 같아야 한다.
10. tag가 이미 있으면 덮어쓰지 말고 중단한다.
11. push는 force 없이 현재 branch와 새 tag만 원격에 올린다.
12. 성공 시 tag push가 GitHub prerelease workflow를 트리거한다는 점을 마지막에 짧게 알린다.

## 실행 순서

1. `git status --short --branch`로 상태 확인
2. `pwsh -NoProfile -File scripts/headver.ps1 -Head <head> -Build <build> [-Suffix <suffix>]` 실행
3. 버전 파일 2~3개 갱신
4. 버전 값 재검증
5. `git add <touched files>`
6. `git commit -m "release: <version>"` 또는 사용자 지정 메시지
7. `git tag -a <version> -m "release: <version>"`
8. `git push origin HEAD`
9. `git push origin <version>`

## 실패 처리

- worktree가 더럽고 포함 대상이 불명확하면 중단한다.
- 버전 파일 중 하나라도 갱신 실패면 commit 하지 않는다.
- commit 실패, tag 충돌, push 실패 시 현재 상태와 다음 수동 복구 지점만 짧게 보고한다.