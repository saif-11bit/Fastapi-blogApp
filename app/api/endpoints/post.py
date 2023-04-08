from fastapi import APIRouter, Request, status, HTTPException, Depends
from ...models.post import (
    PostInUpdate,
    PostInResponse,
    PostInCreate
)
from ...crud.post import (
    list_of_posts_in_db,
    get_post_by_id_in_db,
    create_post_in_db,
    update_post_in_db,
    delete_post_in_db
)
from typing import List
from ...core.jwt_oauth2 import get_current_user
from ...crud.utils import check_existance_of_post_and_permission


router = APIRouter(prefix='/posts', tags=['Post'])


@router.get('/', response_model=List[PostInResponse])
async def get_all_posts(request: Request):
    posts = await list_of_posts_in_db(request) 
    return posts


@router.get('/{id}', response_model=PostInResponse)
async def get_post_by_id(
    id: str,
    request: Request
):
    post = await get_post_by_id_in_db(id, request)
    return post


@router.post(
    '/',
    response_model=PostInResponse,
    status_code=status.HTTP_201_CREATED
)
async def create_post(post: PostInCreate, request:Request, current_user: str = Depends(get_current_user)):
    post_created = await create_post_in_db(post, request, current_user)
    return post_created


@router.put('/{id}', response_model=PostInResponse)
async def update_post(id: str, update_post: PostInUpdate, request: Request, current_user: str = Depends(get_current_user)):
    await check_existance_of_post_and_permission(id, request, current_user['_id'])
    updated_post = await update_post_in_db(request, id, update_post)
    return updated_post


@router.delete('/{id}')
async def delete_post(request: Request, id: str, current_user: str = Depends(get_current_user)):
    try:
        await check_existance_of_post_and_permission(id, request, current_user['_id'])
        deleted = await delete_post_in_db(request, id)
        return deleted
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="Something went wrong!")
