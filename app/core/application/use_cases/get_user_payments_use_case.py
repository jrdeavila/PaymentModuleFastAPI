from core.application.exceptions.message_exception import MessageException
from core.domain.entities.payment import Payment
from core.domain.repositories.user_repository import UserRepository
from core.domain.services.fetch_user_payments_service import FetchUserPaymentsService


class GetUserPaymentsUseCase:
    fetch_user_payments_service: FetchUserPaymentsService
    user_repository: UserRepository

    def __init__(
        self,
        fetch_user_payments_service: FetchUserPaymentsService,
        user_repository: UserRepository,
    ) -> None:
        self.fetch_user_payments_service = fetch_user_payments_service
        self.user_repository = user_repository

    def get(self, user_id: str) -> list[Payment]:
        user = self.user_repository.get(user_id)
        if not user:
            raise MessageException(
                name="User not found",
                message=f"User with id {user_id} not found",
                code=404,
            )
        return self.fetch_user_payments_service.fetch(user_id)
