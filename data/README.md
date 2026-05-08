# data/

외부 데이터 git 저장소를 모아두는 위치입니다.

| 저장소 | 출처 | 비고 |
| --- | --- | --- |
| `legalize-kr/` | https://github.com/legalize-kr/legalize-kr | shallow clone (`git clone --depth 1`) |

처음 받을 때:

```
git clone https://github.com/luncliff/my-politics-agents.git
cd my-politics-agents
git clone --depth 1 https://github.com/legalize-kr/legalize-kr.git data/legalize-kr
```

이미 받은 저장소라면:

```
git -C data/legalize-kr pull --depth 1
```
