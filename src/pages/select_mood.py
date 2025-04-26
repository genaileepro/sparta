import streamlit as st
from src.utils.session_state import update_step, add_token, get_tokens
from src.components.choice_grid import create_choice_grid

def show():
    """상황/분위기 선택 페이지 표시"""
    
    # 3단계: 상황/분위기 선택
    
    # 현재 선택된 토큰 표시
    tokens = get_tokens()
    st.info(f"선택: {tokens['region']} → {tokens['taste']} → {tokens['cuisine']}")
    
    st.header("어떤 상황에서 드실건가요?")
    
    # 🔥 상황/분위기 옵션 (수정됨: 12개 옵션)
    mood_options = [
        ("혼밥하기 좋은 🧍", "혼밥"),
        ("데이트하기 좋은 💑", "데이트"),
        ("회식하기 좋은 👥", "회식"),
        ("가족 식사하기 좋은 👨‍👩‍👧‍👦", "가족"),
        ("친구와 함께 👫", "친구"),
        ("술과 함께 🍶", "술안주"),
        ("인스타 감성 📱", "인스타"),
        ("가성비 좋은 💰", "가성비"),
        ("건강에 좋은 🥗", "건강"),
        ("시간 없을 때 ⏱️", "빠른식사"),
        ("배달/포장 좋은 📦", "배달포장"),
        ("아무 상황이나 괜찮아요 ✨", "상관없음")
    ]
    
    # 화면에 표시할 옵션만 추출
    display_options = [option[0] for option in mood_options]
    
    # 선택 처리 함수
    def on_mood_selected(selected_display):
        # 선택된 표시 텍스트에 해당하는 값 찾기
        for display, value in mood_options:
            if display == selected_display:
                add_token("mood", value)
                break
        update_step("select_cook")
    
    # 선택 그리드 생성
    create_choice_grid(
        display_options, 
        cols=3, 
        key_prefix="mood", 
        on_click=on_mood_selected
    )
    
    # 이전 단계로 돌아가는 버튼
    if st.button("← 이전 단계로", key="back_button"):
        update_step("select_cuisine")
        st.rerun() 