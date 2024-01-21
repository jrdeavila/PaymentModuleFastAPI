from typing import Union
from core.domain.entities.entity import AppEntity


class Application(AppEntity):
    id: Union[str, None] = None
    username: str
    email: str
    name: str = None
    disabled: bool = None

    def __init__(self, **data) -> None:
        super().__init__(**data)
