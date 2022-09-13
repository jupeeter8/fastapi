from pydantic import BaseModel


class VotesResposne(BaseModel):
    user_id: int
    post_id: int
    vote_value: int

    class Config:
        orm_mode = True
