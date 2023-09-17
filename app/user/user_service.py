from app.user.models import User
from app.database.session import SessionLocal

def generate_verification_code():
    # 여기에서 이메일 인증 코드를 생성하는 로직을 작성
    pass

def get_user_by_id(db: SessionLocal, user_id: int):
    return db.query(User).filter(User.id == user_id).first()
