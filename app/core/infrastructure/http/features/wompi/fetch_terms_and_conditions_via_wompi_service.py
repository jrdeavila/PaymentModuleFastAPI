import httpx

from core.application.use_cases.get_terms_and_conditions_use_case import (
    FetchTermsAndConditionsService,
    TermsAndConditions,
)
from core.infrastructure.http.features.wompi.models import (
    wompi_presigned_acceptance_from_dict,
    wompi_presigned_acceptances_to_tems_and_conditions,
)


class FetchTermsAndConditionsViaWompiService(FetchTermsAndConditionsService):
    public_key: str
    private_key: str
    environtment: str

    def __init__(self, public_key: str, private_key: str, environtment: str) -> None:
        self.public_key = public_key
        self.private_key = private_key
        self.environtment = environtment

    def fetch(self) -> TermsAndConditions:
        res = httpx.get(
            f"https://{self.environtment}.wompi.co/v1/merchants/{self.public_key}",
            headers={
                "Accept": "application/json",
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.private_key}",
            },
        )
        print(res.json()["data"])
        wompi_presigned_acceptance = wompi_presigned_acceptance_from_dict(
            res.json()["data"]
        )

        return wompi_presigned_acceptances_to_tems_and_conditions(
            wompi_presigned_acceptance
        )
