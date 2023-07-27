from typing import Optional

from pydantic import EmailStr
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_title: str = "Телеграм-информер"
    description: str = "Сервис для отправки информационных сообщений в telegram"
    database_url: str = "sqlite+aiosqlite:///./fastapi.db"
    secret: str = "SECRET"
    service_url: Optional[str] = None
    service_port: Optional[int] = None
    first_superuser_email: Optional[EmailStr] = None
    first_superuser_password: Optional[str] = None
    secret_key_service: Optional[str] = None
    secret_algorithm_service: Optional[str] = None
    telegram_token: Optional[str] = None
    webhook_path: Optional[str] = None
    admin_chat_id: Optional[int] = None
    db_name: Optional[str] = None
    postgres_user: Optional[str] = None
    postgres_password: Optional[str] = None
    db_host: Optional[str] = None
    db_port: Optional[int] = None

    class Config:
        env_file = ".env"


settings = Settings()
