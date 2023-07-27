from pydantic import BaseModel


class MessageBase(BaseModel):
    user: int
    message: str


class MessageSend(MessageBase):
    service: str = 'telegram_informer'
