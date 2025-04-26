import streamlit as st

def initialize_session_state():
    """
    세션 상태 초기화 함수
    - current_step: 현재 단계
    - tokens: 사용자가 선택한 키워드 모음
    """
    # 현재 단계 초기화 (처음 시작 = 'home')
    if "current_step" not in st.session_state:
        st.session_state["current_step"] = "home"
        print(f"세션 상태 초기화: current_step = 'home'")
    
    # 토큰(키워드) 저장소 초기화
    if "tokens" not in st.session_state:
        st.session_state["tokens"] = {
            "region": "",
            "taste": "",
            "cuisine": "",
            "cook": ""
        }
        print("토큰 저장소 초기화 완료")

def update_step(step_name):
    """
    현재 단계를 업데이트하는 함수
    """
    old_step = st.session_state.get("current_step", "없음")
    st.session_state["current_step"] = step_name
    print(f"단계 업데이트: {old_step} -> {step_name}")
    # 디버깅용: 세션 상태가 실제로 변경되었는지 확인
    print(f"업데이트 후 세션 상태: {st.session_state.get('current_step', '정보 없음')}")

def add_token(key, value):
    """
    토큰(키워드)을 추가하는 함수
    """
    old_value = st.session_state["tokens"].get(key, "없음")
    st.session_state["tokens"][key] = value
    print(f"토큰 추가: {key} = {old_value} -> {value}")

def reset_tokens():
    """
    모든 토큰(키워드)을 초기화하는 함수
    """
    st.session_state["tokens"] = {
        "region": "",
        "taste": "",
        "cuisine": "",
        "cook": ""
    }
    print("모든 토큰 초기화 완료")
    
def get_tokens():
    """
    현재 선택된 모든 토큰(키워드)을 반환하는 함수
    """
    return st.session_state["tokens"] 