from datetime import datetime
from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.db import get_async_session
from app.crud.service import service_crud

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    service_name: str
    token: str


class Service(BaseModel):
    name: str


def create_access_token(service_name: str):
    to_encode = {"service_name": service_name}
    to_encode.update({"created": str(datetime.utcnow())})
    encoded_jwt = jwt.encode(
        to_encode,
        settings.secret_key_service,
        algorithm=settings.secret_algorithm_service,
    )
    return encoded_jwt


async def get_current_service(
    token: Annotated[str, Depends(oauth2_scheme)],
    session: AsyncSession = Depends(get_async_session),
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token,
            settings.secret_key_service,
            algorithms=[settings.secret_algorithm_service],
        )
        service_name: str = payload.get("service_name")
        if service_name is None:
            raise credentials_exception
        token_data = TokenData(service_name=service_name, token=token)
    except JWTError:
        raise credentials_exception
    service = await service_crud.get_service_for_auth(
        service_name=token_data.service_name,
        token=token_data.token,
        session=session,
    )
    if service is None:
        raise credentials_exception
    return service
