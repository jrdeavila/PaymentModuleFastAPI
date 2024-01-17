from core.domain.entities.payment import Payment
from core.domain.repositories.repository import AppRepository


class PaymentRepository(AppRepository):
    def __init__(self):
        super().__init__(Payment)

    def create(self, entity: Payment) -> Payment:
        return super().create(entity)

    def get(self, id: str) -> Payment:
        return super().get(id)

    def get_all(self) -> list[Payment]:
        return super().get_all()

    def update(self, entity: Payment) -> None:
        return super().update(entity)
