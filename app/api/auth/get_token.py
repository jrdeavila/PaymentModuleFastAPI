from typing import Annotated, Union
from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm

from api.auth.models import ApplicationToken
from api.requests.register_application_request import RegisterApplicationRequest
from core.domain.entities.application import Application
from core.domain.services.application_auth_service import (
    ApplicationLoginService,
    ApplicationRegisterService,
)
from core.infrastructure.injection.inject_application_auth_service import (
    inject_application_login_service,
    inject_application_register_service,
)


async def get_authenticate_application_token(
    login_service: Annotated[
        ApplicationLoginService, Depends(inject_application_login_service)
    ],
    form_data: OAuth2PasswordRequestForm = Depends(),
) -> Union[ApplicationToken, None]:
    application = login_service.login(
        username=form_data.username, password=form_data.password
    )
    return generate_application_token(application)


async def get_register_application_token(
    register_service: Annotated[
        ApplicationRegisterService, Depends(inject_application_register_service)
    ],
    register_application_request: RegisterApplicationRequest,
) -> ApplicationToken:
    application = Application(
        name=register_application_request.name,
        username=register_application_request.username,
        email=register_application_request.email,
        disabled=False,
    )
    application = register_service.register(
        application=application, password=register_application_request.password
    )

    return generate_application_token(application)


def generate_application_token(application: Application) -> ApplicationToken:
    return ApplicationToken(
        access_token=application.id,
        token_type="bearer",
    )
