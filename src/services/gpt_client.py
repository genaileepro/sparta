import os
import streamlit as st
from openai import OpenAI

class GPTClient:
    def __init__(self):
        # OpenAI API 키 설정
        self.api_key = os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            st.error("OpenAI API 키가 설정되지 않았습니다. '.env' 파일을 확인하세요.")
        
        # OpenAI 클라이언트 초기화
        self.client = OpenAI(api_key=self.api_key)
    
    def generate_recommendation(self, tokens):
        """
        사용자 선택 키워드(토큰)를 기반으로 음식과 식당 추천 생성
        
        Parameters:
        - tokens: 키워드 딕셔너리 (region, taste, cuisine, cook)
        
        Returns:
        - 음식 및 식당 추천 정보 딕셔너리
        """
        try:
            # 프롬프트 생성
            prompt = self._build_prompt(tokens)
            
            # GPT API 호출
            response = self.client.chat.completions.create(
                model="gpt-4o",  # 또는 "gpt-4"
                messages=[
                    {"role": "system", "content": "당신은 맛집 추천 전문가입니다. 사용자의 선호에 맞는 음식과 식당을 추천해주세요."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=800
            )
            
            # 응답 텍스트 추출
            recommendation_text = response.choices[0].message.content
            
            # 파싱 (단순화를 위해 텍스트 그대로 반환)
            return {
                "text": recommendation_text,
                "raw_response": response
            }
            
        except Exception as e:
            st.error(f"GPT API 호출 중 오류가 발생했습니다: {str(e)}")
            return {
                "text": "추천을 생성하는 중 오류가 발생했습니다. 다시 시도해주세요.",
                "error": str(e)
            }
    
    def _build_prompt(self, tokens):
        """
        토큰을 기반으로 프롬프트 생성
        """
        return (f"{tokens['region']} 근처에서 {tokens['taste']} {tokens['cuisine']} "
                f"{tokens['cook']} 요리를 판매하는 식당 3곳을 추천해줘. "
                "각 식당의 추천 메뉴와 주소를 함께 알려주고, 왜 이 식당을 추천하는지 짧게 설명해줘.") 