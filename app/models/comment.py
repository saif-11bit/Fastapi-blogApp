from pydantic import BaseModel
from .dbmodel import DBModelMixin
from .rwmodel import RWModel
from .dbmodel import PyObjectId
from typing import Optional

class CommentBase(RWModel):
    body: str
    

class Comment(CommentBase):
    pass


class CommentInDB(DBModelMixin, Comment):
    post_id: PyObjectId
    commented_by: PyObjectId


class CommentInResponse(CommentInDB):
    pass


class CommentInCreate(CommentBase):
    pass