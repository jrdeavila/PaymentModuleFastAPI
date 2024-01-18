from pydantic import BaseModel


class TermsAndConditions(BaseModel):
    token: str
    link: str

    def __init__(self, **data: dict) -> None:
        super().__init__(**data)


class FetchTermsAndConditionsService:
    def fetch(self) -> TermsAndConditions:
        pass


class GetTermsAndConditionsUseCase:
    fetch_terms_and_conditions_service: FetchTermsAndConditionsService

    def __init__(
        self, fetch_terms_and_conditions_service: FetchTermsAndConditionsService
    ) -> None:
        self.fetch_terms_and_conditions_service = fetch_terms_and_conditions_service

    def execute(self) -> TermsAndConditions:
        return self.fetch_terms_and_conditions_service.fetch()
