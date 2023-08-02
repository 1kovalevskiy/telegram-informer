from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.service import create_access_token
from app.core.user import current_superuser, current_active_user
from app.crud.service import service_crud
from app.schemas.service import (
    ServiceBase,
    ServiceBaseFull,
    ServiceDB,
    ServiceUpdate,
)
from app.schemas.user import UserCreate
from app.services.telegram import send_message

router = APIRouter()


@router.post(
    "/",
    response_model=ServiceDB,
    dependencies=[Depends(current_active_user)],
    status_code=status.HTTP_201_CREATED,
)
async def add_new_service(
    service: ServiceBase,
    session: AsyncSession = Depends(get_async_session),
    user: UserCreate = Depends(current_active_user),
):
    exist_service = await service_crud.get_by_name(
        service_name=service.name, session=session
    )
    await send_message(f"{user.email} create service token for `{service.name}`")
    if exist_service:
        raise HTTPException(status_code=403, detail="Service exist")
    new_token = create_access_token(service_name=service.name)
    service = ServiceBaseFull(**service.model_dump(), token=new_token)
    new_service = await service_crud.create(service, session, user)
    return new_service


@router.patch(
    "/",
    response_model=ServiceDB,
    dependencies=[Depends(current_active_user)],
    status_code=status.HTTP_200_OK,
)
async def update_token(
    service: ServiceBase,
    session: AsyncSession = Depends(get_async_session),
    user: UserCreate = Depends(current_active_user),
):
    exist_service = await service_crud.get_by_name(
        service_name=service.name, session=session, user=user
    )
    if not exist_service:
        raise HTTPException(status_code=404, detail="Service doesn't exist")
    await send_message(f"Try update service token for `{service.name}`")
    new_token = create_access_token(service_name=service.name)
    service = ServiceUpdate(token=new_token, return_token=service.return_token)
    patch_service = await service_crud.update(exist_service, service, session)
    return patch_service


@router.get(
    "/",
    response_model=list[ServiceDB],
    dependencies=[Depends(current_active_user)],
)
async def get_my_services(
    session: AsyncSession = Depends(get_async_session),
    user: UserCreate = Depends(current_active_user),
):
    services = await service_crud.get_all_user_services(session, user)
    return services


@router.get(
    "/all",
    response_model=list[ServiceDB],
    dependencies=[Depends(current_superuser)],
)
async def get_all_services(
    session: AsyncSession = Depends(get_async_session),
):
    services = await service_crud.get_multi(session)
    return services
