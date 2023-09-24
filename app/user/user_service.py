from database.models import User, Auth
from passlib.context import CryptContext
from database.session import SessionLocal

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated="auto")

def get_user_by_id(db: SessionLocal, id: int):
    return db.query(User).filter(User.id == id).first()

def create_user(db:SessionLocal ,auth_code : int , email : str, userID : str, password : str, nickname : str):
    new_user = User(id = auth_code ,email=email, userID=userID, password=password, nickname=nickname)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def hash_password(password):
    return bcrypt_context.hash(password)

def get_user_by_userID(db:SessionLocal, userID : str):
    return db.query(User).filter(User.userID == userID).first()

def get_user_by_auth_code(db:SessionLocal, auth_code : int):
    return db.query(User).filter(User.id == auth_code).first()

def get_user_by_email(db:SessionLocal, email : str):
    return db.query(User).filter(User.email == email).first()

def find_auth_code(db:SessionLocal, auth_code: int):
    return db.query(Auth).filter(Auth.id == auth_code).first()