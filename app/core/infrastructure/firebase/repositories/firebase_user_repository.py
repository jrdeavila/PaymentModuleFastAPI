from core.domain.entities.user import User, user_from_dict
from core.domain.repositories.user_repository import UserRepository


class FirebaseUserRepository(UserRepository):
    firestore_db: any

    def __init__(self, firebase_db: any) -> None:
        self.firestore_db = firebase_db

    def get(self, id: str) -> User:
        snapshot = self.firestore_db.collection("users").document(id).get()
        if not snapshot.exists:
            return None
        user = user_from_dict(snapshot.to_dict())
        return user
