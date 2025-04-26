import streamlit as st
import os
import sys

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
    
    # 디버깅: 세션 상태 정보 표시
    st.sidebar.write("디버깅 정보")
    st.sidebar.write(f"현재 단계: {st.session_state.get('current_step', '정보 없음')}")
    if 'tokens' in st.session_state:
        st.sidebar.write("토큰:", st.session_state['tokens'])
    
    # 현재 단계에 따라 해당 페이지 표시
    current_step = st.session_state["current_step"]
    st.sidebar.write(f"페이지 로딩 시도: {current_step}")
    
    if current_step == "home":
        st.sidebar.write("홈 페이지 로드 중...")
        home.show()
    elif current_step == "select_taste":
        st.sidebar.write("맛/질감 선택 페이지 로드 중...")
        from src.pages import select_taste
        select_taste.show()
    elif current_step == "select_cuisine":
        st.sidebar.write("음식 장르 선택 페이지 로드 중...")
        from src.pages import select_cuisine
        select_cuisine.show()
    elif current_step == "select_cook":
        st.sidebar.write("조리방식 선택 페이지 로드 중...")
        from src.pages import select_cook
        select_cook.show()
    elif current_step == "result":
        st.sidebar.write("결과 페이지 로드 중...")
        from src.pages import result
        result.show()
    else:
        st.error(f"알 수 없는 단계: {current_step}")

if __name__ == "__main__":
    main() 