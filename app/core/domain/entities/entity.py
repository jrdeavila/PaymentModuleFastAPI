from pydantic import BaseModel


class AppEntity(BaseModel):
    def __init__(self, **data: dict) -> None:
        super().__init__(**data)
