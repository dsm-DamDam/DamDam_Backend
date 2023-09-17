from sqlalchemy import Column, Integer, String, Boolean
from app.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    is_verified = Column(Boolean, default=False)
    verification_code = Column(String, nullable=True)  # 이메일 인증을 위한 코드 저장

class Count(Base):
    __tablename__ = "counts"

    day = Column(String)
    cnt = Column(Integer)