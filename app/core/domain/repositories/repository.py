from core.domain.entities.entity import AppEntity


class AppRepository:
    _entity: type[AppEntity]

    def __init__(self, entity) -> None:
        self._entity = entity

    def get(self, id: str) -> AppEntity:
        pass

    def get_all(self) -> list[AppEntity]:
        pass

    def create(self, entity: AppEntity) -> AppEntity:
        pass

    def update(self, entity: AppEntity) -> AppEntity:
        pass

    def delete(self, id: str) -> None:
        pass
