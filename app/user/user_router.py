from fastapi import APIRouter, Depends, HTTPException, Path
from sqlalchemy.orm import Session
from app.database.session import get_db
from .schemas import UserCreate, UserLogin
from app.user import user_service, schemas

router = APIRouter()

@router.post("/send-verification-email", response_model=schemas.VerificationResponse)
async def send_verification_email(
    user_id: int = Path(..., title="사용자 ID"),
    db: Session = Depends(get_db)
):
    user = user_service.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="사용자를 찾을 수 없습니다.")

    # 이메일 인증 코드 생성 및 이메일 전송 (send_email_verification 함수는 실제로 작성되어야 함)
    verification_code = user_service.generate_verification_code()
    user.verification_code = verification_code
    db.commit()

    # send_email_verification 함수로 이메일 전송

    return {"message": "이메일 인증 코드가 전송되었습니다."}

@router.post("/email", response_model=schemas.VerificationResponse)
async def verify_email(
    user_id: int = Path(..., title="사용자 ID"),
    verification_request: schemas.VerificationRequest = None,  # 선택적으로 만듦
    db: Session = Depends(get_db)
):
    user = user_service.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="사용자를 찾을 수 없습니다.")

    if user.is_verified:
        raise HTTPException(status_code=400, detail="이미 인증된 이메일 주소입니다.")

    if user.verification_code == verification_request.verification_code:
        user.is_verified = True
        user.verification_code = None  # 코드 사용 후 삭제
        db.commit()
        return {"message": "이메일이 성공적으로 인증되었습니다."}
    else:
        raise HTTPException(status_code=400, detail="유효하지 않은 인증 코드입니다.")


@router.post("/sign")
async def register_user(user_data: schemas.UserCreate, db: Session = Depends(get_db)):
    # 비밀번호 확인
    if user_data.password != user_data.confirm_password:
        raise HTTPException(status_code=400, detail="비밀번호가 일치하지 않습니다.")
    
    # 이메일 중복 확인
    if user_service.get_user_by_email(db, user_data.email):
        raise HTTPException(status_code=400, detail="이미 등록된 이메일 주소입니다.")
    
    # 아이디 중복 확인
    if user_service.get_user_by_username(db, user_data.username):
        raise HTTPException(status_code=400, detail="이미 사용 중인 아이디입니다.")
    
    # 비밀번호 해싱 (보안을 위해 실제로는 bcrypt 또는 다른 해싱 알고리즘 사용을 권장)
    hashed_password = user_service.hash_password(user_data.password)
    
    # 사용자 등록
    new_user = user_service.create_user(db, user_data.email, user_data.username, hashed_password, user_data.nickname)
    
    # 이메일 인증 코드 생성 및 이메일 전송 (이 부분은 이메일 전송 로직으로 대체해야 함)
    verification_code = user_service.generate_verification_code()
    new_user.verification_code = verification_code
    db.commit()
    
    # 이메일 전송 로직 호출 (실제로는 이메일 전송 서비스를 사용해야 함)
    #send_email_verification(new_user.email, verification_code)
    
    return new_user

@router.post("/login")
def login_user(user: UserLogin, db: Session = Depends(get_db)):

    # 사용자 인증 및 로그인 처리
    user_in_db = db.execute("SELECT * FROM users WHERE username = ? AND password = ?", user.username, user.password).fetchone()
    if not user_in_db:
        raise HTTPException(status_code=401, detail="로그인 실패: 잘못된 사용자 이름 또는 비밀번호")

    return {"message": "로그인이 성공적으로 완료되었습니다."}
