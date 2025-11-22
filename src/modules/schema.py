from pydantic import BaseModel

class Writing(BaseModel):
    title: str
    writer: str
    board: str
    date: str
    content: str
    liked: str

