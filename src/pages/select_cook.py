import streamlit as st
from src.utils.session_state import update_step, add_token, get_tokens
from src.components.choice_grid import create_choice_grid

def show():
    """조리방식 선택 페이지 표시"""
    
    # 4단계: 조리방식 선택
    
    # 현재 선택된 토큰 표시
    tokens = get_tokens()
    st.info(f"선택: {tokens['region']} → {tokens['taste']} → {tokens['cuisine']} → {tokens['mood']}")
    
    st.header("어떻게 조리된 음식이 좋을까요?")
    
    # 조리방식 옵션 정의 (이모지 추가 및 9개로 확장)
    cook_options = [
        ("매콤하게 볶음 🔥", "볶음"), 
        ("노릇하게 구이 🍖", "구이"), 
        ("바삭하게 튀김 🍗", "튀김"),
        ("부드럽게 찜 🥘", "찜"), 
        ("얼큰하게 탕/국 🍲", "탕/국"), 
        ("신선하게 생식 🥗", "생식"),
        ("담백하게 삶음 🍜", "삶음"), 
        ("든든하게 비빔 🍚", "비빔"), 
        ("아무거나 상관없음 🍽️", "상관없음")
    ]
    
    # 화면에 표시할 옵션만 추출
    display_options = [option[0] for option in cook_options]
    
    # 선택 처리 함수
    def on_cook_selected(selected_display):
        # 선택된 표시 텍스트에 해당하는 값 찾기
        for display, value in cook_options:
            if display == selected_display:
                add_token("cook", value)
                break
        update_step("result")
    
    # 선택 그리드 생성
    create_choice_grid(
        display_options, 
        cols=3, 
        key_prefix="cook", 
        on_click=on_cook_selected
    )
    
    # 이전 단계로 돌아가는 버튼
    if st.button("← 이전 단계로", key="back_button"):
        update_step("select_mood")
        st.rerun() 