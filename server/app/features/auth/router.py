from fastapi import APIRouter, Depends, Request, Response
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.features.auth import services
from app.features.auth.constants import REFRESH_COOKIE_NAME, REFRESH_COOKIE_PATH
from app.features.auth.dependencies import get_current_user
from app.features.auth.exceptions import InvalidCredentialsError
from app.features.auth.schemas import LoginResponse, TokenResponse
from app.models.db.user import User

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=LoginResponse)
def login(
    request: Request,
    response: Response,
    form: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
) -> LoginResponse:
    user = services.authenticate_user(
        db,
        form.username,
        form.password,
    )

    access_token = services.generate_access_token(user)

    refresh_token = services.generate_refresh_token(
        db,
        user,
        user_agent=request.headers.get("user-agent"),
        ip_address=request.client.host if request.client else None,
    )

    _set_refresh_cookie(response, refresh_token)

    return LoginResponse(
        token=access_token,
        token_type="bearer",
    )


@router.post("/refresh", response_model=TokenResponse)
def refresh(
    request: Request,
    response: Response,
    db: Session = Depends(get_db),
) -> TokenResponse:
    refresh_token = request.cookies.get(REFRESH_COOKIE_NAME)

    if refresh_token is None:
        raise InvalidCredentialsError()

    access_token, new_refresh_token = services.redeem_refresh_token(
        db,
        refresh_token,
    )

    _set_refresh_cookie(response, new_refresh_token)

    return TokenResponse(
        token=access_token,
        token_type="bearer",
    )


@router.post("/logout", status_code=204)
def logout(
    request: Request,
    response: Response,
    db: Session = Depends(get_db),
) -> None:
    refresh_token = request.cookies.get(REFRESH_COOKIE_NAME)

    if refresh_token is not None:
        services.logout(db, refresh_token)

    _clear_refresh_cookie(response)


@router.post("/logout-all", status_code=204)
def logout_all(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> None:
    services.logout_all(db, current_user)


def _set_refresh_cookie(response: Response, refresh_token: str) -> None:
    response.set_cookie(
        key=REFRESH_COOKIE_NAME,
        value=refresh_token,
        httponly=True,
        secure=True,
        samesite="lax",
        path=REFRESH_COOKIE_PATH,
    )


def _clear_refresh_cookie(response: Response) -> None:
    response.delete_cookie(
        key=REFRESH_COOKIE_NAME,
        path=REFRESH_COOKIE_PATH,
    )
