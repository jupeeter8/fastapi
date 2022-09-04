from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class User(BaseModel):
    username: str
    password: str


class CreatedUser(BaseModel):
    # Email validator can be used to validate emails.
    id: int
    username: str
    joined_at: datetime

    class Config:
        orm_mode = True
