---
name: hwp-to-text
description: HWP/HWPX 문서를 Markdown 텍스트로 변환 (rhwp 등 활용).
---

# hwp-to-text

## 목적

HWP/HWPX 문서를 사람이 읽기 좋은 Markdown으로 변환한다.

## 권장 도구

- [rhwp](https://github.com/rhwp/rhwp) — VS Code 확장 + WASM
- 대안: `hwp5proc` (Python, hwp5 바이너리 필요)

## 절차

1. 입력 파일 확장자 판별. HWPX는 우선 ZIP 해제 후 `Contents/section0.xml`을 파싱하는 경로 시도.
2. 변환 결과를 `archive/processed/<topic>/<basename>.md`로 저장.
3. 표·각주는 가능한 한 보존. 이미지·도형은 `assets/`로 분리하고 본문에 링크.
4. 변환 손실은 문서 끝 `## 변환 노트` 섹션에 명시.

## 한계

- 복잡한 표·페이지 레이아웃은 손실될 수 있음.
- 워터마크·서명 영역은 추출하지 않음.
