from pydantic import BaseModel

class TokenData(BaseModel):
    id: str

class Token(BaseModel):
    access_token: str
    token_type: str