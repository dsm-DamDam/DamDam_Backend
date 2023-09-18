from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from core.config import settings

# MySQL 데이터베이스 연결 문자열을 생성합니다.
DATABASE_URL = f"mysql://{settings.DB_USER}:{settings.DB_PASSWORD}@{settings.DB_HOST}/{settings.DB_NAME}"

# SQLAlchemy 엔진을 생성합니다.
engine = create_engine(DATABASE_URL)

# SQLAlchemy 세션 생성기를 생성합니다.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)