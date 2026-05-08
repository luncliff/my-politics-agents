# data/

외부 데이터 git 저장소를 모아두는 위치입니다.

| 저장소 | 출처 | 비고 |
| --- | --- | --- |
| `legalize-kr/` | https://github.com/legalize-kr/legalize-kr | shallow clone (`git clone --depth 1`) |
| `precedent-kr/` | https://github.com/legalize-kr/precedent-kr | shallow clone (`git clone --depth 1`) |
| `admrule-kr/` | https://github.com/legalize-kr/admrule-kr | shallow clone (`git clone --depth 1`) |
| `ordinance-kr/` | https://github.com/legalize-kr/ordinance-kr | shallow clone (`git clone --depth 1`) |

처음 받을 때:

```
git clone https://github.com/luncliff/my-politics-agents.git
cd my-politics-agents
pwsh -ExecutionPolicy Bypass -File scripts/fetch_legalize_kr.ps1
```

이미 받은 저장소라면:

```
git -C data/legalize-kr pull --depth 1
git -C data/precedent-kr pull --depth 1
git -C data/admrule-kr pull --depth 1
git -C data/ordinance-kr pull --depth 1
```
