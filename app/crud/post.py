from typing import List
from fastapi import (
    Request,
    HTTPException,
    status
)
from ..models.post import (
    PostInDB,
    PostInCreate,
    PostInUpdate
)
from datetime import datetime
from bson import ObjectId


async def list_of_posts_in_db(
    request: Request, limit: int, offset: int) -> List[PostInDB]:
    posts = [doc async for doc in request.app.mongodb['posts'].find(limit=limit, skip=offset)]
    # for doc in await request.app.mongodb["posts"].find().to_list(1000):
    #     posts.append(
    #         PostInDB(
    #             **doc
    #         )
    #     )
    
    return posts


async def get_post_by_id_in_db(
    id: str, request: Request) -> PostInDB:
    try:
        if (post := await request.app.mongodb["posts"].find_one({"_id": ObjectId(id)})) is not None:
            return PostInDB(**post)
        
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No post with id {id}")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid ID!")
        

async def create_post_in_db(post: PostInCreate, request: Request, current_user: str) -> PostInDB:
    post_dict =post.dict()
    post_dict["author_id"] = current_user['_id']
    post_dict["updated_at"] = datetime.now()
    post_dict["created_at"] = datetime.now()
    
    response = await request.app.mongodb["posts"].insert_one(post_dict)
    return PostInDB(**post_dict)


async def update_post_in_db(request: Request, id: str, update_post: PostInUpdate) -> PostInDB:
    
    post = await get_post_by_id_in_db(id, request)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid ID!")

    if update_post.title:
        post.title = update_post.title
    if update_post.content:
        post.content = update_post.content
 
    post.updated_at = datetime.now()
    await request.app.mongodb['posts'].update_one({"_id": ObjectId(id)}, {"$set":post.dict()})
    
    return post
    
    
async def delete_post_in_db(request: Request, id: str):
    try:
        post = await get_post_by_id_in_db(id, request)
        if not post:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid ID!")
        post = await request.app.mongodb['posts'].delete_one({"_id": ObjectId(id)})
        return True
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="Something went wrong!")
    