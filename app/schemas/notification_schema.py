from pydantic import BaseModel, EmailStr, validator
from pydantic.types import conint
from datetime import datetime
from typing import Optional, List, Union
from uuid import uuid4, UUID


class NotificationBase(BaseModel):
    owner_id: int
    content_id: int
    type: str
    title: str


class NotificationCreate(NotificationBase):
    pass


class Notification(NotificationBase):
    notification_id: int
    unread: bool = True

    class Config:
        orm_mode = True
