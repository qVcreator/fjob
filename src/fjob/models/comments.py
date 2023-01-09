from pydantic import BaseModel


class CreateComment(BaseModel):
    user_to_id: int
    rating: int
    text: str


class CommentOutput(BaseModel):
    user_from_id: int
    user_to_id: int
    rating: int
    text: str

    class Config:
        orm_mode = True
