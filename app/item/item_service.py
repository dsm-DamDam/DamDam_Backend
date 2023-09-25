from database.models import Count
from database.session import SessionLocal

def add_count(db:SessionLocal,date : int, count : int):
    new_count_data = Count(date = date, count = count)
    db.add(new_count_data)
    db.commit()
    db.refresh(new_count_data)
    return new_count_data
