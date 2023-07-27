from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.service import Service
from app.schemas.user import UserRead


class CRUDService(CRUDBase):
    async def get_service_for_auth(
        self,
        service_name: str,
        token: str,
        session: AsyncSession,
    ) -> Service | None:
        db_service = await session.execute(
            select(self.model)
            .where(self.model.name == service_name)
            .where(self.model.token == token)
        )
        db_service = db_service.scalars().first()
        return db_service

    async def get_by_name(
        self,
        service_name: str,
        session: AsyncSession,
        user: Optional[UserRead] = None,
    ) -> Service | None:
        query = select(self.model).where(self.model.name == service_name)
        if user:
            query = query.where(self.model.user_id == user.id)
        db_service = await session.execute(query)
        db_service = db_service.scalars().first()
        return db_service

    async def get_all_user_services(
        self,
        session: AsyncSession,
        user: UserRead,
    ) -> list[Service]:
        db_service = await session.execute(
            select(self.model).where(self.model.user_id == user.id)
        )
        db_service = db_service.scalars().all()
        return db_service


service_crud = CRUDService(Service)
