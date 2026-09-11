from pydantic import BaseModel

from app.models.db import User


class LoginResponse(BaseModel):
    token: str
    token_type: str = "bearer"


class LoginResult:
    user: User
    access_token: str
    refresh_token: str
