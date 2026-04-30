---
name: pdf-extract
description: PDF에서 본문·표·메타를 추출. opendataloader-pdf(JVM) 우선, 대안으로 pypdf.
applyTo: ["archive/raw/**/*.pdf"]
tools: ["filesystem"]
model: ""
---

# pdf-extract

## 목적

정부 공개 PDF(예산서·회의록·고시)에서 본문과 표를 정확히 뽑는다.

## 권장 도구

- [opendataloader-pdf](https://github.com/...) — JVM 11+, 표 정확도 우수
- 대안: `pypdf` + `pdfplumber` (가벼움, 표 처리 약함)

## 절차

1. `java -version`이 가능한지 확인. 가능하면 opendataloader-pdf 경로.
2. 출력은 페이지별 텍스트 + 표 JSON. Markdown으로 합치며 표는 GFM 표로 변환.
3. 페이지 번호와 원본 좌표를 주석으로 남겨 인용 추적 가능하게.
4. 결과는 `archive/processed/<topic>/<basename>.md`.

## 한계

- 스캔 PDF(이미지)는 OCR이 별도로 필요(이번 단계 미지원).
