---
name: gokr-fetch
description: go.kr 도메인에서 자료를 받아 archive/raw에 저장하고 SHA-256과 인용 메타를 만든다.
---

# gokr-fetch

## 목적

`*.go.kr`, `*.or.kr` 도메인 자료를 우선 보존하고, 점진적으로 `*.kr` 및 지방정부·지방의회 공식 사이트까지 확장한다.

## 절차

1. 입력 URL을 분류한다: 1순위 `*.go.kr`/`*.or.kr`, 2순위 `*.kr`/지방정부·지방의회 공식 사이트, 그 외 도메인.
2. `archive_fetch(url, note?)` 호출 → `archive/raw/<host>/<basename>` 저장.
3. 동일 URL의 기존 해시와 비교해 **동일/변경/신규** 보고.
4. 파일명에는 수집 날짜를 붙이지 않고, 시간순 정렬은 `.meta.json`의 `collected_at`을 기준으로 한다.
5. `archive_cite(path)` 결과를 `archive/processed/<topic>/source.md`에 누적.

## 안전

- robots.txt 위반·rate limit 의심 시 즉시 중단.
- 자격증명·개인 식별 가능한 쿼리 파라미터는 URL에서 분리해 별도로 처리.
