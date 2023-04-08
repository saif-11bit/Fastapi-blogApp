from fastapi import (
    APIRouter,
    Request,
    Depends,
    HTTPException,
    status
)
from ...models.user import (
    UserInCreate,
    UserInResponse
)
from ...models.token import Token
from ...crud.utils import check_free_username_and_email
from ...crud.user import create_user_in_db, get_user_by_username
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from ...core.security import verify_password
from ...core.jwt_oauth2 import create_access_token

router = APIRouter(prefix='/auth', tags=['Authentication'])


@router.post("/register", response_model=UserInResponse)
async def register(user: UserInCreate, request:Request):
    
    await check_free_username_and_email(request, user.username, user.email)
    user = await create_user_in_db(request, user)
    return user


@router.post("/login", response_model=Token)
async def login(request: Request, user_credentials: OAuth2PasswordRequestForm = Depends()):
    
    user = await get_user_by_username(request, user_credentials.username)
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='invalid credentials!')
    if not verify_password(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='invalid credentials!')
    
    access_token = create_access_token(data={"user_id": str(user.id)})
    return {"access_token": access_token, "token_type": "bearer"}


