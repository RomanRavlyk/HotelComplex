from pydantic import BaseModel

class CreateUser(BaseModel):
    username: str
    password: str

class UserResponse(BaseModel):
    username: str
    user_id: int
