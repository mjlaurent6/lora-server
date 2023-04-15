# build a schema using pydantic
from pydantic import BaseModel

class EventUp(BaseModel):
    name: str
    age: int

    class Config:
        orm_mode = True

