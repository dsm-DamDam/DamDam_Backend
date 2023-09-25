from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from database.session import get_db
from item import item_service
from .schemas import HW, daily_count
from datetime import date
from database.models import Count

router = APIRouter()

@router.post("/get-item")
async def get_item(item : HW, db : Session = Depends(get_db)):
    add_data = item_service.add_count(db, date.today() ,item.count)
    if add_data is None:
        raise HTTPException(status_code=400, detail="데이터가 전송이 되지 않았습니다.")
    return add_data, {"detail":"데이터가 성공적으로 전송 되었습니다."}

@router.get("/daily-total-cnt")
async def daily_total_count( db : Session = Depends(get_db)):
    total =  db.query(func.sum(Count.count)).filter(Count.date == date.today()).scalar() or 0
    return {"total_count": total, "today":date.today()}