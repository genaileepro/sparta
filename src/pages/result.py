import streamlit as st
import os
from openai import OpenAI
from src.services.gpt_client import GPTClient
from src.utils.session_state import get_tokens

def generate_food_image(food_name):
    """OpenAI DALL-E API를 사용하여 음식 이미지를 생성합니다."""
    try:
        # proxies 매개변수 문제 해결을 위한 초기화 방식 변경
        try:
            # 환경 변수에서 프록시 설정을 제거
            http_proxy = os.environ.pop('HTTP_PROXY', None)
            https_proxy = os.environ.pop('HTTPS_PROXY', None)
            
            # 기본 매개변수만으로 클라이언트 초기화
            client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
            
            # 환경 변수 복원 (필요한 경우)
            if http_proxy:
                os.environ['HTTP_PROXY'] = http_proxy
            if https_proxy:
                os.environ['HTTPS_PROXY'] = https_proxy
        except Exception as e:
            print(f"OpenAI 클라이언트 초기화 중 오류: {e}")
            # 대체 초기화 방법 시도
            client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        
        # 이미지 생성 요청 (한국어 음식 이름에 "한국 음식"을 추가하여 더 정확한 결과 얻기)
        response = client.images.generate(
            model="dall-e-3",  # 또는 "dall-e-2"
            prompt=f"고품질 음식 사진: {food_name}, 한국 음식, 맛있는 음식 사진, 고해상도, 레스토랑 품질",
            size="1024x1024",
            quality="standard",
            n=1,
        )
        
        # 생성된 이미지 URL 반환
        return response.data[0].url
    except Exception as e:
        print(f"이미지 생성 중 오류: {e}")
        # 오류 발생 시 기본 이미지 반환
        return "https://recipe1.ezmember.co.kr/img/mobile/icon_food2.png"

def show():
    st.title("🍽️ 음식 추천 결과")

    state = get_tokens()

    if not all(k in state for k in ("region", "taste", "cuisine", "cook")):
        st.error("모든 조건이 입력되지 않았습니다. 처음부터 다시 진행해 주세요.")
        return

    tokens = {
        "region": state["region"],
        "taste": state["taste"],
        "cuisine": state["cuisine"],
        "cook": state["cook"],
        "mood": state.get("mood", ""),
    }

    with st.spinner("추천 생성 중..."):
        try:
            client = GPTClient()
            result = client.recommend(tokens)
        except Exception as e:
            st.error(f"추천 생성 중 오류가 발생했습니다: {e}")
            return

    if "error" in result:
        st.error(result["error"])
        return

    st.subheader(f"📍 추천 지역: {result.get('region', '')}")

    # 선택한 조건 표시
    st.info(f"선택: {tokens['region']} → {tokens['taste']} → {tokens['cuisine']} → {tokens['mood']} → {tokens['cook']}")

    foods = result.get("foods", [])
    if foods:
        st.markdown("### 🍴 추천 음식 리스트")
        
        # 음식 항목을 카드 형태로 표시
        cols = st.columns(3)  # 3개의 열로 표시
        
        # 각 음식에 대해 AI로 이미지 생성
        for i, food in enumerate(foods):
            food_name = food.get("food", "알 수 없음")
            map_url = food.get("map_url", "#")
            
            with cols[i % 3]:
                with st.spinner(f"{food_name} 이미지 생성 중..."):
                    img_url = generate_food_image(food_name)
                    st.image(img_url, caption=food_name, width=200)
                st.markdown(f"[{food_name} 지도에서 보기]({map_url})")
                st.write("---")
    else:
        st.warning("추천된 음식이 없습니다.")

    # 버튼 추가 (홈으로 돌아가기)
    if st.button("🏠 홈으로 돌아가기"):
        for key in ("region", "taste", "cuisine", "cook", "mood"):
            if key in state:
                del state[key]
        st.rerun()
