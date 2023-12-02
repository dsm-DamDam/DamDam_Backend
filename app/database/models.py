from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship


Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True,autoincrement=True)
    userID = Column(String(20))
    email = Column(String(50), unique = True, index = True)
    nickname = Column(String(20))
    password = Column(String(30))

class Count(Base):
    __tablename__ = "counts"

    id = Column(Integer, primary_key=True, index=True,autoincrement=True)
    date = Column(Date)
    count = Column(Integer)


class Auth(Base):
    __tablename__ = "auths"

    id = Column(Integer, primary_key = True, index=True)


class Auth_user(Base):
    __tablename__ = "user_auths"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))  # 사용자의 ID를 참조하는 외래 키
    token = Column(String(255))  # 토큰 정보를 저장하는 필드