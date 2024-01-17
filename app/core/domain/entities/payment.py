from typing import Union
from pydantic import BaseModel
from core.domain.entities.entity import AppEntity


class _PaymentData(AppEntity):
    payment_type: str

    def __init__(self, **data: dict) -> None:
        super().__init__(**data)


class NequiPaymentData(_PaymentData):
    number_phone: str
    payment_type: str = "Nequi"

    def __init__(self, **data: dict) -> None:
        super().__init__(**data)


class BancolombiaPaymentData(_PaymentData):
    account_number: str
    payment_type: str = "Bancolombia"

    def __init__(self, **data: dict) -> None:
        super().__init__(**data)


class CreditCardPaymentData(_PaymentData):
    owner_name: str
    number_card: str
    cvv: str
    expiration_date: str
    payment_type: str = "CreditCard"

    def __init__(self, **data: dict) -> None:
        super().__init__(**data)


class Payment(AppEntity):
    id: str = None
    amount: int
    user_id: str
    payment_data: Union[_PaymentData, None] = None

    def __init__(self, **data: dict) -> None:
        super().__init__(**data)


def payment_from_dict(data: dict) -> Payment:
    payment = Payment(data["amount"], data["user_id"])
    if data["payment_data"]["payment_type"] == "Nequi":
        payment.payment_data = NequiPaymentData(data["payment_data"]["number_phone"])
    elif data["payment_data"]["payment_type"] == "Bancolombia":
        payment.payment_data = BancolombiaPaymentData(
            data["payment_data"]["account_number"]
        )
    elif data["payment_data"]["payment_type"] == "CreditCard":
        payment.payment_data = CreditCardPaymentData(
            data["payment_data"]["owner_name"],
            data["payment_data"]["number_card"],
            data["payment_data"]["cvv"],
            data["payment_data"]["expiration_date"],
        )
    return payment
