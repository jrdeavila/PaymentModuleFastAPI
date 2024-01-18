from core.application.exceptions.message_exception import MessageException
from core.domain.entities.payment import Payment
from core.domain.entities.transaction import transaction_from_payment_and_user
from core.domain.repositories.payment_repository import PaymentRepository
from core.domain.repositories.user_repository import UserRepository
from core.domain.services.send_transaction_service import SendTransactionService


class CreatePaymentUseCase:
    payment_repository: PaymentRepository
    send_transaction_service: SendTransactionService
    user_repository: UserRepository

    def __init__(
        self,
        payment_repository: PaymentRepository,
        user_repository: UserRepository,
        send_transaction_service: SendTransactionService,
    ) -> None:
        self.payment_repository = payment_repository
        self.user_repository = user_repository
        self.send_transaction_service = send_transaction_service

    def execute(self, payment: Payment) -> Payment:
        user = self.user_repository.get(payment.user_id)
        if user is None:
            raise MessageException(
                "User Not Found",
                f"User with id {payment.user_id} not found",
                404,
            )
        transaction = transaction_from_payment_and_user(payment, user)
        transaction_result = self.send_transaction_service.send(transaction)
        payment.id = transaction_result.id
        payment.status = transaction_result.status
        payment.reference = transaction_result.reference
        return self.payment_repository.create(payment)
