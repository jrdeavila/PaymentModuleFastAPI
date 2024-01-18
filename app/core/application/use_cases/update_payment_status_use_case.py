from core.domain.entities.payment import Payment
from core.domain.repositories.payment_repository import PaymentRepository


class UpdatePaymentStatusUseCase:
    payment_repository: PaymentRepository

    def __init__(self, payment_repository: PaymentRepository) -> None:
        self.payment_repository = payment_repository

    def execute(self, id: str) -> Payment:
        payment = self.payment_repository.get(id)
        return payment