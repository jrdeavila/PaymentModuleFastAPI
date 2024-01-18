from dataclasses import dataclass
from typing import Any, Type, TypeVar, cast

from core.application.use_cases.get_terms_and_conditions_use_case import (
    TermsAndConditions,
)


T = TypeVar("T")


def from_str(x: Any) -> str:
    assert isinstance(x, str)
    return x


def to_class(c: Type[T], x: Any) -> dict:
    assert isinstance(x, c)
    return cast(Any, x).to_dict()


@dataclass
class PresignedAcceptance:
    acceptance_token: str
    permalink: str
    type: str

    @staticmethod
    def from_dict(obj: Any) -> "PresignedAcceptance":
        assert isinstance(obj, dict)
        acceptance_token = from_str(obj.get("acceptance_token"))
        permalink = from_str(obj.get("permalink"))
        type = from_str(obj.get("type"))
        return PresignedAcceptance(acceptance_token, permalink, type)

    def to_dict(self) -> dict:
        result: dict = {}
        result["acceptance_token"] = from_str(self.acceptance_token)
        result["permalink"] = from_str(self.permalink)
        result["type"] = from_str(self.type)
        return result


@dataclass
class WompiPresignedAcceptance:
    presigned_acceptance: PresignedAcceptance

    @staticmethod
    def from_dict(obj: Any) -> "WompiPresignedAcceptance":
        assert isinstance(obj, dict)
        presigned_acceptance = PresignedAcceptance.from_dict(
            obj.get("presigned_acceptance")
        )
        return WompiPresignedAcceptance(presigned_acceptance)

    def to_dict(self) -> dict:
        result: dict = {}
        result["presigned_acceptance"] = to_class(
            PresignedAcceptance, self.presigned_acceptance
        )
        return result


def wompi_presigned_acceptance_from_dict(s: Any) -> WompiPresignedAcceptance:
    return WompiPresignedAcceptance.from_dict(s)


def wompi_presigned_acceptance_to_dict(x: WompiPresignedAcceptance) -> Any:
    return to_class(WompiPresignedAcceptance, x)


def wompi_presigned_acceptances_from_dict(data: dict) -> WompiPresignedAcceptance:
    return WompiPresignedAcceptance(**data["presigned_acceptance"])


def wompi_presigned_acceptances_to_tems_and_conditions(
    WompiPresignedAcceptance,
) -> TermsAndConditions:
    return TermsAndConditions(
        token=WompiPresignedAcceptance.presigned_acceptance.acceptance_token,
        link=WompiPresignedAcceptance.presigned_acceptance.permalink,
    )
