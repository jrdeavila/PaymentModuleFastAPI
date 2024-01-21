from typing import Annotated

from fastapi.security import OAuth2PasswordBearer

from api.auth.get_token import (
    get_authenticate_admin_application_token,
    get_authenticate_application_token,
    get_register_application_token,
)
from api.auth.models import ApplicationToken
from fastapi import APIRouter, Depends

from core.domain.entities.application import Application


router = APIRouter()


oauth2_admin_scheme = OAuth2PasswordBearer(
    tokenUrl="/api/v1/auth/admin/token", scheme_name="Admin Token"
)


@router.post("/register", dependencies=[Depends(oauth2_admin_scheme)])
async def register(
    get_register_application: Annotated[
        Application, Depends(get_register_application_token)
    ]
) -> Application:
    return get_register_application


@router.post("/token")
async def login(
    get_authenticate_application_token: Annotated[
        ApplicationToken, Depends(get_authenticate_application_token)
    ]
) -> ApplicationToken:
    return get_authenticate_application_token


@router.post("/admin/token")
async def login_admin(
    get_authenticate_application_token: Annotated[
        ApplicationToken, Depends(get_authenticate_admin_application_token)
    ]
) -> ApplicationToken:
    return get_authenticate_application_token
