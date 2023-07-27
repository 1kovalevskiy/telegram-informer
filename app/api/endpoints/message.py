from typing import Annotated

from fastapi import APIRouter, status, Depends

from app.core.service import get_current_service
from app.schemas.message import MessageBase, MessageSend
from app.schemas.service import ServiceDB
from app.services.telegram import application

router = APIRouter()


@router.post(
    "/",
    status_code=status.HTTP_202_ACCEPTED,
    dependencies=[Depends(get_current_service)],
)
async def send_message(
    request: MessageBase,
    service: Annotated[ServiceDB, Depends(get_current_service)],
):
    await application.update_queue.put(
        MessageSend(service=service.name, **request.model_dump())
    )
