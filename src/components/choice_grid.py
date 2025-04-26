import streamlit as st

def create_choice_grid(choices, cols=3, key_prefix="choice", on_click=None):
    """
    여러 선택지를 그리드 형태로 보여주는 컴포넌트
    
    Parameters:
    - choices: 선택지 목록 (리스트 또는 딕셔너리)
    - cols: 한 행에 표시할 열 수
    - key_prefix: 버튼 키의 접두사
    - on_click: 버튼 클릭 시 실행할 함수
    
    Returns:
    - 선택된 값 (없으면 None)
    """
    # 문자열만 처리하도록 간소화된 버전으로 변경
    # 열 생성
    columns = st.columns(cols)
    
    # 선택된 값 저장 변수
    selected_value = None
    
    # 각 선택지를 그리드에 배치
    for idx, choice in enumerate(choices):
        col_idx = idx % cols
        
        # 버튼 생성
        with columns[col_idx]:
            # 고유한 키 생성 - 항상 문자열로 변환
            unique_key = f"{key_prefix}_{idx}"
            
            try:
                if st.button(str(choice), key=unique_key, use_container_width=True):
                    selected_value = choice
                    if on_click:
                        on_click(selected_value)
            except Exception as e:
                st.error(f"버튼 생성 오류: {e}, 값: {choice}, 타입: {type(choice)}")
    
    return selected_value 