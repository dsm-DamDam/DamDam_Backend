from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    #is_verified = Column(Boolean, default=False)
    #verification_code = Column(String, nullable=True)

class Count(Base):
    __tablename__ = "counts"

    id = Column(Integer, primary_key=True)
    day = Column(String)
    cnt = Column(Integer)