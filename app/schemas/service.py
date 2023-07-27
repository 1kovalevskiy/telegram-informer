from typing import Optional

from pydantic import BaseModel, Field, UUID4


class ServiceUpdate(BaseModel):
    return_token: str | None = Field(None, min_length=1, max_length=300)
    token: str = Field(..., min_length=1, max_length=300)


class ServiceBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    return_token: str | None = Field(None, min_length=1, max_length=300)


class ServiceBaseFull(ServiceBase):
    token: str | None = Field(None, min_length=1, max_length=300)


class ServiceDB(ServiceBaseFull):
    id: int
    user_id: Optional[UUID4]

    class Config:
        from_attributes = True
