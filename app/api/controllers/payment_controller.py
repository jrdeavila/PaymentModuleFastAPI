from fastapi import APIRouter, Depends
from api.requests.create_payment_request import CreatePaymentRequest
from core.application.use_cases.create_payment_use_case import CreatePaymentUseCase
from core.infrastructure.injection.inject_use_cases import (
    inject_create_payment_use_case,
)
from core.domain.entities.payment import Payment

from core.domain.repositories.payment_repository import PaymentRepository
from core.infrastructure.injection.inject_payment_repository import (
    inject_payment_repository,
)


class PaymentCtrl:
    router = APIRouter()

    @router.get("/")
    def get_all(
        payment_repository: PaymentRepository = Depends(inject_payment_repository),
    ) -> list[Payment]:
        res = payment_repository.get_all()
        return res

    @router.get("/{id}")
    def get(
        id: str,
        payment_repository: PaymentRepository = Depends(inject_payment_repository),
    ) -> Payment:
        res = payment_repository.get(id)
        return res

    @router.post("/", status_code=201)
    def create(
        request: CreatePaymentRequest,
        create_payment_use_case: CreatePaymentUseCase = Depends(
            inject_create_payment_use_case
        ),
    ) -> Payment:
        res = create_payment_use_case.execute(request.to_payment())
        return res

    @router.delete("/", status_code=204)
    def delete(
        id: str,
        payment_repository: PaymentRepository = Depends(inject_payment_repository),
    ) -> None:
        payment_repository.delete(id)
