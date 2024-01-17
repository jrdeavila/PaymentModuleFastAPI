from pydantic import BaseModel, Field

from core.domain.entities.payment import NequiPaymentData, Payment


class CreatePaymentRequest(BaseModel):
    amount: int = Field(default=1500, ge=1499, description="Amount of payment")
    payment_type: str = Field(
        default="Nequi",
        description="Type of payment",
        example="Nequi",
        pattern="Nequi|Bancolombia|CreditCard",
    )
    payment_data: dict = Field(
        description="Data of payment",
        examples=[
            {
                "number_phone": "3000000000",
            },
            {
                "account_number": "1234567890",
            },
            {
                "owner_name": "John Doe",
                "number_card": "1234567890123456",
                "cvv": "123",
                "expiration_date": "12/2025",
            },
        ],
    )
    user_id: str = Field(description="User identifier")

    def to_payment(self) -> Payment:
        payment_data = None

        if self.payment_type == "Nequi":
            payment_data = NequiPaymentData(
                number_phone=self.payment_data["number_phone"]
            )
        elif self.payment_type == "Bancolombia":
            payment_data = NequiPaymentData(
                account_number=self.payment_data["account_number"]
            )
        elif self.payment_type == "CreditCard":
            payment_data = NequiPaymentData(
                owner_name=self.payment_data["owner_name"],
                number_card=self.payment_data["number_card"],
                cvv=self.payment_data["cvv"],
                expiration_date=self.payment_data["expiration_date"],
            )
        payment = Payment(
            amount=self.amount,
            user_id=self.user_id,
            payment_data=payment_data,
        )
        return payment
