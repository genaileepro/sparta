# 먹깨비 (Meokkaebi)

맛집 추천 AI 서비스 - 당신의 취향을 분석해 딱 맞는 음식을 추천해 드립니다!

## 배포 방법

### Streamlit Cloud 배포

1. [Streamlit Cloud](https://streamlit.io/cloud)에 가입하고 로그인합니다.
2. "New app" 버튼을 클릭합니다.
3. GitHub 저장소와 브랜치를 선택합니다.
4. 메인 파일로 `app.py`를 지정합니다.
5. "Advanced settings"에서 다음 환경 변수를 설정합니다:
    - `OPENAI_API_KEY`: OpenAI API 키

### 로컬 실행 방법

1. 저장소를 클론합니다:

    ```
    git clone [저장소 URL]
    cd [프로젝트 폴더]
    ```

2. 가상 환경을 생성하고 활성화합니다:

    ```
    python -m venv venv
    source venv/bin/activate  # Windows: venv\Scripts\activate
    ```

3. 의존성을 설치합니다:

    ```
    pip install -r requirements.txt
    ```

4. `.env` 파일을 생성하고 다음 환경 변수를 설정합니다:

    ```
    OPENAI_API_KEY=your_openai_api_key
    ```

5. 애플리케이션을 실행합니다:
    ```
    streamlit run app.py
    ```

## 기능

-   지역 입력
-   맛/질감 선택 (8가지 옵션)
-   음식 장르 선택 (8가지 옵션)
-   조리방식 선택 (7가지 옵션)
-   GPT 기반 개인화된 음식 및 식당 추천

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
