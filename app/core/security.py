from .config import settings
import secrets
from database.session import get_db
from sqlalchemy.orm import Session
from jose import jwt, JWTError
from database.models import User
from fastapi import Depends, HTTPException, status

SECRET_KEY = secrets.token_hex(32)
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def verify_token(token: str, db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="토큰이 유효하지 않습니다.",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id : str = payload.get("sub")
        print(user_id)
        if user_id is None:
            raise credentials_exception
    except JWTError as e:
        print(f"JWT decode error: {e}")
        raise credentials_exception
    
    user = db.query(User).filter(User.id == int(user_id)).first()
    print(user)
    if user is None:
        raise credentials_exception

    return user