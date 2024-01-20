from core.domain.entities.payment import Payment, payment_from_dict
from core.domain.services.fetch_user_payments_service import FetchUserPaymentsService
from google.cloud.firestore_v1.base_query import FieldFilter


class FirebaseFetchUserPaymentsService(FetchUserPaymentsService):
    firestore_db: any

    def __init__(self, firestore_db: any):
        self.firestore_db = firestore_db

    def fetch(self, user_id: str) -> list[Payment]:
        payments = []
        for snapshot in (
            self.firestore_db.collection("payments")
            .where(filter=FieldFilter("user_id", "==", user_id))
            .get()
        ):
            payment = payment_from_dict(snapshot.to_dict())
            payments.append(payment)
        return payments
