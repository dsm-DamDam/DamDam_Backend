from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship


Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True,autoincrement=True)

    userID = Column(String(20), unique = True, index=True)
    email = Column(String(50), unique=True, index=True)
    nickname = Column(String(10))
    password = Column(String(30))
    #counts = relationship("Count", back_populates="user")
    #is_verified = Column(Boolean, default=False)
    #verification_code = Column(String, nullable=True)
    
class Count(Base):
    __tablename__ = "counts"

    id = Column(Integer, primary_key=True, index=True,autoincrement=True)
    #userID = Column(Integer, ForeignKey("users.id"))
    date = Column(Date)
    count = Column(Integer)

    #user = relationship("User", back_populates="counts")


class Auth(Base):
    __tablename__ = "auths"

    id = Column(Integer, primary_key = True, index=True)