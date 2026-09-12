from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.features.auth import services
from app.features.auth.schemas import LoginResponse

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=LoginResponse)
def login(
    form: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
) -> LoginResponse:
    user = services.authenticate_user(
        db,
        form.username,
        form.password,
    )

    access_token = services.generate_access_token(user)

    return LoginResponse(
        token=access_token,
        token_type="bearer",
    )
