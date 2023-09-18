from pydantic import BaseModel, validator, constr
from fastapi import HTTPException, status
import re

class VerificationRequest(BaseModel):
    email: constr()
    verification_code: constr()

class User(BaseModel):
    id: constr()
    nickname: constr()
    email: constr()
    password: constr()

    class Config:
        orm_mode = True

class SignUp(BaseModel):
    nickname: constr()
    email: constr()
    account_id: constr()
    password: constr()
    confirm_password: constr()

    @validator('password')
    def check_password(cls, v):
        REGEX_PASSWORD = r'^(?=.*[\d])(?=.*[A-Z])(?=.*[a-z])(?=.*[!@#$%^&*()])[\w\d!@#$%^&*()]{8,24}$'
        if not re.fullmatch(REGEX_PASSWORD, v):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="비밀번호 형식이 잘못됨")
        return v

class Login(BaseModel):
    account_id: constr()
    password: constr()

    @validator('password')
    def check_password(cls, v):
        REGEX_PASSWORD = r'^(?=.*[\d])(?=.*[A-Z])(?=.*[a-z])(?=.*[!@#$%^&*()])[\w\d!@#$%^&*()]{8,24}$'
        if not re.fullmatch(REGEX_PASSWORD, v):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="비밀번호 형식이 잘못됨")
        return v