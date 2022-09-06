from datetime import datetime
from pydantic import BaseModel
from typing import Optional


class Post(BaseModel):
    title: str
    content: str
    user: Optional[str]


class updatePost(BaseModel):
    title: Optional[str] = None
    content: Optional[str]
    user: str


class PostResponse(Post):
    created_at: datetime

    class Config:
        orm_mode = True
