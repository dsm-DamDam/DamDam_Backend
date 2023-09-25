from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "DamDam-App"
    DEBUG: bool = False
    DB_USER: str = "default_user"
    DB_PASSWORD: str = "default_password"
    DB_HOST: str = "localhost"
    DB_NAME: str = "default_database"
    DB_PORT: int = 3306
    SECRET_KEY : str = "909889124130safa31bda1"

settings = Settings()
