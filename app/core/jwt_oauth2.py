from datetime import datetime, timedelta
from jose import jwt, JWTError
from .config import settings
from ..models.token import TokenData
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status, Request
from bson import ObjectId

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/auth/login',scheme_name="JWT")

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    
    return encoded_jwt


def verify_access_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        id = payload.get("user_id")
        if id is None:
            raise credentials_exception
        token_data = TokenData(id=id)
    except JWTError:
        raise credentials_exception
    return token_data


async def get_current_user(request: Request, token: str = Depends(oauth2_scheme)):
    
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Could not validata credentials", headers={"WW-Authenticate": "Bearer"})
    token = verify_access_token(token, credentials_exception)
    user = await request.app.mongodb['users'].find_one({'_id': ObjectId(token.id)})
    return  user
