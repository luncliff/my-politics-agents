# notebooks/

- [shared-notebooks.json](shared-notebooks.json)에 등록된 공유 노트북 목록입니다.
- [notebooklm-mcp-cli]: https://github.com/jacob-bd/notebooklm-mcp-cli

## MCP 서버

저장소는 mock publisher를 두지 않고 외부 NotebookLM CLI/MCP를 직접 사용합니다.

`.vscode/mcp.json` 설정 (서버 이름: `notebooklm`):

```json
{
  "type": "stdio",
  "command": "uvx",
  "args": ["--from", "notebooklm-mcp-cli", "notebooklm-mcp"]
}
```

- MCP 서버 바이너리: `notebooklm-mcp` (VS Code Copilot Chat 연동)
- CLI 바이너리: `nlm` (터미널 직접 사용)
  - `uvx --from notebooklm-mcp-cli nlm --help`
  - 최초 인증: `uvx --from notebooklm-mcp-cli nlm login`
  - VS Code Task: **civic: notebooklm login** / **civic: notebooklm doctor**

> 두 바이너리 모두 같은 패키지 `notebooklm-mcp-cli`에서 설치됩니다.
> `pyproject.toml` 의존성 불필요 — `uvx`가 실행 시 자동 설치합니다.

## 노트북 목록 조회 절차

NotebookLM에 접근하려면 Google 계정 인증이 필요합니다. 아래 순서로 진행합니다.

### 1단계: 인증 (`nlm login`)

```pwsh
uvx --from notebooklm-mcp-cli nlm login
```

또는 VS Code Task: **civic: notebooklm login**

- 브라우저가 열리면 Google 계정으로 로그인합니다.
- 인증 토큰이 로컬에 저장됩니다 (`~/.config/notebooklm-mcp-cli/` 또는 동등 경로).
- 계정을 전환할 때는 `nlm login switch <profile>`을 사용합니다.

### 2단계: 연결 확인 (`nlm doctor`)

```pwsh
uvx --from notebooklm-mcp-cli nlm doctor
```

또는 VS Code Task: **civic: notebooklm doctor**

- 인증 상태와 MCP 서버 연결을 진단합니다.

### 3단계: 노트북 목록 조회 (`nlm notebook list`)

```pwsh
uvx --from notebooklm-mcp-cli nlm notebook list
```

또는 VS Code Task: **civic: notebooklm notebook list**

- 인증된 Google 계정에서 접근 가능한 노트북 목록을 반환합니다.
- 출력된 `notebook_id`를 [shared-notebooks.json](shared-notebooks.json)에 등록해 관리합니다.

> 인증 오류 시: `nlm login`을 재실행하거나, MCP 서버에서 `mcp_notebooklm_refresh_auth` 도구를 호출합니다.

