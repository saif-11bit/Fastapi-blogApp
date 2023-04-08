import uuid
from typing import Optional, List
from pydantic import BaseModel, Field
from .rwmodel import RWModel
from .dbmodel import DateTimeModelMixin, DBModelMixin, PyObjectId
        

class PostBase(RWModel):
    title: str
    content: str


class Post(DateTimeModelMixin, PostBase):
    pass


class PostInDB(DBModelMixin, Post):
    author_id: PyObjectId

class PostInResponse(PostInDB):
    pass


class PostInCreate(PostBase):
    pass


class PostInUpdate(PostBase):
    pass

    