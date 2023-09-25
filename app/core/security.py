# from .config import settings
# from .security import setup_security
import secrets

# # 애플리케이션 초기화
# def initialize_app():
#     # 보안 설정 초기화
#     setup_security(settings)

# # 애플리케이션 초기화 함수를 실행
# initialize_app()

SECRET_KEY = secrets.token_hex(32)
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30