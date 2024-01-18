from core.domain.entities.user import User
from core.domain.entities.payment import (
    BancolombiaPaymentData,
    CreditCardPaymentData,
    NequiPaymentData,
    Payment,
)


class TransactionPaymentMethod:
    payment_description: str

    def __init__(self, payment_description: str) -> None:
        self.payment_description = payment_description


class NequiTransactionPaymentMethod(TransactionPaymentMethod):
    phone_number: str

    def __init__(self, number_phone: str) -> None:
        super().__init__(payment_description="Payment via Nequi to Motodomi")
        self.phone_number = number_phone


class BancolombiaTransactionPaymentMethod(TransactionPaymentMethod):
    account_number: str

    def __init__(self, account_number: str) -> None:
        super().__init__(payment_description="Payment via Bancolombia to Motodomi")
        self.account_number = account_number


class CreditCardTransactionPaymentMethod(TransactionPaymentMethod):
    owner_name: str
    number_card: str
    cvv: str
    expiration_date: str

    def __init__(
        self,
        owner_name: str,
        number_card: str,
        cvv: str,
        expiration_date: str,
    ) -> None:
        super().__init__(payment_description="Payment via CreditCard to Motodomi")
        self.owner_name = owner_name
        self.number_card = number_card
        self.cvv = cvv
        self.expiration_date = expiration_date


class Transaction:
    amount: int
    customer_email: str
    payment_method: TransactionPaymentMethod

    def __init__(
        self, amount: int, customer_email: str, payment_method: TransactionPaymentMethod
    ) -> None:
        self.amount = amount
        self.customer_email = customer_email
        self.payment_method = payment_method


class TransactionResult:
    id: str
    status: str
    reference: str

    def __init__(self, id: str, status: str, reference: str) -> None:
        self.id = id
        self.status = status
        self.reference = reference


def transaction_from_payment_and_user(payment: Payment, user: User) -> Transaction:
    payment_method: TransactionPaymentMethod = None
    if type(payment.payment_data) == NequiPaymentData:
        payment_method = NequiTransactionPaymentMethod(
            number_phone=payment.payment_data.number_phone
        )
    if type(payment.payment_data) == BancolombiaPaymentData:
        payment_method = BancolombiaTransactionPaymentMethod(
            account_number=payment.payment_data.account_number
        )

    if type(payment.payment_data) == CreditCardPaymentData:
        payment_method = CreditCardTransactionPaymentMethod(
            owner_name=payment.payment_data.owner_name,
            number_card=payment.payment_data.number_card,
            cvv=payment.payment_data.cvv,
            expiration_date=payment.payment_data.expiration_date,
        )

    return Transaction(
        amount=payment.amount,
        customer_email=user.email,
        payment_method=payment_method,
    )
