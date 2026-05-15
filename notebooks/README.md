# notebooks/

- 참고: <https://github.com/jacob-bd/notebooklm-mcp-cli>
- [shared-notebooks.json](shared-notebooks.json)에 등록된 공유 노트북 목록입니다.
  - 접근 상태 재확인: MCP 도구 `mcp_notebooklm_notebook_get`으로 각 `notebook_id`를 조회하거나, 인증 후 `nlm notebook list`로 목록에 포함 여부를 확인합니다.

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

## Troubleshooting

### `nlm login` 성공 후 `nlm notebook list` 인증 오류

#### 증상

`nlm login`이 성공(`✓ Successfully authenticated!`, 쿠키 96개 추출)했음에도
직후 `nlm notebook list` 및 MCP `mcp_notebooklm_notebook_list`가 아래 오류를 반환.

```
✗ Authentication Error
  Authentication expired. Run 'nlm login' in your terminal to re-authenticate.
```

`mcp_notebooklm_refresh_auth` 호출 후에도 동일 오류 지속.

#### 원인

`uvx`는 호출마다 독립 프로세스를 실행하므로 직전 `nlm login`으로 저장된 쿠키를
다음 `uvx` 호출에서 즉시 인식하지 못하는 세션 격리 현상으로 추정.
VS Code Task로 실행한 경우도 동일하게 재현됨 (exit code 1).

#### 해결

동일 셸 세션에서 `nlm login`과 `nlm notebook list`를 연속 실행:

```pwsh
uvx --from notebooklm-mcp-cli nlm login --force 2>&1
if ($LASTEXITCODE -eq 0) {
    uvx --from notebooklm-mcp-cli nlm notebook list 2>&1
}
```

`--force`: 이미 저장된 자격증명이 있어도 재인증 강제 적용.
재인증 후 MCP 서버도 자동으로 새 토큰을 로드함.

#### 확인된 동작

- `nlm doctor` 출력의 `Cookies: present`, `CSRF token: yes`는 **파일 존재 여부**만 확인하며 유효성을 보장하지 않음.
- `nlm login --check`도 파일이 있어도 세션 유효성이 없으면 오류를 반환함.
- 재인증 후 쿠키 수가 96개 → 113개로 증가하며 정상 조회 확인됨.
