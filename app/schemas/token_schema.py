from pydantic import BaseModel, EmailStr
from typing import Optional


class Email(BaseModel):
    email: EmailStr


class Token(BaseModel):
    data: dict
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str] = None


class two_factor(Email):
    mfa_hash: str
