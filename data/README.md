# data/

외부 데이터 git submodule을 모아두는 위치입니다.

| 서브모듈 | 출처 | 비고 |
| --- | --- | --- |
| `legalize-kr/` | https://github.com/legalize-kr/legalize-kr | shallow clone (`.gitmodules`) |

처음 받을 때:

```
git clone --recurse-submodules https://github.com/luncliff/my-politics-agents.git
```

이미 받은 저장소라면:

```
git submodule update --init --recursive --depth 1
```
