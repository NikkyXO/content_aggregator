from pydantic import BaseModel, EmailStr, validator, HttpUrl
from typing import Optional, List


class CreateArticle(BaseModel):
    title: str
    name: str
    description: str
    url: HttpUrl
    pub_date: str
