from typing import Optional

from pydantic import BaseModel, Field, UUID4


class ServiceUpdate(BaseModel):
    token: str = Field(..., min_length=1, max_length=300)


class ServiceBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)


class ServiceBaseFull(ServiceBase):
    token: str | None = Field(None, min_length=1, max_length=300)


class ServiceDB(ServiceBaseFull):
    id: int
    user_id: Optional[UUID4]

    class Config:
        from_attributes = True
