---
name: notebooklm-sync
description: notebooks/<slug>/manifest.yml을 NotebookLM에 동기화 (외부 MCP 위임).
applyTo: ["notebooks/**"]
tools: ["filesystem"]
model: ""
---

# notebooklm-sync

## 절차

1. `notebooks/<slug>/manifest.yml` 로드 + 검증
   - 모든 `sources[].path` 존재 확인
   - `sources[].citation`이 정제본 frontmatter `source_url`과 일치하는지 확인
   - 불일치 시 동기화 중단 + 사용자에게 차이 표시
2. 외부 MCP(예: `notebooklm-mcp`)가 등록돼 있는지 확인. 없으면 안내만 출력.
3. 등록돼 있다면 변경분만 업로드(해시 비교).
4. 결과(`notebook_id`, 업로드/스킵 카운트)를 manifest에 다시 기록.
5. 회고에 한 줄 추가 후보를 남긴다.

## 안전

- `visibility: public` 전환은 사용자 명시 동의 후에만.
- 자격증명은 환경변수 / 외부 MCP 설정에 위임. 본 스킬은 토큰을 다루지 않음.
