from pydantic import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "DamDam-App"
    DEBUG: bool = False
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_NAME: str

settings = Settings()
