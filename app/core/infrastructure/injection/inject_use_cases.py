from core.application.use_cases.create_payment_use_case import CreatePaymentUseCase
from core.infrastructure.injection.inject_payment_repository import (
    inject_payment_repository,
    inject_user_repository,
)
from core.infrastructure.injection.inject_send_transaction_service import (
    inject_send_transaction_service,
)


def inject_create_payment_use_case():
    return CreatePaymentUseCase(
        payment_repository=inject_payment_repository(),
        user_repository=inject_user_repository(),
        send_transaction_service=inject_send_transaction_service(),
    )
