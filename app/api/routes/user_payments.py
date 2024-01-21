from fastapi import APIRouter, Depends

from core.application.use_cases.get_user_payments_use_case import GetUserPaymentsUseCase
from core.domain.entities.payment import Payment
from core.infrastructure.injection.inject_use_cases import (
    inject_get_user_payments_use_case,
)


router: APIRouter = APIRouter()


@router.get("/user/{user_id}/payments")
def get_all(
    user_id: str,
    get_user_payments_use_case: GetUserPaymentsUseCase = Depends(
        inject_get_user_payments_use_case
    ),
) -> list[Payment]:
    return get_user_payments_use_case.get(user_id)
