from pydantic import BaseModel, ConfigDict
from typing import Optional

class UserCreate(BaseModel):
    username: str
    email: str
    plan: str
    password: str

class UserLogin(BaseModel):
    email: str
    password: str

class UserOut(BaseModel):
    id: int
    username: str
    email: str
    plan: str
    model_config = ConfigDict(from_attributes=True)

# Schema for creating content (sent to Backend)
class ContentCreate(BaseModel):
    prompt: str
    file_path: str
    owner_id: int

# Schema for returning content (sent to Frontend)
class ContentOut(BaseModel):
    id: int
    prompt: str
    file_path: str
    gemini_output: Optional[str] = None
    owner_id: int

    model_config = ConfigDict(from_attributes=True)