from pydantic import BaseModel

class Token(BaseModel):
    access_token : str
    token_type : str
    id : int 

class updatePW(BaseModel):
    id : int
    password : str
    change_password : str
    confirm_change_password : str

class updateInfo(BaseModel):
    id : int
    new_nickname : str
    new_userID : str
    new_email : str
    password : str

class User(BaseModel):
    userID: str
    nickname: str
    email: str
    password: str

    class Config:
        from_attributes = True

class SignUp(BaseModel):
    auth_code : int
    nickname: str
    email: str
    userID: str
    password: str
    confirm_password: str

class Login(BaseModel):
    userID: str
    password: str