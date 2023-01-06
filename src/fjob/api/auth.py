from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from .. import models
from ..services.auth import AuthService

router = APIRouter(
    prefix='/auth',
    tags=['auth'],
)


@router.post(
    '/sign-in/',
    response_model=models.Token,
)
def sign_in(
        auth_data: OAuth2PasswordRequestForm = Depends(),
        auth_service: AuthService = Depends(),
):
    return auth_service.authenticate_user(
        auth_data.username,
        auth_data.password,
    )
