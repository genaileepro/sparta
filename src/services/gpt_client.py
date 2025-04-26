"""
gpt_client.py

음식 이름 3개를 GPT-4o에 요청한 뒤
<지역 + 음식명> 조합으로 네이버 지도 검색 URL을 만들어 반환합니다.
"""

from __future__ import annotations

import os
import urllib.parse
from pprint import pprint
from typing import Dict, List

from openai import OpenAI


class GPTClient:
    """
    ▸ 필수 환경변수 : OPENAI_API_KEY  
    ▸ 사용 예시
        >>> client = GPTClient()
        >>> result = client.recommend({
        ...     "region":  "강남구 봉은사역",
        ...     "taste":   "매콤한",
        ...     "cuisine": "중식",
        ...     "cook":    "볶음",
        ...     "mood":    "혼밥"   # optional
        ... })
    """

    def __init__(self, api_key: str | None = None, model: str = "gpt-4o-mini") -> None:
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise RuntimeError("OPENAI_API_KEY 누락")
        self.model = model
        self.client = OpenAI(api_key=self.api_key)

    # ------------------------------------------------------------------ #
    def recommend(self, tokens: Dict[str, str]) -> Dict:
        """
        Parameters
        ----------
        tokens : dict
            {
                "region" : "강남구 봉은사역",
                "taste"  : "매콤한",
                "cuisine": "중식",
                "cook"   : "볶음",
                "mood"   : "혼밥"  # optional
            }

        Returns
        -------
        dict
            {
              "region": "...",
              "keywords": {...},
              "foods": [
                 {"food": "마라샹궈", "map_url": "..."},
                 ...
              ]
            }
        """
        foods = self._ask_gpt(tokens)
        if not foods:
            return {"error": "GPT 추천 실패"}

        results: List[Dict[str, str]] = []
        for food in foods:
            query = urllib.parse.quote_plus(f"{tokens['region']} {food}")
            map_url = f"https://map.naver.com/v5/search/{query}"
            results.append({"food": food, "map_url": map_url})

        return {
            "region": tokens["region"],
            "keywords": tokens,
            "foods": results,
        }

    # ------------------------------------------------------------------ #
    def _ask_gpt(self, t: Dict[str, str]) -> List[str]:
        """GPT-4o 호출 → 음식 이름 3개 리스트 반환"""
        system_msg = (
            "너는 한국의 맛집·음식 추천 전문가야. "
            "사용자의 조건에 맞는 음식 이름만 3줄로 추천해."
        )

        user_lines = [
            f"지역: {t['region']}",
            f"맛/질감: {t['taste']}",
            f"음식 장르: {t['cuisine']}",
            f"조리 방식: {t['cook']}",
        ]
        if t.get("mood"):
            user_lines.append(f"상황/분위기: {t['mood']}")
        user_lines.append("\n조건에 가장 어울리는 음식 세 가지를 음식 이름만 줄바꿈해서 알려줘.")

        try:
            resp = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_msg},
                    {"role": "user", "content": "\n".join(user_lines)},
                ],
                temperature=0.7,
            )
            answer = resp.choices[0].message.content.strip()
            return [line.strip() for line in answer.splitlines() if line.strip()]
        except Exception as exc:
            print(f"[GPT ERROR] {exc}")
            return []


# ---------------------------------------------------------------------- #
# CLI 테스트용 스크립트 실행
# ---------------------------------------------------------------------- #
if __name__ == "__main__":
    sample_tokens = {
        "region": "강남구 봉은사역",
        "taste": "매콤한",
        "cuisine": "중식",
        "cook": "볶음",
        "mood": "혼밥",
    }

    client = GPTClient()
    result = client.recommend(sample_tokens)
    print(result)
