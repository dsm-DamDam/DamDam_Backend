from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, Depends, HTTPException, Request
import uvicorn
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from core.config import settings
from database.models import Base
from user.user_router import router as user_router
from item.item_router import router as item_router

DB_URL = f"mysql+pymysql://{settings.DB_USER}:{settings.DB_PASSWORD}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}?charset=utf8"

engine = create_engine(DB_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

app = FastAPI(title=settings.APP_NAME, debug=settings.DEBUG, version='1.0.0')
app.router.redirect_slashes = False

app.include_router(user_router, prefix="/user", tags=["users"])
app.include_router(item_router, prefix="/item", tags=["items"])

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get('/')
async def test():
    return 'Server is Working!'

if __name__ == '__main__':
    uvicorn.run("main:app", host='',port=8080,reload=True)
