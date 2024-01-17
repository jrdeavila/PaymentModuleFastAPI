from core.infrastructure.firebase.repositories.firebase_user_repository import (
    FirebaseUserRepository,
)
from core.domain.repositories.user_repository import UserRepository
from core.domain.repositories.payment_repository import PaymentRepository
from core.infrastructure.firebase.repositories.firebase_payment_repository import (
    FirebasePaymentRepository,
)
from core.infrastructure.injection.inject_firestore import inject_firestore


def inject_payment_repository() -> PaymentRepository:
    return FirebasePaymentRepository(inject_firestore())


def inject_user_repository() -> UserRepository:
    return FirebaseUserRepository(inject_firestore())
