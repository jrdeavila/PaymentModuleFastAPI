from dataclasses import dataclass
from typing import Any, List, TypeVar, Type, cast, Callable


T = TypeVar("T")


def from_bool(x: Any) -> bool:
    assert isinstance(x, bool)
    return x


def from_str(x: Any) -> str:
    assert isinstance(x, str)
    return x


def to_class(c: Type[T], x: Any) -> dict:
    assert isinstance(x, c)
    return cast(Any, x).to_dict()


def from_none(x: Any) -> Any:
    assert x is None
    return x


def from_int(x: Any) -> int:
    assert isinstance(x, int) and not isinstance(x, bool)
    return x


def from_list(f: Callable[[Any], T], x: Any) -> List[T]:
    assert isinstance(x, list)
    return [f(y) for y in x]


@dataclass
class Extra:
    is_three_ds: bool
    transfer_voucher: str
    async_payment_url: str
    external_identifier: str

    @staticmethod
    def from_dict(obj: Any) -> "Extra":
        assert isinstance(obj, dict)
        is_three_ds = from_bool(obj.get("is_three_ds"))
        transfer_voucher = from_str(obj.get("transfer_voucher"))
        async_payment_url = from_str(obj.get("async_payment_url"))
        external_identifier = from_str(obj.get("external_identifier"))
        return Extra(
            is_three_ds, transfer_voucher, async_payment_url, external_identifier
        )

    def to_dict(self) -> dict:
        result: dict = {}
        result["is_three_ds"] = from_bool(self.is_three_ds)
        result["transfer_voucher"] = from_str(self.transfer_voucher)
        result["async_payment_url"] = from_str(self.async_payment_url)
        result["external_identifier"] = from_str(self.external_identifier)
        return result


@dataclass
class PaymentMethod:
    type: str
    extra: Extra
    user_type: str
    payment_description: str

    @staticmethod
    def from_dict(obj: Any) -> "PaymentMethod":
        assert isinstance(obj, dict)
        type = from_str(obj.get("type"))
        extra = Extra.from_dict(obj.get("extra"))
        user_type = from_str(obj.get("user_type"))
        payment_description = from_str(obj.get("payment_description"))
        return PaymentMethod(type, extra, user_type, payment_description)

    def to_dict(self) -> dict:
        result: dict = {}
        result["type"] = from_str(self.type)
        result["extra"] = to_class(Extra, self.extra)
        result["user_type"] = from_str(self.user_type)
        result["payment_description"] = from_str(self.payment_description)
        return result


@dataclass
class Transaction:
    id: str
    status: str
    currency: str
    reference: str
    created_at: str
    billing_data: None
    finalized_at: str
    redirect_url: None
    customer_data: None
    customer_email: str
    payment_method: PaymentMethod
    status_message: str
    amount_in_cents: int
    payment_link_id: None
    shipping_address: None
    payment_source_id: None
    payment_method_type: str

    @staticmethod
    def from_dict(obj: Any) -> "Transaction":
        assert isinstance(obj, dict)
        id = from_str(obj.get("id"))
        status = from_str(obj.get("status"))
        currency = from_str(obj.get("currency"))
        reference = from_str(obj.get("reference"))
        created_at = from_str(obj.get("created_at"))
        billing_data = from_none(obj.get("billing_data"))
        finalized_at = from_str(obj.get("finalized_at"))
        redirect_url = from_none(obj.get("redirect_url"))
        customer_data = from_none(obj.get("customer_data"))
        customer_email = from_str(obj.get("customer_email"))
        payment_method = PaymentMethod.from_dict(obj.get("payment_method"))
        status_message = from_str(obj.get("status_message"))
        amount_in_cents = from_int(obj.get("amount_in_cents"))
        payment_link_id = from_none(obj.get("payment_link_id"))
        shipping_address = from_none(obj.get("shipping_address"))
        payment_source_id = from_none(obj.get("payment_source_id"))
        payment_method_type = from_str(obj.get("payment_method_type"))
        return Transaction(
            id,
            status,
            currency,
            reference,
            created_at,
            billing_data,
            finalized_at,
            redirect_url,
            customer_data,
            customer_email,
            payment_method,
            status_message,
            amount_in_cents,
            payment_link_id,
            shipping_address,
            payment_source_id,
            payment_method_type,
        )

    def to_dict(self) -> dict:
        result: dict = {}
        result["id"] = from_str(self.id)
        result["status"] = from_str(self.status)
        result["currency"] = from_str(self.currency)
        result["reference"] = from_str(self.reference)
        result["created_at"] = from_str(self.created_at)
        result["billing_data"] = from_none(self.billing_data)
        result["finalized_at"] = from_str(self.finalized_at)
        result["redirect_url"] = from_none(self.redirect_url)
        result["customer_data"] = from_none(self.customer_data)
        result["customer_email"] = from_str(self.customer_email)
        result["payment_method"] = to_class(PaymentMethod, self.payment_method)
        result["status_message"] = from_str(self.status_message)
        result["amount_in_cents"] = from_int(self.amount_in_cents)
        result["payment_link_id"] = from_none(self.payment_link_id)
        result["shipping_address"] = from_none(self.shipping_address)
        result["payment_source_id"] = from_none(self.payment_source_id)
        result["payment_method_type"] = from_str(self.payment_method_type)
        return result


@dataclass
class Data:
    transaction: Transaction

    @staticmethod
    def from_dict(obj: Any) -> "Data":
        assert isinstance(obj, dict)
        transaction = Transaction.from_dict(obj.get("transaction"))
        return Data(transaction)

    def to_dict(self) -> dict:
        result: dict = {}
        result["transaction"] = to_class(Transaction, self.transaction)
        return result


@dataclass
class Signature:
    checksum: str
    properties: List[str]

    @staticmethod
    def from_dict(obj: Any) -> "Signature":
        assert isinstance(obj, dict)
        checksum = from_str(obj.get("checksum"))
        properties = from_list(from_str, obj.get("properties"))
        return Signature(checksum, properties)

    def to_dict(self) -> dict:
        result: dict = {}
        result["checksum"] = from_str(self.checksum)
        result["properties"] = from_list(from_str, self.properties)
        return result


@dataclass
class TransactionEventRequest:
    data: Data
    event: str
    sent_at: str
    signature: Signature
    timestamp: int
    environment: str

    @staticmethod
    def from_dict(obj: Any) -> "TransactionEventRequest":
        assert isinstance(obj, dict)
        data = Data.from_dict(obj.get("data"))
        event = from_str(obj.get("event"))
        sent_at = from_str(obj.get("sent_at"))
        signature = Signature.from_dict(obj.get("signature"))
        timestamp = from_int(obj.get("timestamp"))
        environment = from_str(obj.get("environment"))
        return TransactionEventRequest(
            data, event, sent_at, signature, timestamp, environment
        )

    def to_dict(self) -> dict:
        result: dict = {}
        result["data"] = to_class(Data, self.data)
        result["event"] = from_str(self.event)
        result["sent_at"] = from_str(self.sent_at)
        result["signature"] = to_class(Signature, self.signature)
        result["timestamp"] = from_int(self.timestamp)
        result["environment"] = from_str(self.environment)
        return result


def wompi_transaction_event_from_dict(s: Any) -> TransactionEventRequest:
    return TransactionEventRequest.from_dict(s)


def wompi_transaction_event_to_dict(x: TransactionEventRequest) -> Any:
    return to_class(TransactionEventRequest, x)
