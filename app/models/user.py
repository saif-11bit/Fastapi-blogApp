from typing import Optional
from pydantic import EmailStr
from .dbmodel import DBModelMixin
from .rwmodel import RWModel


class UserBase(RWModel):
    username: str
    email: EmailStr


class User(DBModelMixin, UserBase):
    pass


class UserInDB(User):
    password: str


class UserInResponse(User):
    pass


class UserInCreate(UserBase):
    password: str
    

class UserInUpdate(UserBase):
    password: str
