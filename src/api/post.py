from datetime import datetime

from fastapi import APIRouter
from pydantic import BaseModel

post_router = APIRouter()


class Post(BaseModel):
    id: str
    author: str
    title: str
    content: str
    created_at: datetime


class PostCreate(BaseModel):
    author: str
    title: str
    content: str
