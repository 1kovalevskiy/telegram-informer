from fastapi import APIRouter, Request
from telegram import Update

from app.services.telegram import application

router = APIRouter()


@router.post("")
async def telegram(
    request: Request,
):
    body = await request.json()
    await application.update_queue.put(
        Update.de_json(data=body, bot=application.bot)
    )
