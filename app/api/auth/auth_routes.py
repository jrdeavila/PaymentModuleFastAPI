from typing import Annotated

from api.auth.get_token import (
    get_authenticate_application_token,
    get_register_application_token,
)
from api.auth.models import ApplicationToken
from fastapi import APIRouter, Depends


router = APIRouter()


@router.post("/register")
async def register(
    get_register_application: Annotated[
        ApplicationToken, Depends(get_register_application_token)
    ]
) -> ApplicationToken:
    return get_register_application


@router.post("/token")
async def login(
    get_authenticate_application_token: Annotated[
        ApplicationToken, Depends(get_authenticate_application_token)
    ]
) -> ApplicationToken:
    return get_authenticate_application_token
