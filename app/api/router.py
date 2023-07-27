from fastapi import APIRouter

from app.api.endpoints import (
    message_router,
    service_router,
    telegram_router,
    user_router,
)
from app.core.config import settings

main_router = APIRouter()
main_router.include_router(message_router, prefix="/message", tags=["Message"])
main_router.include_router(service_router, prefix="/service", tags=["Service"])
main_router.include_router(
    telegram_router,
    prefix=settings.webhook_path,
    tags=["Telegram Webhook"],
    include_in_schema=False,
)
main_router.include_router(user_router)
