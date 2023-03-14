from datetime import datetime

from pydantic import BaseModel


class UserBase(BaseModel):
    user_id: str
    name: str
    email: str


class UserCreate(UserBase):
    password1: str
    password2: str


class UserUpdate(UserBase):
    is_admin: bool
    is_active: bool


class User(UserBase):
    id: int
    is_admin: bool
    is_active: bool
    create_date: datetime
    update_date: datetime

    class Config:
        orm_mode = True


class UserLogin(BaseModel):
    user_id: str
    password: str
    

class FileBase(BaseModel):
    name: str
    size: int
    is_active: bool


class FileCreate(FileBase):
    pass


class FileUpdate(FileBase):
    pass


class File(FileBase):
    id: int
    save_name: str
    create_date: datetime
    update_date: datetime

    class Config:
        orm_mode = True
