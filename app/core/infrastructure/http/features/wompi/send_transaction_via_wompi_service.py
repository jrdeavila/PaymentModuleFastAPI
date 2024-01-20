from datetime import datetime
import hashlib
import os
import httpx

from core.application.exceptions.message_exception import MessageException
from core.domain.entities.transaction import (
    BancolombiaTransactionPaymentMethod,
    DaviplataTransactionPaymentMethod,
    NequiTransactionPaymentMethod,
    Transaction,
    TransactionResult,
)
from core.domain.services.send_transaction_service import SendTransactionService
import pytz


def create_wompi_reference() -> str:
    current_date = datetime.now(pytz.timezone("America/Bogota")).strftime(
        "%Y-%m-%d-%H-%M-%S"
    )
    return f"{current_date}"


def create_wompi_signature(
    reference: str, amount_int_cents: int, currency: str = "COP"
) -> str:
    signature_token_env = os.getenv("WOMPI_INTEGRITY_KEY")
    pattern = f"{reference}{amount_int_cents}{currency}{signature_token_env}"
    m = hashlib.sha256()
    m.update(pattern.encode("utf-8"))
    return m.hexdigest()


class WompiTransaction:
    amount_in_cents: int
    currency: str
    customer_email: str
    payment_method: dict

    def __init__(self, **data: dict) -> None:
        self.amount_in_cents = data["amount_in_cents"]
        self.currency = data["currency"]
        self.customer_email = data["customer_email"]
        self.payment_method = data["payment_method"]
        self.reference = create_wompi_reference()

    def to_dict(self) -> dict:
        signature = self.get_signature()
        return {
            "reference": self.reference,
            "amount_in_cents": self.amount_in_cents,
            "currency": self.currency,
            "customer_email": self.customer_email,
            "payment_method": self.payment_method,
            "signature": signature,
        }

    def get_signature(self) -> str:
        return create_wompi_signature(
            self.reference,
            self.amount_in_cents,
            self.currency,
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
            "user_type": "PERSON",
        }
        payment_method.update(vars(transaction.payment_method))

    if type(transaction.payment_method) == DaviplataTransactionPaymentMethod:
        payment_method = {
            "type": "DAVIPLATA",
            "installments": 1,
            "user_type": "PERSON",
        }
        payment_method.update(vars(transaction.payment_method))

    return WompiTransaction(
        amount_in_cents=transaction.amount * 100,
        currency="COP",
        customer_email=transaction.customer_email,
        payment_method=payment_method,
    )


class SendTransactionViaWompiService(SendTransactionService):
    public_key: str
    private_key: str
    environment: str

    def __init__(self, private_key: str, public_key: str, environment: str) -> None:
        self.private_key = private_key
        self.public_key = public_key
        self.environment = environment

    def _get_acceptance_token(self) -> str:
        res = httpx.get(
            f"https://{self.environment}.wompi.co/v1/merchants/{self.public_key}",
            headers={
                "Accept": "application/json",
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.private_key}",
            },
            timeout=10,
        )

        acceptance_token: str = res.json()["data"]["presigned_acceptance"][
            "acceptance_token"
        ]
        return acceptance_token

    def _check_status_code(self, res: httpx.Response) -> None:
        print(res.status_code)
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
        if res.status_code != 201 and res.status_code != 200:
            raise MessageException(
                "Wompi Unknown Error",
                res.json(),
            )

    def send(self, transaction: Transaction) -> TransactionResult:
        try:
            wompi_transaction = transaction_to_wompi_transaction(transaction)

            acceptance_token = self._get_acceptance_token()

            data = {
                "acceptance_token": acceptance_token,
            }
            data.update(wompi_transaction.to_dict())

            res = httpx.post(
                f"https://{self.environment}.wompi.co/v1/transactions",
                headers={
                    "Accept": "application/json",
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {self.private_key}",
                },
                json=data,
                timeout=10,
            )

            self._check_status_code(res)

            return TransactionResult(
                id=res.json()["data"]["id"],
                status=res.json()["data"]["status"],
                reference=res.json()["data"]["reference"],
            )
        except httpx.ConnectTimeout:
            raise MessageException(
                "Wompi Timeout Error",
                "Wompi is not responding",
            )
