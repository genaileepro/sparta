import os
import sys
from dotenv import load_dotenv

# 환경 변수 로드
load_dotenv()

# 현재 파일의 부모 디렉토리를 Python 경로에 추가
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 세션 상태 초기화 함수를 직접 임포트
from src.utils.session_state import initialize_session_state

# 메인 앱 실행
from src.app import main

if __name__ == "__main__":
    # 세션 상태 초기화 명시적 호출
    initialize_session_state()
    # 메인 함수 실행
    main() 