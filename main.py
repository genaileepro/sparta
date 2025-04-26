import os
import sys
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()

# 필요한 환경 변수 확인
if not os.getenv("OPENAI_API_KEY"):
    print("경고: OPENAI_API_KEY가 설정되지 않았습니다.")
    print("OpenAI API 키를 환경 변수로 설정하거나 .env 파일에 추가해주세요.")
    print("예시: OPENAI_API_KEY=your_api_key_here")

# src 디렉토리를 파이썬 경로에 추가
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Streamlit 앱 실행
if __name__ == "__main__":
    print("먹깨비 애플리케이션을 시작합니다...")
    print("아래 명령어로 앱을 실행하세요:")
    print("streamlit run main.py")
    
    # streamlit 명령어로 앱을 직접 실행하는 대신, 사용자에게 안내만 제공합니다.
    # 이렇게 하면 사용자가 streamlit run 명령어로 앱을 실행할 수 있습니다.
    
    # Streamlit 앱 연결
    import src.app 