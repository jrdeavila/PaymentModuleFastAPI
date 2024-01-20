from core.domain.entities.payment import Payment


class FetchUserPaymentsService:
    def fetch(self, user_id: str) -> list[Payment]:
        pass
