from datetime import datetime
from typing import List

from pydantic import BaseModel

from ..models import Role


class BaseUser(BaseModel):
    id: int
    first_name: str
    second_name: str
    role: Role

    class Config:
        orm_mode = True


class CreateUser(BaseModel):
    email: str
    password: str
    first_name: str
    second_name: str

    class Config:
        orm_mode = True


class AuthUser(BaseModel):
    id: int
    role: Role

    class Config:
        orm_mode = True


class UpdateExecutor(BaseModel):
    first_name: str
    second_name: str


class Comments(BaseModel):
    rating: int
    text: str

    class Config:
        orm_mode = True


class ExecutorFullInfo(BaseModel):
    first_name: str
    second_name: str
    email: str
    date_create: datetime
    comments: List[Comments]
