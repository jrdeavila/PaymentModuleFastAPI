from typing import Union
from fastapi import APIRouter, Depends
from core.application.use_cases.update_payment_status_use_case import (
    UpdatePaymentStatusUseCase,
)

from core.domain.entities.payment import Payment
from core.infrastructure.injection.inject_use_cases import (
    inject_update_payment_status_use_case,
)


class OnTransactionChangeEventCtrl:
    router: APIRouter = APIRouter()

    @router.get("/")
    def on_transaction_change_event(
        id: Union[str, None] = None,
        update_payment_status_use_case: UpdatePaymentStatusUseCase = Depends(
            inject_update_payment_status_use_case
        ),
    ) -> Payment:
        return update_payment_status_use_case.execute(id)
