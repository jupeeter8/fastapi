from pydantic import BaseModel


class VotesResposne(BaseModel):
    user_id: int
    post_id: int

    class Config:
        orm_mode = True
