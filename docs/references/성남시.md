# 성남시 참고자료

문서 갱신일: 2026-05-01

이 문서는 성남시·판교 생활권 조사에 직접 쓰는 성남시 단위 참고자료만 모아 둔 카탈로그입니다.

## 1. 자치법규·의회

- [행정안전부 자치법규정보시스템](https://www.elis.go.kr/alrpop/locgovAlrPopup?ctpvCd=41&sggCd=130): 성남시 자치법규 목록, 공포번호, 시행일, 개정이력 확인의 1차 진입점
- [성남시의회 의안검색](https://www.sncouncil.go.kr/kr/bill/bill.do): 최신 조례안·규칙안·결의안의 발의/처리 상태 확인 진입점
- [국가법령정보센터](https://www.law.go.kr/자치법규/성남시도시계획조례): 최종 정리된 조례 본문과 연계 법령 확인용
- [성남시청](https://www.seongnam.go.kr/main.do): 자치법규 및 시정정보 진입점
- [성남시의회](https://www.sncouncil.go.kr/): 자치입법 및 의정정보 진입점
- [성남시의회](https://www.sncouncil.go.kr/kr/assembly/cmsRecordCategory.do): 회의록 분류 및 열람 진입점
- [성남시의회](https://www.sncouncil.go.kr/kr/assembly/committee.do): 상임위원회 및 회의기록 진입점
- [성남시의회](https://sncouncil.go.kr/kr/bill/bill.do?sTh=9&session=309&startDay=20220701&endDay=20260630&x=61&y=7): 제9대 의안 검색 예시로 조례안·결의안·청원·예산안의 발의자, 소관위, 처리결과 확인

## 2. 성남시 최신 조례 수집 절차

성남시 조례의 최신 목록은 행정 부서 체계가 아니라 **공포·의안·최종본문**의 3단계로 수집합니다.

1. **ELIS로 최신 목록 확인**
	- 성남시 자치법규 목록을 먼저 조회해 현재 유효한 조례와 개정이력을 확인합니다.
	- 조례명, 공포번호, 시행일, 소관부서를 우선 추출합니다.
2. **성남시의회로 최신 입법 동향 확인**
	- 의안검색에서 조례안/규칙안의 발의자, 소관위원회, 처리결과를 확인합니다.
	- ELIS에 아직 반영되지 않은 최근 제정·개정안은 여기서 먼저 잡습니다.
3. **law.go.kr로 최종 본문 검증**
	- 조례 본문과 연계 법령을 확인해 최종 정리본을 검증합니다.
	- 본문이 길거나 개정 이력이 복잡한 경우 law.go.kr의 조문 구조를 기준으로 대조합니다.
4. **원문 보존 후 Markdown 변환**
	- 원문 HTML/PDF는 `archive/raw/`에 그대로 보존합니다.
	- Markdown 본문 상단에는 HTML 주석으로 메타데이터를 둡니다.
5. **주제별(Semantic) 재분류**
	- 조례 제목과 제1조 목적을 기준으로 아래 카테고리 중 하나를 선택합니다.
	- 행정 부서명은 보조 메타데이터로만 남기고, 저장 구조는 주제별 폴더를 우선합니다.

## 3. Semantic 분류 기준

다음 6개 카테고리 중 하나만 선택합니다.

- `일반행정`: 시정 운영, 조직, 인사, 재정, 자산
- `보건복지`: 복지 서비스, 보건소, 노인·아동·장애인 지원
- `교통안전`: 도로, 교통망, 재난·안전, 소방, 보행
- `산업경제`: 지역경제, 일자리, 기업 지원, 상업, 농업
- `도시환경`: 도시계획, 주택, 환경 보호, 공원, 청소
- `교육문화`: 교육 지원, 도서관, 예술, 관광, 체육

분류가 애매하면 제목보다 제1조 목적을 우선하고, 그래도 모호하면 사용자 확인 후 저장합니다.

## 4. 저장 규칙

- 파일명은 `성남시-{조례명}.md` 형식을 따릅니다.
- 파일명에서 특수문자, 괄호, 따옴표는 제거하거나 공백으로 치환합니다.
- 본문 원문은 토씨 하나 바꾸지 않고 보존합니다.
- 메타데이터 주석에는 최소한 `시행일`, `소관부서`, `공포번호`, `원본 URL`, `수집 시각`, `sha256`을 둡니다.
- 개정 이력이 있으면 기존 파일을 덮어쓰지 않고 `개정 이력`에 누적합니다.

## 5. 통계·재정

- [성남통계 사이트맵](https://www.seongnam.go.kr/stat/1001729/11152/contents.do): 분야별통계, 최신통계, 통계보고서, 통계DB 진입점
- [KOSIS 통계조회 및 다운로드](https://stat.kosis.kr/nsieu/view/tree.do?task=branchView&id=612_61201*MT_OTITLE&hOrg=612): 경기도 성남시 통계연보 항목별 조회
- [성남시청](https://www.seongnam.go.kr/city/1000170/20189/program.do): 재정공시, 예산, 결산, 기금운용현황 진입점
- [성남시청](https://www.seongnam.go.kr/city/1000170/339/11608/subTabCont.do): 2026년 세입세출예산서, 특별회계, 성인지 예산
- [성남시청](https://www.seongnam.go.kr/city/1000172/10099/contents.do): 결산의 의의, 관련 법규, 결산 업무 처리순기
- [성남시청](https://www.seongnam.go.kr/city/1000179/30030/bbsList.do): 기금운용계획 및 성과분석보고서
- [성남시 정책기획과 빅데이터팀](https://www.seongnam.go.kr/stat/1001694/11142/contents.do): 성남의 재정

## 6. 연구·공개자료

- [성남시청](https://www.seongnam.go.kr/city/1002229/30501/bbsList.do): 성남시 맞춤형 정책연구 개요와 연도별 과제 목록
- [성남시청](https://www.seongnam.go.kr/city/1000201/30217/bbsList.do?post_size=50): 부서별 계획, 연구, 현황 자료
- [성남시청](https://www.seongnam.go.kr/city/1000201/30217/bbsList.do?post_size=50): 예산집행, 채무관리계획 등 부서별 공개자료
- [성남시정연구원](https://www.snri.re.kr/web/contents/SNRI40100000.do): 연구성과 및 연구보고서 목록

## 7. 교통·도시기반

- [성남시청](https://www.seongnam.go.kr/publicOrder/publicOrderList.do?menuIdx=1000631): 공공발주사업 설계내역서·도급내역서 공개
- [성남시 정책기획과 빅데이터팀](https://www.seongnam.go.kr/stat/1001698/11146/contents.do): 성남의 자동차
- [성남시 정책기획과 빅데이터팀](https://www.seongnam.go.kr/stat/1001695/11143/contents.do): 성남의 주택
- [성남시 정책기획과 빅데이터팀](https://www.seongnam.go.kr/stat/newStat/newStat.do?menuIdx=1001708&p_category_idx=4): 지역경제

## 8. 청년·교육·복지

- [성남시](https://youth.seongnam.go.kr/): 성남시 청년포털
- [성남시청 청년청소년과](https://www.seongnam.go.kr/city/1000201/30217/bbsList.do?post_size=50): 청년정책 시행계획 등 부서별 공개자료
- [성남시 정책기획과 빅데이터팀](https://www.seongnam.go.kr/stat/1001700/11148/contents.do): 성남의 교육
- [성남시 정책기획과 빅데이터팀](https://www.seongnam.go.kr/stat/1001701/11149/contents.do): 성남의 보건사회

## 9. 공식 포털 진입점

- [성남시청](https://www.seongnam.go.kr/main.do): 성남시 메인 포털
- [성남시청](https://www.seongnam.go.kr/city/1000193/20045/program.do): 사전 정보공표
- [성남시청](https://www.seongnam.go.kr/city/1000515/10418/contents.do): 정보공개제도 안내
- [성남시청](https://www.seongnam.go.kr/city/1000202/10111/contents.do): 공공데이터 개방 안내

## 10. 사용 메모

- 성남시청, 성남시의회, 성남통계, 성남시정연구원 같이 시 단위 원문을 찾을 때 이 문서를 먼저 사용합니다.
- 경기도 상위 기관이나 광역 의정자료는 `docs/references-경기도.md`를 먼저 봅니다.
- 성남시 공개데이터셋 세부 활용 판단은 `docs/references-seongnam-open-data.md`를 함께 봅니다.