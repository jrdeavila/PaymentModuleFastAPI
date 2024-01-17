from core.domain.entities.entity import AppEntity


class User(AppEntity):
    uuid: str
    email: str
    name: str
    phone: str

    def __init__(self, **data) -> None:
        super().__init__(**data)


def user_from_dict(data: dict) -> User:
    user = User(
        uuid=data["uuid"], email=data["email"], name=data["name"], phone=data["phone"]
    )
    return user
