import streamlit as st
from src.utils.session_state import update_step, add_token, get_tokens
from src.components.choice_grid import create_choice_grid

def show():
    """음식 장르 선택 페이지 표시"""
    
    # 현재 선택된 토큰 표시
    tokens = get_tokens()
    st.info(f"선택: {tokens['region']} → {tokens['taste']}")
    
    st.write("🍲 어떤 종류의 음식을 드시고 싶으신가요?")
    
    # 음식 장르 옵션 정의
    cuisine_options = [
        "한식", "중식", "일식", "양식",
        "분식", "아시안", "멕시칸", "패스트푸드"
    ]
    
    # 선택 처리 함수
    def on_cuisine_selected(selected_cuisine):
        add_token("cuisine", selected_cuisine)
        update_step("select_cook")
    
    # 선택 그리드 생성
    create_choice_grid(
        cuisine_options, 
        cols=3,  # 3x3 그리드로 변경
        key_prefix="cuisine", 
        on_click=on_cuisine_selected
    )
    
    # 이전 단계로 돌아가는 버튼
    if st.button("← 이전 단계로", key="back_button"):
        update_step("select_taste")
        st.rerun() 