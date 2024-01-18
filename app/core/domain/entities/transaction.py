from core.domain.entities.user import User
from core.domain.entities.payment import (
    BancolombiaPaymentData,
    CreditCardPaymentData,
    DaviplataPaymentData,
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


class DaviplataTransactionPaymentMethod(TransactionPaymentMethod):
    user_legal_id_type: str
    user_legal_id: str

    def __init__(
        self,
        user_legal_id_type: str,
        user_legal_id: str,
    ) -> None:
        super().__init__(payment_description="Payment via Daviplata to Motodomi")
        self.user_legal_id_type = user_legal_id_type
        self.user_legal_id = user_legal_id


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

    if type(payment.payment_data) == DaviplataPaymentData:
        payment_method = DaviplataTransactionPaymentMethod(
            user_legal_id_type=payment.payment_data.dni_type,
            user_legal_id=payment.payment_data.dni_number,
        )

    return Transaction(
        amount=payment.amount,
        customer_email=user.email,
        payment_method=payment_method,
    )
