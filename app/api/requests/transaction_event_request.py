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
class Transaction:
    id: str
    status: str
    reference: str

    @staticmethod
    def from_dict(obj: Any) -> "Transaction":
        assert isinstance(obj, dict)
        id = from_str(obj.get("id"))
        status = from_str(obj.get("status"))
        reference = from_str(obj.get("reference"))

        return Transaction(
            id,
            status,
            reference,
        )

    def to_dict(self) -> dict:
        result: dict = {}
        result["id"] = from_str(self.id)
        result["status"] = from_str(self.status)
        result["reference"] = from_str(self.reference)

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
class TransactionEventRequest:
    data: Data

    @staticmethod
    def from_dict(obj: Any) -> "TransactionEventRequest":
        assert isinstance(obj, dict)
        data = Data.from_dict(obj.get("data"))
        return TransactionEventRequest(
            data,
        )

    def to_dict(self) -> dict:
        result: dict = {}
        result["data"] = to_class(Data, self.data)
        return result


def wompi_transaction_event_from_dict(s: Any) -> TransactionEventRequest:
    return TransactionEventRequest.from_dict(s)


def wompi_transaction_event_to_dict(x: TransactionEventRequest) -> Any:
    return to_class(TransactionEventRequest, x)
