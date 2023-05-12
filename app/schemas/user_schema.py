from pydantic import BaseModel, EmailStr, validator
from typing import Optional, List


class User(BaseModel):
    user_id: int
    username: str
    first_name: str
    last_name: str
    email: EmailStr
    date_of_birth: str
    gender: str
    description: str
    image_url: str
    phone_number: str
    work_experience: str
    position: str
    stack: str
    links: List[str]
    role: str
    following: str
    followers: str
    location: str
    account_balance: int
    tokens_earned: int
    total_likes: int
    created_at: str
    is_admin: Optional[bool]

    class Config:
        arbitrary_types_allowed = True


class UserOut(BaseModel):
    user_id: int
    username: str
    first_name: str
    last_name: str
    email: EmailStr
    description: Optional[str]
    image_url: str
    location: str
    account_balance: int


class UserSignInRequest(BaseModel):
    username: str
    firstname: str
    lastname: str
    email: EmailStr
    password: str
    confirmPassword: str

    @validator('confirmPassword')
    def passwords_match(cls, v, values, **kwargs):
        if 'password' in values and v != values['password']:
            raise ValueError('passwords do not match')
        return v


class UserSignInAdminRequest(BaseModel):
    username: str
    firstname: str
    lastname: str
    email: EmailStr
    password: str
    confirmPassword: str
    is_admin: Optional[bool]

    @validator('confirmPassword')
    def passwords_match(cls, v, values, **kwargs):
        if 'password' in values and v != values['password']:
            raise ValueError('passwords do not match')
        return v


class UserVerification(BaseModel):
    email: EmailStr
    verification_code: int


class UserUpdate(BaseModel):
    username: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    description: Optional[str] = None
    phone_number: Optional[str] = None
    date_of_birth: Optional[str] = None
    gender: Optional[str] = None
    work_experience: Optional[str] = None
    position: Optional[str] = None
    stack: Optional[str] = None
    links: List[str] = None
    role: Optional[str] = None
    image_url: Optional[str] = None
    location: Optional[str] = None


class UserSignInResponse(BaseModel):
    pass


class UserBase(UserSignInRequest):
    user_id: int

    class Config:
        orm_mode = True


class ReadUser(UserBase):
    pass


class ChangePasswordRequest(BaseModel):
    oldPassword: str
    newPassword: str
    confirmPassword: str


class ForgotPassword(BaseModel):
    newPassword: str
    confirmPassword: str

    @validator('confirmPassword')
    def passwords_match(cls, v, values, **kwargs):
        if 'newPassword' in values and v != values['newPassword']:
            raise ValueError('passwords do not match')
        return v
