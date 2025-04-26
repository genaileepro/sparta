🍽 먹깨비 — 기능 명세서 + 최종 플로우차트 (통합본)

1. 기능 명세서 (요약)

구분 핵심 내용
목표 지역·맛·장르·조리방식을 3-4 클릭으로 입력 → GPT API에 단어를 묶어 질의 → 메뉴 + 식당 이름/주소 즉시 추천
주요 사용자 흐름 0) 지역 입력 → 1) 맛/질감 선택 → 2) 음식 장르 선택 → 3) 조리방식 선택 → 🔘 추천받기 → 결과 카드/테이블
Frontend Streamlit v1.33
∙ st.session*state 로 키워드 누적
∙ 3×3 / 4×2 버튼 그리드 컴포넌트
Backend OpenAI GPT-4/4o (ChatCompletion)
∙ 프롬프트 자동 생성 모듈
∙ 결과 파싱 → 표/카드 렌더
핵심 파일 app.py(엔트리) ∙ pages/0~5*\*.py ∙ components/choice_grid.py ∙ services/gpt_client.py
상태 관리 st.session_state["tokens"] = {region, taste, cuisine, cook}
에러 처리 입력 검증·재시도·API 오류 시 Toast 알림
확장 로드맵 리뷰 크롤링 → Lottie 애니 → 즐겨찾기 저장(DB) → A/B 테스트 2. 최종 플로우차트
2-1. 사용자·데이터 흐름
(Mermaid 코드 — 복사해 Live Editor/Notion 등에서 렌더링 가능)

mermaid
복사
편집
flowchart TD
subgraph UI["📱 사용자 화면"]
A0[0. 지역 입력<br>(텍스트)] --> A1[1. 맛/질감 선택<br>(8 버튼)]
A1 --> A2[2. 음식 장르 선택<br>(8 버튼)]
A2 --> A3[3. 조리방식 선택<br>(6-8 버튼)]
A3 --> BTN[🔘 추천받기]
end

    subgraph APP["🖥 Streamlit App"]
        BTN --> S1[키워드 누적<br>region+taste+cuisine+cook]
        S1 --> GPT[GPT API 요청]
        GPT --> S2[응답 파싱<br>(메뉴·식당·주소)]
        S2 --> RES[결과 카드/표 렌더]
    end

2-2. 디렉터리 구조(확장 버전)
mermaid
복사
편집
flowchart TB
ROOT["meokkaebi/"] --> SRC(src/)
SRC --> APP[app.py]
SRC --> PAGES(pages/)
SRC --> COMP(components/)
SRC --> SERV(services/)
SRC --> UTIL(utils/)
ROOT --> CFG[Dockerfile & requirements.txt]

    PAGES --> P1[01_home.py]
    PAGES --> P2[.._select_taste.py]
    PAGES --> P3[.._select_cuisine.py]
    PAGES --> P4[.._select_cook.py]
    PAGES --> P5[05_result.py]

    COMP --> CG(choice_grid.py)
    COMP --> HD(header.py)

    SERV --> GCLI(gpt_client.py)
    SERV --> ALOG(analytics.py)

    UTIL --> PB(prompt_builder.py)

(초기 MVP는 main.py + 3~4 파일만으로 시작 → 위 구조로 점진 확장)

3. GPT 프롬프트 빌드 예시
   python
   복사
   편집
   def build_prompt(tokens: dict) -> str:
   """
   tokens = {
   'region': '강남구 봉은사역',
   'taste': '매콤한',
   'cuisine': '중식',
   'cook': '볶음'
   }
   """
   return (f"{tokens['region']} 근처에서 {tokens['taste']} {tokens['cuisine']} "
   f"{tokens['cook']} 요리를 판매하는 식당 3곳을 추천해줘. "
   "식당 이름과 주소를 표 형식으로 알려줘.")
   ✅ 한 눈 정리
   Streamlit

단계별 버튼 UI + 세션 상태 저장

GPT 호출

지역·맛·장르·조리법 4 키워드 → 자연어 프롬프트 → 결과 파싱

결과 표시

메뉴 제안 + 식당/주소, 다시 고르기 버튼

코드/폴더

MVP → 확장 구조까지 트리·플로우 완비 🚀

이 문서 하나면 기획·개발·협업 전 과정의 공통 레퍼런스로 활용할 수 있습니다.
