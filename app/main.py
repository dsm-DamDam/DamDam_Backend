from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
import uvicorn
from core.config import settings
from user.user_router import router as user_router

app = FastAPI(title=settings.APP_NAME, debug=settings.DEBUG, version='1.0.0')
app.include_router(user_router, prefix="/user", tags=["users"])

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
    uvicorn.run("main:app", reload=True)