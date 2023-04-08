from fastapi import Request, HTTPException, status
from ..models.user import UserInDB, UserInCreate
from pydantic import EmailStr
from datetime import datetime
from ..core.security import hash_password
from typing import List
from bson import ObjectId


async def get_all_users_in_db(request: Request, \
    offset: int, limit: int) -> List[UserInDB]:
    users = [doc async for doc in request.app.mongodb['users'].find(limit=limit, skip=offset)]

    return users

async def get_user_by_username(request: Request, username: str) -> UserInDB:
    user = await request.app.mongodb['users'].find_one({'username': username})
    if user:
        return UserInDB(**user)

    
async def get_user_by_email(request: Request, email: EmailStr) -> UserInDB:
    user = await request.app.mongodb['users'].find_one({'email': email})
    if user:
        return UserInDB(**user)
    

async def get_user_by_id_in_db(request: Request, id: str) -> UserInDB:
    user = await request.app.mongodb["users"].find_one({'_id': ObjectId(id)})
    if user:
        return UserInDB(**user)
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No user with id {id}")
    
async def create_user_in_db(request: Request, user: UserInCreate) -> UserInDB:
    hashed_password = hash_password(user.password)
    user.password = hashed_password
    user_dict =user.dict()
    user_dict["updated_at"] = datetime.now()
    user_dict["created_at"] = datetime.now()
    await request.app.mongodb['users'].insert_one(user_dict)
    
    return UserInDB(**user_dict)

