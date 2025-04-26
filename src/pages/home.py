import streamlit as st
from src.utils.session_state import update_step, add_token, get_tokens

def show():
    """홈 페이지 표시 (지역 입력)"""
    
    st.write("🌏 어느 지역에서 음식을 찾고 계신가요?")
    
    # 지역 입력 필드
    region = st.text_input(
        "지역명을 입력하세요 (예: 강남구 봉은사역, 서울역 주변, 종로구 등)",
        placeholder="지역명 입력...",
        key="region_input"
    )
    
    # 다음 단계로 이동하는 버튼
    if st.button("위치설정 완료", use_container_width=True, type="primary"):
        if not region:
            st.error("지역을 입력해주세요!")
            return
        
        # 지역 정보 저장
        add_token("region", region)
        
        # 다음 단계로 이동
        update_step("select_taste")
        st.rerun()
    
    # 앱 소개 (접을 수 있는 영역)
    with st.expander("🔍 먹깨비란?"):
        st.markdown("""
        **먹깨비**는 당신의 음식 취향을 몇 번의 클릭으로 파악하여 맞춤형 음식과 식당을 추천해 드립니다.

        **사용 방법**
        1. 지역 입력 (현재 단계)
        2. 원하는 맛/질감 선택
        3. 음식 장르 선택
        4. 조리방식 선택
        5. 추천 결과 확인
        
        GPT를 활용해 당신의 취향에 꼭 맞는 맛집을 찾아드립니다!
        """) 