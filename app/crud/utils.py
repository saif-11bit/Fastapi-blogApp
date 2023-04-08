from fastapi import Request, HTTPException, status
from pydantic import EmailStr
from .user import get_user_by_username, get_user_by_email
from bson import ObjectId
from .post import get_post_by_id_in_db


async def check_free_username_and_email(request: Request, username: str, email: EmailStr):
    if username:
        user_by_username = await get_user_by_username(request, username)
        if user_by_username:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, \
                detail="User with this username already exists!")

    if email:
        user_by_email = await get_user_by_email(request, email)
        if user_by_email:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, \
                detail="User with this email already exists!")
            
            
async def check_existance_of_post_and_permission(id: str, request: Request, current_user: ObjectId):
    post = await get_post_by_id_in_db(id, request)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='No such post!')
    if post.author_id != current_user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='You cannot access this post!')
    
