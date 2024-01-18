import os
from core.application.use_cases.get_terms_and_conditions_use_case import (
    FetchTermsAndConditionsService,
)

from core.infrastructure.http.features.wompi.fetch_terms_and_conditions_via_wompi_service import (
    FetchTermsAndConditionsViaWompiService,
)


def inject_fetch_terms_and_conditions_service() -> FetchTermsAndConditionsService:
    return FetchTermsAndConditionsViaWompiService(
        public_key=os.getenv("WOMPI_PUBLIC_KEY"),
        private_key=os.getenv("WOMPI_PRIVATE_KEY"),
        environtment=os.getenv("WOMPI_ENV"),
    )
