# schemas.py

from pydantic import BaseModel

class UserCreate(BaseModel):
    clerkId: str
    username: str
    pic: str
    email: str

    class Config:
        orm_mode = True
