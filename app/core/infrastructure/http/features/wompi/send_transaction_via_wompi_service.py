from datetime import datetime
import hashlib
import os
import httpx

from core.application.exceptions.message_exception import MessageException
from core.domain.entities.transaction import (
    BancolombiaTransactionPaymentMethod,
    CreditCardTransactionPaymentMethod,
    NequiTransactionPaymentMethod,
    Transaction,
    TransactionResult,
)
from core.domain.services.send_transaction_service import SendTransactionService


def create_wompi_reference(customer_email: str, amount_in_cents: int) -> str:
    app_name = os.getenv("APP_NAME")
    current_date = datetime.now().strftime("%Y%m%d%H%M%S")
    return f"{app_name}{customer_email}{amount_in_cents}{current_date}"


def create_wompi_signature(reference: str, amount_int_cents: int) -> str:
    signature_token_env = os.getenv("WOMPI_SIGNATURE_KEY")
    pattern = f"${reference}{amount_int_cents}COP{signature_token_env}"
    signature = hashlib.sha256(pattern.encode("utf-8")).hexdigest()
    return signature


class WompiTransaction:
    amount_in_cents: int
    currency: str
    customer_email: str
    payment_method: dict
    reference: str = None

    def __init__(self, **data: dict) -> None:
        self.amount_in_cents = data["amount_in_cents"]
        self.currency = data["currency"]
        self.customer_email = data["customer_email"]
        self.payment_method = data["payment_method"]
        self.reference = create_wompi_reference(
            self.customer_email, self.amount_in_cents
        )

    def to_dict(self) -> dict:
        return {
            "reference": self.reference,
            "amount_in_cents": self.amount_in_cents,
            "currency": self.currency,
            "customer_email": self.customer_email,
            "payment_method": self.payment_method,
        }

    def get_signature(self) -> str:
        return create_wompi_signature(
            self.reference,
            self.amount_in_cents,
        )


def transaction_to_wompi_transaction(transaction: Transaction) -> WompiTransaction:
    payment_method: dict = None
    if type(transaction.payment_method) == NequiTransactionPaymentMethod:
        payment_method = {
            "type": "NEQUI",
        }
        payment_method.update(vars(transaction.payment_method))

    if type(transaction.payment_method) == BancolombiaTransactionPaymentMethod:
        payment_method = {
            "type": "BANCOLOMBIA_TRANSFER",
        }
        payment_method.update(vars(transaction.payment_method))

    if type(transaction.payment_method) == CreditCardTransactionPaymentMethod:
        payment_method = {
            "type": "CREDIT_CARD",
        }
        payment_method.update(vars(transaction.payment_method))

    return WompiTransaction(
        amount_in_cents=transaction.amount * 100,
        currency="COP",
        customer_email=transaction.customer_email,
        payment_method=payment_method,
    )


class SendTransactionViaWompiService(SendTransactionService):
    token: str
    environment: str

    def __init__(self, token: str, environment: str) -> None:
        self.token = token
        self.environment = environment

    def send(self, transaction: Transaction) -> TransactionResult:
        wompi_transaction = transaction_to_wompi_transaction(transaction)
        print(wompi_transaction.to_dict())
        res = httpx.post(
            f"https://{self.environment}.wompi.co/v1/transactions",
            headers={
                "Accept": "application/json",
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.token}",
            },
            json=wompi_transaction.to_dict(),
        )

        if res.status_code == 401:
            raise MessageException(
                "Wompi Authorization Error",
                res.json()["error"]["reason"],
            )
        if res.status_code == 400:
            raise MessageException(
                "Wompi Bad Request Error",
                res.json()["error"]["reason"],
            )
        if res.status_code == 500:
            raise MessageException(
                "Wompi Server Error",
                res.json()["error"]["reason"],
            )
        if res.status_code == 422:
            raise MessageException(
                "Wompi Unprocessable Entity Error",
                res.json()["error"]["messages"],
            )
        if res.status_code != 200:
            raise MessageException(
                "Wompi Unknown Error",
                res.json(),
            )

        return res.json()
