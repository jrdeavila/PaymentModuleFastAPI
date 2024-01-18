from typing import Union

from fastapi import APIRouter, Depends

from api.requests.transaction_event_request import TransactionEventRequest
from core.application.use_cases.rechage_user_balance_use_case import (
    RechargeUserBalanceUseCase,
)
from core.domain.entities.payment import Payment
from core.infrastructure.injection.inject_use_cases import (
    inject_update_payment_status_use_case,
)


class OnTransactionChangeEventCtrl:
    router: APIRouter = APIRouter()

    @router.post("/")
    def on_transaction_change_event(
        transaction_event_request: TransactionEventRequest,
        recharge_use_balance_use_case: RechargeUserBalanceUseCase = Depends(
            inject_update_payment_status_use_case
        ),
    ) -> Payment:
        payment = recharge_use_balance_use_case.execute(
            transaction_event_request.data.transaction.id,
            transaction_event_request.data.transaction.status,
        )
        return payment
