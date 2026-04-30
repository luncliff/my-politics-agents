---
name: gokr-fetch
description: go.kr 도메인에서 자료를 받아 archive/raw에 저장하고 SHA-256과 인용 메타를 만든다.
---

# gokr-fetch

## 목적

`*.go.kr`(또는 정부 공인 도메인) 자료를 표준 형식으로 받아 보존한다.

## 절차

1. 입력 URL이 정부 도메인인지 확인. 아니면 사용자에게 명시 동의 요청.
2. `archive_fetch(url, note?)` 호출 → `archive/raw/<host>/<YYYY-MM-DD>/<basename>` 저장.
3. 동일 URL의 기존 해시와 비교해 **동일/변경/신규** 보고.
4. `archive_cite(path)` 결과를 `archive/processed/<topic>/source.md`에 누적.

## 안전

- robots.txt 위반·rate limit 의심 시 즉시 중단.
- 자격증명·개인 식별 가능한 쿼리 파라미터는 URL에서 분리해 별도로 처리.
