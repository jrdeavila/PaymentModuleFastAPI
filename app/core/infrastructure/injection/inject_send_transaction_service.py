from core.domain.services.send_transaction_service import SendTransactionService
from core.infrastructure.http.features.wompi.send_transaction_via_wompi_service import (
    SendTransactionViaWompiService,
)

import os


def inject_send_transaction_service():
    environment_env_var = os.getenv("WOMPI_ENV")
    token_env_var = os.getenv("WOMPI_PRIVATE_KEY")

    return SendTransactionViaWompiService(
        token=token_env_var, environment=environment_env_var
    )
