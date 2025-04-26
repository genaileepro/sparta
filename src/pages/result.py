import streamlit as st
import time
from src.utils.session_state import update_step, get_tokens, reset_tokens
from src.services.gpt_client import GPTClient

def show():
    """결과 페이지 표시 (GPT 기반 추천)"""
    
    # 현재 선택된 토큰 표시
    tokens = get_tokens()
    st.info(f"선택: {tokens['region']} → {tokens['taste']} → {tokens['cuisine']} → {tokens['cook']}")
    
    # 추천 결과 캐싱 상태 확인
    if "recommendation_result" not in st.session_state:
        with st.spinner("맛있는 음식을 찾고 있어요..."):
            # GPT 클라이언트 생성
            gpt_client = GPTClient()
            
            # 결과 생성 (시간 측정)
            start_time = time.time()
            result = gpt_client.generate_recommendation(tokens)
            elapsed_time = time.time() - start_time
            
            # 결과 저장
            st.session_state["recommendation_result"] = result
            st.session_state["recommendation_time"] = elapsed_time
    
    # 결과 표시
    result = st.session_state["recommendation_result"]
    elapsed_time = st.session_state.get("recommendation_time", 0)
    
    # 타이틀
    st.header("🍽️ 추천 결과")
    
    # 생성 시간 표시
    st.caption(f"생성 시간: {elapsed_time:.2f}초")
    
    # 추천 텍스트 표시
    st.markdown(result["text"])
    
    # 액션 버튼들
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("새로운 추천 받기", use_container_width=True):
            # 토큰 초기화 후 첫 페이지로
            reset_tokens()
            # 추천 결과 제거
            if "recommendation_result" in st.session_state:
                del st.session_state["recommendation_result"]
            if "recommendation_time" in st.session_state:
                del st.session_state["recommendation_time"]
            update_step("home")
            st.rerun()
    
    with col2:
        if st.button("다른 조리방식으로 변경", use_container_width=True):
            # 조리방식 선택 페이지로 돌아가기
            # 추천 결과 제거
            if "recommendation_result" in st.session_state:
                del st.session_state["recommendation_result"]
            if "recommendation_time" in st.session_state:
                del st.session_state["recommendation_time"]
            update_step("select_cook")
            st.rerun() 