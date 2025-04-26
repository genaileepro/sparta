# 🍽️ 먹깨비

먹깨비는 사용자의 음식 취향을 클릭 몇 번으로 파악하여 맞춤형 음식과 식당을 추천해주는 Streamlit 애플리케이션입니다.

## 기능

-   지역 입력
-   맛/질감 선택 (8가지 옵션)
-   음식 장르 선택 (8가지 옵션)
-   조리방식 선택 (7가지 옵션)
-   GPT 기반 개인화된 음식 및 식당 추천

## 설치 방법

1. 저장소 클론

```bash
git clone https://github.com/yourusername/meokkaebi.git
cd meokkaebi
```

2. 필요한 패키지 설치

```bash
pip install -r requirements.txt
```

3. `.env` 파일 생성 및 API 키 설정

```
OPENAI_API_KEY=your_openai_api_key_here
```

## 사용 방법

1. Streamlit 앱 실행

```bash
streamlit run main.py
```

2. 웹 브라우저에서 앱 접속 (기본: http://localhost:8501)

3. 단계별로 선택하여 맞춤형 추천 받기:
    - 지역 입력
    - 맛/질감 선택
    - 음식 장르 선택
    - 조리방식 선택
    - 추천 결과 확인

## 디렉토리 구조

```
meokkaebi/
├── main.py                  # 메인 실행 파일
├── requirements.txt         # 필요한 패키지 목록
├── README.md                # 이 파일
├── src/
│   ├── app.py               # Streamlit 앱 진입점
│   ├── pages/               # 페이지별 모듈
│   │   ├── home.py          # 홈 페이지 (지역 입력)
│   │   ├── select_taste.py  # 맛/질감 선택 페이지
│   │   ├── select_cuisine.py# 음식 장르 선택 페이지
│   │   ├── select_cook.py   # 조리방식 선택 페이지
│   │   └── result.py        # 결과 페이지
│   ├── components/          # 재사용 가능한 컴포넌트
│   │   └── choice_grid.py   # 선택 그리드 컴포넌트
│   ├── services/            # 서비스 모듈
│   │   └── gpt_client.py    # GPT API 클라이언트
│   └── utils/               # 유틸리티 함수
│       └── session_state.py # 세션 상태 관리
```

## 사용된 기술

-   Streamlit v1.33
-   OpenAI API (GPT-4/4o)
-   Python 3.9+

## 향후 계획

-   리뷰 크롤링 기능 추가
-   Lottie 애니메이션 추가
-   즐겨찾기 저장 기능
-   A/B 테스트
