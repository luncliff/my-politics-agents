# scripts/

| 파일 | 용도 | 비고 |
| --- | --- | --- |
| `setup.ps1` / `setup.sh` | 환경 설정 (탐지→계획→동의→설치→검증) | `--DryRun` / `--dry-run` 지원 |
| `auth-purge.ps1` / `auth-purge.sh` | 자격증명·세션 정리 | 각 단계 동의 필요 |
| `lint_frontmatter.py` | agents/skills/prompts의 YAML frontmatter 검사 | CI에서도 사용 |
| `lib/common.{ps1,sh}` | 공용 헬퍼(로그·confirm·repo_root) | 직접 실행하지 않음 |

전역 변경(`npm i -g`, `winget install`, `brew install`)은 항상 사용자 동의를 요구합니다.
비대화 환경에서 자동 진행이 꼭 필요할 때만 `-Yes`/`--yes`를 쓰세요(권장하지 않음).
