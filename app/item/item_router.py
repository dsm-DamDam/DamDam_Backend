from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database.session import get_db
from item import item_service
from .schemas import HW, daily_count
from datetime import datetime


router = APIRouter()

@router.post("/get_item")
async def get_item(item : HW, db : Session = Depends(get_db)):
    add_data = item_service.add_count(db, datetime.now() ,item.count)
    if add_data is None:
        raise HTTPException(status_code=400, detail="데이터가 전송이 되지 않았습니다.")
    return add_data, {"detail":"데이터가 성공적으로 전송 되었습니다."}

