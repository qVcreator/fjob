import decimal

from pydantic import BaseModel
from enum import Enum


class Status(str, Enum):
    CREATED = 1,
    IN_PROGRESS = 2,
    FINISHED = 3,
    CANCELLED = 4


class Category(str, Enum):
    WEB = 1,
    BACKEND = 2,
    FRONTEND = 3,
    BOT = 4,
    REWRITING = 5,
    ART = 6


class SuggestionCreate(BaseModel):
    user_id: int
    name = str
    description: str
    price: decimal
    category: Category
