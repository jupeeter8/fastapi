from datetime import datetime
from pydantic import BaseModel
from typing import Optional


class Post(BaseModel):
    title: str
    content: str


class updatePost(BaseModel):
    title: Optional[str] = None
    content: Optional[str]


class PostResponse(Post):
    created_at: datetime
    user_id: int

    class Config:
        orm_mode = True
