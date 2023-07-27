from fastapi_users_db_sqlalchemy import GUID
from sqlalchemy import Column, String, ForeignKey

from app.core.db import Base


class Service(Base):
    name = Column(String(100), unique=True)
    token = Column(String(300))
    return_token = Column(String(300), nullable=True)
    user_id = Column(GUID, ForeignKey("user.id"))
