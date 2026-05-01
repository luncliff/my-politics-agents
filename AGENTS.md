# AGENTS.md — 에이전트 공통 행동 규약

이 문서는 **GitHub Copilot CLI**와 **VS Code Copilot Chat**에서 동일하게 적용되는
이 저장소의 행동 규약입니다. 모든 custom agent / skill / prompt 파일은 이 문서를 따릅니다.

> 더 좁은 범위(파일·폴더)의 규칙이 있으면 그것이 우선합니다.
> `applyTo` 패턴이 일치하는 `.instructions.md`, 그 다음 `agents/`, 마지막으로 이 파일.

## 1. 미션

대한민국 지방정치 현장에서 **신뢰 가능한 정보 흐름**을 만든다.
수집(collect) → 정제(process) → 출판(publish) 모든 단계에서 **출처가 항상 따라다니게** 한다.

## 2. 핵심 원칙

### 2.1 워크스페이스 로컬 우선

- 모든 설정·자격증명·캐시는 이 저장소 폴더 안에 둔다.
- 시스템 전역 변경(`npm i -g`, `git config --global`, `~/.copilot/*` 수정 등)은 **반드시 사용자에게 묻고** 진행한다.
- `~/.aws`, `~/.ssh`, OS 키체인 접근은 금지. 필요하면 사용자가 직접 처리하도록 안내한다.

### 2.2 출처(Citation) 의무

- 외부 데이터를 다루는 모든 산출물에는 **원본 URL · 수집 일시 · SHA-256 해시**를 footer에 포함한다.
- `archive/raw/<host>/<filename>.<ext>`에 원본을 보존한다(재현성).
- 파일명에 날짜를 강제하지 않고, 시간순 추적은 같은 경로의 `.meta.json`에 기록된 `collected_at`을 기준으로 한다.
- `gov-archive` MCP의 `archive_cite` 도구를 사용해 인용 메타를 생성한다.

### 2.3 PII·개인정보

- 회의록·민원서 등에서 사람 이름·전화번호·주민번호·이메일은 `pii-mask` 스킬을 **반드시 통과**시킨 뒤 저장·게시한다.
- 마스킹된 원본 키는 디스크에 남기지 않는다.

### 2.4 정치적 중립

- 정당·후보·특정 인물에 대한 산출물은 **사실 카드(Facts)**와 **해석(Interpretation)**을 분리해 작성한다.
- 추측·주관 표현을 사실 카드에 섞지 않는다.

### 2.5 안전한 자동화

- `Bypass Approvals`, `Autopilot`, `/yolo`, `chat.tools.global.autoApprove`는 사용하지 않는다.
- 새 도구·도메인은 **명시 동의** 후 자동 승인 목록에 추가한다.
- 파괴적 명령(`rm -rf`, `git push --force`, `mkfs`, `dd`, `curl|bash`)은 항상 사람의 확인이 필요하다.

## 3. 작업 흐름

### 3.1 세션 시작

1. Copilot CLI hooks가 정책 배너를 출력한다.
2. 작업 의도를 한 줄로 요약하고, 영향을 받을 디렉터리를 명시한다.
3. 위험·범위·예상 산출물을 사용자에게 확인받는다.

### 3.2 세션 진행

- 새로운 사이트/포맷을 만나면 먼저 `archive_fetch`로 원본을 보존한 뒤 처리한다.
- 같은 작업을 두 번 이상 하게 되면 **스킬 후보**로 분류해 회고에 기록한다.
- 도메인 특화 페르소나가 두 번 이상 등장하면 **에이전트 후보**로 분류한다.

### 3.3 세션 종료 — 회고 의무

`retrospective-writer` 스킬을 호출해 다음 내용을 `retrospectives/YYYY-MM-DD-<slug>.md`로 저장한다.

- 무엇을 시도했는가 / 무엇이 성공했는가 / 무엇이 막혔는가
- 새로 알게 된 사이트·포맷·정책
- 다음 번에 자동화할 후보(skill / agent / task / hook)
- 누락된 출처·PII가 있었다면 즉시 수정

## 4. 산출물 형식

### 4.1 정제 문서 (Markdown)

```markdown
---
title: "<문서 제목>"
source_url: "<원본 URL>"
collected_at: "<ISO-8601>"
content_sha256: "<해시>"
license: "공공누리 1유형"   # 또는 해당 라이선스
pii_masked: true
# <제목>

본문 …

---
출처: <원본 URL> · 수집 <ISO-8601> · sha256:<짧은해시>
```

### 4.2 NotebookLM 업로드 매니페스트

`notebooks/<slug>/manifest.yml` — 스펙은 [docs/reference/manifest-schema.md](docs/reference/manifest-schema.md) 참조.

### 4.3 회고

`retrospectives/YYYY-MM-DD-<slug>.md` — `retrospective-writer` 스킬이 템플릿 제공.

## 5. 도구 사용 우선순위

1. **워크스페이스 로컬 MCP 서버** (`mcp-servers/*`) — 출처·해시·로깅이 통일됨
2. **Skill에 정의된 명령** — 안전 가드 통과
3. **VS Code 내장 도구**(`#fetch`, `#problems`, `#codebase` 등)
4. **터미널** — `chat.tools.terminal.autoApprove`에 등록된 패턴만 무인 실행

128 tool 한도에 닿으면 `Tool Sets`(`.vscode/toolsets.jsonc`)로 묶어 호출한다.

## 6. 금지 사항

- `archive/raw/`의 파일을 임의로 수정·삭제 (불변 보존)
- 자격증명·토큰을 채팅·로그·커밋 메시지·산출물에 포함
- robots.txt 위반, rate-limit 무시
- 출처 없이 단정적 진술

## 7. 참고

- [.github/copilot-instructions.md](.github/copilot-instructions.md) — VS Code Chat 특이사항
- [docs/governance.md](docs/governance.md) — 데이터·라이선스·윤리 상세
- [docs/security.md](docs/security.md) — 보안 모델·자격증명 정리
- [docs/architecture.md](docs/architecture.md) — 시스템 개요
