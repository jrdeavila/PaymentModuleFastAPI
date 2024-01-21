from core.infrastructure.injection.inject_mongo_client import inject_mongo_client
from core.infrastructure.mongo.services.mongo_application_auth_service import (
    MongoApplicationLoginService,
    MongoRegisterApplicationService,
)
from core.domain.services.application_auth_service import (
    ApplicationLoginService,
    ApplicationRegisterService,
)


def inject_application_login_service() -> ApplicationLoginService:
    return MongoApplicationLoginService(inject_mongo_client())


def inject_application_register_service() -> ApplicationRegisterService:
    return MongoRegisterApplicationService(inject_mongo_client())
