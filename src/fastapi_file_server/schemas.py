from datetime import datetime

from pydantic import BaseModel


class UserBase(BaseModel):
    name: str
    email: str


class UserCreate(UserBase):
    user_id: str
    password1: str
    password2: str


class UserUpdate(UserBase):
    password1: str
    password2: str


class UserUpdateAdmin(UserBase):
    is_admin: bool
    is_active: bool


class User(UserBase):
    id: int
    user_id: str
    is_admin: bool
    is_active: bool
    licenses: list["License"]
    create_date: datetime
    update_date: datetime

    class Config:
        orm_mode = True


class UserLogin(BaseModel):
    user_id: str
    password: str


class UserPasswordUpdate(BaseModel):
    cur_password: str
    password1: str
    password2: str
    

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


class LicenseBase(BaseModel):
    name: str
    user_id: int
    file_id: int
    is_active: bool
    valid_date: datetime


class LicenseCreate(LicenseBase):
    pass


class LicenseUpdate(LicenseBase):
    pass


class License(LicenseBase):
    id: int
    file: File
    create_date: datetime
    update_date: datetime

    class Config:
        orm_mode = True


User.update_forward_refs()