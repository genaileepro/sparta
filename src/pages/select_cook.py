import streamlit as st
from src.utils.session_state import update_step, add_token, get_tokens
from src.components.choice_grid import create_choice_grid

def show():
    """조리방식 선택 페이지 표시"""
    
    # 현재 선택된 토큰 표시
    tokens = get_tokens()
    st.info(f"선택: {tokens['region']} → {tokens['taste']} → {tokens['cuisine']}")
    
    st.write("🍳 어떤 조리방식의 음식을 원하시나요?")
    
    # 조리방식 옵션 정의
    cook_options = [
        "볶음", "구이", "튀김", "찜",
        "탕/국", "생식", "삶음"
    ]
    
    # 선택 처리 함수
    def on_cook_selected(selected_cook):
        add_token("cook", selected_cook)
        update_step("result")
    
    # 선택 그리드 생성
    create_choice_grid(
        cook_options, 
        cols=3, 
        key_prefix="cook", 
        on_click=on_cook_selected
    )
    
    # 이전 단계로 돌아가는 버튼
    if st.button("← 이전 단계로", key="back_button"):
        update_step("select_cuisine")
        st.rerun() 