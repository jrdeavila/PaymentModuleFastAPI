from core.domain.entities.payment import Payment
from core.domain.repositories.payment_repository import PaymentRepository
from core.domain.services.recharge_user_balance_service import (
    RechargeUserBalanceService,
)


class RechargeUserBalanceUseCase:
    payment_repository: PaymentRepository
    recharge_user_balance_service: RechargeUserBalanceService

    def __init__(
        self,
        payment_repository: PaymentRepository,
        recharge_user_balance_service: RechargeUserBalanceService,
    ) -> None:
        self.payment_repository = payment_repository
        self.recharge_user_balance_service = recharge_user_balance_service

    def execute(self, id: str, status: str) -> Payment:
        payment = self.payment_repository.get(id)
        payment.status = status
        if status == "APPROVED":
            self.recharge_user_balance_service.recharge(payment.user_id, payment.amount)
        return self.payment_repository.update(payment)
