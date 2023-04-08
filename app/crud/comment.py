from fastapi import Request
from typing import List
from ..models.comment import CommentInDB
from bson import ObjectId
from ..models.comment import CommentInCreate
from datetime import datetime
from ..models.dbmodel import PyObjectId

async def get_all_comments_on_post_in_db(id: str, request: Request) -> List[CommentInDB]:
    comments = [doc async for doc in request.app.mongodb['comments'].find({'post_id': ObjectId(id)})]

    return comments


async def add_comment_on_post_db(id: str, request: Request, \
comment: CommentInCreate, current_user: str) -> CommentInDB:
    comment_dict = comment.dict()
    comment_dict['post_id'] = ObjectId(id)
    comment_dict['commented_by'] = current_user['_id']
    comment_dict["updated_at"] = datetime.now()
    comment_dict["created_at"] = datetime.now()
    
    await request.app.mongodb["comments"].insert_one(comment_dict)

    return CommentInDB(**comment_dict)
    