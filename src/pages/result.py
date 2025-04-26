import streamlit as st
import os
from src.services.gpt_client import GPTClient
from src.utils.session_state import get_tokens

def show():
    st.title("🍽️ 먹깨비")
    st.caption("당신의 음식 취향을 클릭 몇 번으로 추천해드려요!")

    state = get_tokens()

    if not all(k in state for k in ("region", "taste", "cuisine", "cook")):
        st.error("모든 조건이 입력되지 않았습니다. 처음부터 다시 진행해 주세요.")
        return

    tokens = {
        "region": state["region"],
        "taste": state["taste"],
        "cuisine": state["cuisine"],
        "cook": state["cook"],
        "mood": state.get("mood", ""),
    }

    with st.spinner("추천 생성 중..."):
        try:
            client = GPTClient()
            result = client.recommend(tokens)
        except Exception as e:
            st.error(f"추천 생성 중 오류가 발생했습니다: {e}")
            return

    if "error" in result:
        st.error(result["error"])
        return

    # 추천 지역 출력
    st.subheader(f"📍 추천 지역: {result.get('region', '')}")
    st.info(f"선택: {tokens['region']} → {tokens['taste']} → {tokens['cuisine']} → {tokens['mood']} → {tokens['cook']}")

    foods = result.get("foods", [])
    if foods:
        st.subheader("🍴 추천 음식 리스트")

        emojis = ["🍛", "🍲", "🥘", "🍜", "🍣", "🍗", "🍖", "🍕", "🥗", "🌮"]

        left_items = []
        right_items = []

        # 음식 분리
        for idx in range(5):
            if idx < len(foods):
                food = foods[idx]
                food_name = food.get("food", "알 수 없음")
                map_url = food.get("map_url", "#")
                emoji = emojis[idx % len(emojis)]
                food_idx = idx + 1  # 번호 1부터

                html_block = f"""
                <p><b>{emoji} {food_idx}. {food_name}</b></p>
                <a href="{map_url}" target="_blank" style="display:inline-block; padding:6px 12px; margin:6px 0; background-color:#f0f2f6; border-radius:5px; text-decoration:none;">📍 지도에서 보기</a>
                <hr style="border:none; border-top:1px solid #eee;">
                """
                if idx < 3:
                    left_items.append(html_block)
                else:
                    right_items.append(html_block)
            else:
                # 빈칸 채우기
                if idx < 3:
                    left_items.append("<p>&nbsp;</p><hr style='border:none;'>")
                else:
                    right_items.append("<p>&nbsp;</p><hr style='border:none;'>")

        # 음식 테이블 출력
        html = f"""
        <table style="width:100%; border-collapse:collapse;">
            <tr>
                <td style="width:50%; border:none; vertical-align:top;">
                    {''.join(left_items)}
                </td>
                <td style="width:50%; border:none; vertical-align:top;">
                    {''.join(right_items)}
                </td>
            </tr>
        </table>
        """

        st.components.v1.html(html, height=350, scrolling=False)

    else:
        st.warning("추천된 음식이 없습니다.")

    st.write("---")

    # 🏠 홈으로 돌아가기 버튼
    if st.button("🏠 홈으로 돌아가기"):
        for key in ("region", "taste", "cuisine", "cook", "mood"):
            if key in state:
                del state[key]
        st.rerun()
        st.stop()

    # 🖼️ 홈으로 돌아가기 버튼 밑에 고정된 iframe 추가
    map_url = ""
    if foods and len(foods) > 0:
        map_url = foods[0].get("map_url", "https://map.naver.com/")
    
    iframe_html = f"""
    <iframe 
        src="{map_url}" 
        width="2500" 
        height="500"
        style="border:0px solid #ccc;">
    </iframe>
    """
    st.components.v1.html(iframe_html, height=510, scrolling=True)
