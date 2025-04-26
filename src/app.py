import streamlit as st
import os
import sys
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()

# 현재 파일의 경로를 기준으로 상위 디렉토리를 파이썬 경로에 추가
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.pages import home
from src.utils.session_state import initialize_session_state

# 페이지 설정
st.set_page_config(
    page_title="먹깨비 - 맛있는 음식 추천",
    page_icon="🍽️",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# 세션 상태 초기화
initialize_session_state()

# 메인 페이지 로드
def main():
    # 상단 타이틀
    st.title("🍽️ 먹깨비")
    st.subheader("당신의 음식 취향을 클릭 몇 번으로 추천해드려요!")
    
    # 현재 단계에 따라 해당 페이지 표시
    current_step = st.session_state["current_step"]
    
    if current_step == "home":
        home.show()
    elif current_step == "select_taste":
        from src.pages import select_taste
        select_taste.show()
    elif current_step == "select_cuisine":
        from src.pages import select_cuisine
        select_cuisine.show()
    elif current_step == "select_mood":
        from src.pages import select_mood
        select_mood.show()
    elif current_step == "select_cook":
        from src.pages import select_cook
        select_cook.show()
    elif current_step == "result":
        from src.pages import result
        result.show()
    else:
        st.error(f"알 수 없는 단계: {current_step}")

if __name__ == "__main__":
    main() 