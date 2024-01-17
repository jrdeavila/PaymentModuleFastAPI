from core.domain.entities.user import User
from core.domain.repositories.repository import AppRepository


class UserRepository(AppRepository):
    def __init__(self) -> None:
        super().__init__(User)

    def get(self, id: str) -> User:
        return super().get(id)
