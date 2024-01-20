from core.domain.services.fetch_user_payments_service import FetchUserPaymentsService
from core.infrastructure.firebase.services.firebase_fetch_user_payments_service import (
    FirebaseFetchUserPaymentsService,
)
from core.infrastructure.injection.inject_firestore import inject_firestore


def inject_fetch_user_payments_service() -> FetchUserPaymentsService:
    return FirebaseFetchUserPaymentsService(
        firestore_db=inject_firestore(),
    )
