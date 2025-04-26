import streamlit as st
from src.utils.session_state import update_step, add_token, get_tokens
from src.components.choice_grid import create_choice_grid

def show():
    """음식 장르 선택 페이지 표시"""
    
    # 2단계: 음식 장르 선택
    
    # 현재 선택된 토큰 표시
    tokens = get_tokens()
    st.info(f"선택: {tokens['region']} → {tokens['taste']}")
    
    st.header("어떤 음식이 당기나요?")
    
    # 🔥 음식 장르 후보
    situation_options = [
        ("한식 땡긴다 🇰🇷", "한식"),
        ("중식 땡긴다 🇨🇳", "중식"),
        ("양식 땡긴다 🍝", "양식"),
        ("일식 땡긴다 🍱", "일식"),
        ("아시안 요리 땡긴다 🥢", "아시안"),
        ("후루룩 면요리 🍜", "면요리"),
        ("가볍게 냠냠 🍱", "가벼운 식사"),
        ("술과 함께 🍻", "술안주"),
        ("달달하게 마무리 🍰", "디저트"),
        ("든든하게 배부르게 🍖", "든든한 식사")
    ]
    
    # 화면에 표시할 옵션만 추출
    display_options = [option[0] for option in situation_options]
    
    # 선택 처리 함수
    def on_cuisine_selected(selected_display):
        # 선택된 표시 텍스트에 해당하는 값 찾기
        for display, value in situation_options:
            if display == selected_display:
                add_token("cuisine", value)
                break
        update_step("select_mood")  # 다음 단계를 select_mood로 변경
    
    # 선택 그리드 생성
    create_choice_grid(
        display_options, 
        cols=3,
        key_prefix="cuisine", 
        on_click=on_cuisine_selected
    )
    
    # 이전 단계로 돌아가는 버튼
    if st.button("← 이전 단계로", key="back_button"):
        update_step("select_taste")
        st.rerun() 