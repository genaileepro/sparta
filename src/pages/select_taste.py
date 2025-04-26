import streamlit as st
from src.utils.session_state import update_step, add_token, get_tokens
from src.components.choice_grid import create_choice_grid

def show():
    """맛/질감 선택 페이지 표시"""
    
    # 현재 선택된 토큰 표시
    tokens = get_tokens()
    st.info(f"선택한 지역: {tokens['region']}")
    
    st.write("🌶️ 어떤 맛이나 식감을 원하시나요?")
    
    # 맛/질감 옵션 정의
    taste_options = [
        "매콤한", "달콤한", "짭짤한", "담백한", 
        "고소한", "시원한", "새콤한", "쫄깃한"
    ]
    
    # 선택 처리 함수 
    def on_taste_selected(selected_taste):
        add_token("taste", selected_taste)
        update_step("select_cuisine")
    
    # 선택 그리드 생성
    create_choice_grid(
        taste_options, 
        cols=3,
        key_prefix="taste", 
        on_click=on_taste_selected
    )
    
    # 이전 단계로 돌아가는 버튼
    if st.button("← 이전 단계로", key="back_button"):
        update_step("home")
        st.rerun() 