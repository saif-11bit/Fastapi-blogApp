from fastapi import APIRouter, Request, Depends, HTTPException, status
from ...core.jwt_oauth2 import get_current_user
from ...models.comment import CommentInCreate, CommentInResponse
from typing import List
from ...crud.post import get_post_by_id_in_db
from ...crud.comment import get_all_comments_on_post_in_db, add_comment_on_post_db


router = APIRouter(tags=['Comment'])

@router.get('/posts/{id}/comment', response_model=List[CommentInResponse])
async def get_all_comments_on_post(id: str, request: Request):
    post = await get_post_by_id_in_db(id, request)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='No post with given id!')
    
    posts = await get_all_comments_on_post_in_db(id, request)
    return posts


@router.post('/posts/{id}/comment', response_model=CommentInResponse)
async def add_comment_to_post(id: str, request: Request, comment: CommentInCreate, current_user: str = Depends(get_current_user)):
    post = await get_post_by_id_in_db(id, request)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='No post with given id!')
    comment = await add_comment_on_post_db(id, request, comment, current_user)
    
    return comment
