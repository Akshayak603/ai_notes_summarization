from pydantic import BaseModel, EmailStr
from typing import Optional

'''User'''
class UserBase(BaseModel):
    email: EmailStr
    username: str

class UserRegister(UserBase):
    password: str
    
    class Config:
        orm_mode = True

class UserRegisterResponse(UserBase):
    id: int

    class Config:
        orm_mode = True

class UserLogin(BaseModel):
    username: str
    password: str

'''Notes'''
class NotesCreate(BaseModel):
    title: str
    content: str
    summary: str

class NotesResponse(NotesCreate):
    id: int
    user_id: int

    class Config:
        orm_mode = True

class NoteSummaryRequest(BaseModel):
    content: str
    previous_summary: Optional[str]=None

class NoteSummaryResponse(BaseModel):
    summary: str

    