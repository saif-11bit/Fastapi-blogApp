from fastapi import (
    Depends,
    APIRouter,
    Request,
    HTTPException,
    status
)
from ...models.user import (
    UserInResponse
)
from typing import List
from ...crud.user import (
    get_all_users_in_db,
    get_user_by_id_in_db
)

router = APIRouter(prefix='/users', tags=['User'])


@router.get("/", response_model=List[UserInResponse])
async def get_all_users(request: Request, offset: int = 0, limit: int = 10):
    users = await get_all_users_in_db(request, offset, limit)
    return users


@router.get("/{id}", response_model=UserInResponse)
async def get_user_by_id(request: Request, id: str):
    try:
        user = await get_user_by_id_in_db(request, id)
        return user
    except:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No user with id {id}")


