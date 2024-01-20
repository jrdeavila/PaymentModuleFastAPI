from fastapi import APIRouter, Depends

from core.application.use_cases.get_terms_and_conditions_use_case import (
    GetTermsAndConditionsUseCase,
    TermsAndConditions,
)
from core.infrastructure.injection.inject_use_cases import (
    inject_get_terms_and_conditions_use_case,
)


class TermsAndConditionController:
    router = APIRouter()

    @router.get("/")
    async def get_terms_and_conditions(
        terms_and_conditions_use_case: GetTermsAndConditionsUseCase = Depends(
            inject_get_terms_and_conditions_use_case
        ),
    ) -> TermsAndConditions:
        return terms_and_conditions_use_case.execute()
