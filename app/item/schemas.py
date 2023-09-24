from pydantic import BaseModel, constr

class HW(BaseModel):
    count : int

class daily_count(BaseModel):
    day : str
    count : int

class CountCreate(BaseModel):
    count: int