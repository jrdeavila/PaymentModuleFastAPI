from core.domain.entities.payment import Payment, payment_from_dict
from core.domain.repositories.payment_repository import PaymentRepository


class FirebasePaymentRepository(PaymentRepository):
    firestore_db: any

    def __init__(self, firestore_db: any) -> None:
        super().__init__()
        self.firestore_db = firestore_db

    def create(self, entity: Payment) -> Payment:
        document = self.firestore_db.collection("payments").document(entity.id)
        if document.get().exists:
            raise Exception("Payment already exists")
        else:
            document.set(entity.to_dict())

        return entity

    def get(self, id: str) -> Payment:
        snapshot = self.firestore_db.collection("payments").document(id).get()
        payment = payment_from_dict(snapshot.to_dict())
        return payment

    def get_all(self) -> list[Payment]:
        payments = []
        for snapshot in self.firestore_db.collection("payments").get():
            payment = payment_from_dict(snapshot.to_dict())
            payments.append(payment)
        return payments

    def update(self, entity: Payment) -> Payment:
        document = self.firestore_db.collection("payments").document(entity.id)
        if document.get().exists:
            document.update(entity.to_dict())
        else:
            raise Exception("Payment not found")
        return entity

    def delete(self, id: str) -> None:
        self.firestore_db.collection("payments").document(id).delete()
        return id
