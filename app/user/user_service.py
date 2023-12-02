from database.models import User, Auth
from passlib.context import CryptContext
from database.session import SessionLocal
from core.security import SECRET_KEY, ALGORITHM
from datetime import datetime, timedelta
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from core import security
from database.session import get_db
from jose import jwt
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
pwd_context = CryptContext(schemes=['bcrypt'], deprecated="auto")

def get_user_by_id(db: SessionLocal, id: int):
    return db.query(User).filter(User.id == id).first()

def create_user(db:SessionLocal ,auth_code : int , email : str, userID : str, password : str, nickname : str):
    new_user = User(id = auth_code ,email=email, userID=userID, password=password, nickname=nickname)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def get_user(db: SessionLocal, userID : str):
    return db.query(User).filter(User.userID == userID).first()

def hash_password(password):
    return pwd_context.hash(password)

def get_user_by_userID(db:SessionLocal, userID : str):
    return db.query(User).filter(User.userID == userID).first()

def get_user_by_auth_code(db:SessionLocal, auth_code : int):
    return db.query(User).filter(User.id == auth_code).first()

def get_user_by_email(db:SessionLocal, email : str):
    return db.query(User).filter(User.email == email).first()

def find_auth_code(db:SessionLocal, auth_code: int):
    return db.query(Auth).filter(Auth.id == auth_code).first()

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    return security.verify_token(token, db)