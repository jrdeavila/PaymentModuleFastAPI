from typing import Union
from pydantic import BaseModel
from core.domain.entities.entity import AppEntity


class _PaymentData(AppEntity):
    payment_type: str

    def __init__(self, **data: dict) -> None:
        super().__init__(**data)

    def to_dict(self) -> dict:
        return {
            "payment_type": self.payment_type,
        }


class NequiPaymentData(_PaymentData):
    number_phone: str
    payment_type: str = "Nequi"

    def __init__(self, **data: dict) -> None:
        super().__init__(**data)

    def to_dict(self) -> dict:
        return {
            "payment_type": self.payment_type,
            "number_phone": self.number_phone,
        }


class BancolombiaPaymentData(_PaymentData):
    account_number: str
    payment_type: str = "Bancolombia"

    def __init__(self, **data: dict) -> None:
        super().__init__(**data)

    def to_dict(self) -> dict:
        return {
            "payment_type": self.payment_type,
            "account_number": self.account_number,
        }


class CreditCardPaymentData(_PaymentData):
    owner_name: str
    number_card: str
    cvv: str
    expiration_date: str
    payment_type: str = "CreditCard"

    def __init__(self, **data: dict) -> None:
        super().__init__(**data)

    def to_dict(self) -> dict:
        return {
            "payment_type": self.payment_type,
            "owner_name": self.owner_name,
            "number_card": self.number_card,
            "cvv": self.cvv,
            "expiration_date": self.expiration_date,
        }


class Payment(AppEntity):
    id: Union[str, None] = None
    reference: Union[str, None] = None
    amount: int
    user_id: str
    status: str = "CREATED"
    payment_data: Union[_PaymentData, None] = None

    def __init__(self, **data: dict) -> None:
        super().__init__(**data)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "reference": self.reference,
            "amount": self.amount,
            "user_id": self.user_id,
            "status": self.status,
            "payment_data": self.payment_data.to_dict(),
        }


def payment_from_dict(data: dict) -> Payment:
    payment_data: Union[_PaymentData, None] = None

    if data["payment_data"]["payment_type"] == "Nequi":
        payment_data = NequiPaymentData(
            number_phone=data["payment_data"]["number_phone"],
            type=data["payment_data"]["payment_type"],
        )
    elif data["payment_data"]["payment_type"] == "Bancolombia":
        payment_data = BancolombiaPaymentData(
            account_number=data["payment_data"]["account_number"],
            type=data["payment_data"]["payment_type"],
        )
    elif data["payment_data"]["payment_type"] == "CreditCard":
        payment_data = CreditCardPaymentData(
            owner_name=data["payment_data"]["owner_name"],
            number_card=data["payment_data"]["number_card"],
            cvv=data["payment_data"]["cvv"],
            expiration_date=data["payment_data"]["expiration_date"],
            type=data["payment_data"]["payment_type"],
        )
    payment = Payment(
        id=data["id"],
        amount=data["amount"],
        user_id=data["user_id"],
        status=data["status"],
        reference=data["reference"],
        payment_data=payment_data,
    )
    return payment
