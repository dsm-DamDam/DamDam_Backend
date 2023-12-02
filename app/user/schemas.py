from pydantic import BaseModel

class Token(BaseModel):
    access_token : str
    token_type : str
    id : int 

class TokenData(BaseModel):
    id : int

class updatePW(BaseModel):
    password : str
    change_password : str
    confirm_change_password : str

class updateInfo(BaseModel):
    new_nickname : str
    new_userID : str

class User(BaseModel):
    userID: str
    nickname: str
    email: str

    class Config:
        from_attributes = True

class Auth(BaseModel):
    auth_code : int

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