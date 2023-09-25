from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database.session import get_db
from user import user_service, schemas
from database.models import User
from .schemas import SignUp, Login, updatePW
from datetime import datetime, timedelta
from core.security import SECRET_KEY, ACCESS_TOKEN_EXPIRE_MINUTES, ALGORITHM
from jose import jwt
import re

router = APIRouter()


@router.post("/sign")
async def signup(user: SignUp, db: Session = Depends(get_db)):
    # 비밀번호 형식 확인
    Regex_Password = r'^(?=.*\d)(?=.*[!@#$%^&*()]).{8,30}$'
    if not(re.fullmatch(Regex_Password, user.password)):
        raise HTTPException(status_code=400, detail="비밀번호 형식이 잘못됐습니다.")
    # 비밀번호 중복 확인
    if user.password != user.confirm_password:
        raise HTTPException(status_code=400, detail="비밀번호가 일치하지 않습니다.")
    # 제품코드 존재 여부 확인
    if user_service.find_auth_code(db, user.auth_code):
        raise HTTPException(status_code=400, detail="존재하지 않은 제품코드입니다.")
    # 제품코드 중복 확인
    if user_service.get_user_by_auth_code(db, user.auth_code):
        raise HTTPException(status_code=400, detail="이미 등록한 제품코드입니다.")
    # 아이디 중복 확인
    if user_service.get_user_by_userID(db, user.userID):
        raise HTTPException(status_code=400, detail= "이미 사용 중인 아이디입니다.")
    # 사용자 등록
    user_service.create_user(db,user.auth_code , user.email, user.userID, user.password, user.nickname)
    return {"detail":"회원가입이 성공적으로 완료되었습니다"}

@router.post("/login", response_model=schemas.Token)
def login(user: Login, db: Session = Depends(get_db)):
    # 사용자 인증 및 로그인 처리
    user_in_db = db.query(User).filter(User.userID == user.userID, User.password == user.password).first()
    if not user_in_db:
        raise HTTPException(status_code=401, detail="로그인 실패: 잘못된 사용자 이름 또는 비밀번호")
    
    user_data = user_service.get_user(db, user.userID)

    data = {
        "sub": user_data.id,
        "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    }
    access_token = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)
    return {"access_token": access_token,"token_type": "bearer","username": user_data.id}, {"detail": "로그인이 성공적으로 완료되었습니다."}


@router.delete("/logout")
async def logout():
    return {"detail": "로그아웃 되었습니다."}

@router.patch("/updatePW/")
async def change_password(updatePW: updatePW, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == updatePW.id).first()
    if not user:
        raise HTTPException(status_code=404, detail="유저를 찾을 수 없습니다.")
    # 이전 비밀번호가 일치하는지 확인
    if not user.password == updatePW.password:
        raise HTTPException(status_code=400, detail="이전 비밀번호가 일치하지 않습니다.")
    # 비밀번호 일치
    if updatePW.change_password != updatePW.confirm_change_password:
        raise HTTPException(status_code=400, detail="비밀번호가 일치하지 않습니다.")
    # 새로운 비밀번호를 설정
    user.password = updatePW.change_password
    # 변경된 비밀번호를 데이터베이스에 저장
    db.commit()
    return {"detail": "비밀번호가 성공적으로 변경되었습니다."}

@router.patch("/updateInfo")
async def update_user(user_data: schemas.updateInfo, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_data.id).first()
    if not user:
        raise HTTPException(status_code=404, detail="유저를 찾을 수 없습니다.")
    if user.password == user_data.password:
        if user_data.new_userID.strip(): 
            user.userID = user_data.new_userID
        if user_data.new_nickname.strip():
            user.nickname = user_data.new_nickname
        if user_data.new_email.strip():
            user.email = user_data.new_email
    else:
        raise HTTPException(status_code=400, detail="비밀번호가 일치하지 않습니다.")
    db.commit()
    return {"detail": "회원정보가 성공적으로 변경되었습니다."}


@router.get("/{id}", response_model=schemas.User)
async def get_user(id: int, db: Session = Depends(get_db)):
    user = user_service.get_user_by_id(db, id)  # user_service 모듈을 사용하여 함수 호출
    if not user:
        raise HTTPException(status_code=404, detail="사용자를 찾을 수 없습니다.")
    return user