import streamlit as st
from src.utils.session_state import update_step, add_token, get_tokens
from src.components.choice_grid import create_choice_grid

def show():
    """맛/질감 선택 페이지 표시"""
    
    # 1단계: 맛 선택
    
    # 현재 선택된 토큰 표시
    tokens = get_tokens()
    st.info(f"선택한 지역: {tokens['region']}")
    
    st.header("지금 어떤 맛이 땡겨?")
    
    # 맛/질감 옵션 정의 (이모지 추가)
    taste_options = [
        "매콤한 🔥", "국물 있는 🍲", "바삭바삭 🍗", "새콤한 🍋",
        "달달한 🍯", "느끼한 🧈", "든든한 🍖", "시원한 🧊"
    ]
    
    # 선택 처리 함수 
    def on_taste_selected(selected_taste):
        # 이모지 제거하여 저장
        clean_taste = selected_taste.split(" ")[0]
        add_token("taste", clean_taste)
        update_step("select_cuisine")
    
    # 선택 그리드 생성
    create_choice_grid(
        taste_options, 
        cols=4,  # 4열로 변경하여 2x4 그리드 형태로 표시
        key_prefix="taste", 
        on_click=on_taste_selected
    )
    
    # 이전 단계로 돌아가는 버튼
    if st.button("← 이전 단계로", key="back_button"):
        update_step("home")
        st.rerun() 