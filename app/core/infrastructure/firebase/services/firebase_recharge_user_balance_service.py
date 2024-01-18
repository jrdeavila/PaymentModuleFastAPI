from core.domain.services.recharge_user_balance_service import (
    RechargeUserBalanceService,
)


class FirebaseRechargeUserBalanceService(RechargeUserBalanceService):
    firestore_db: any

    def __init__(self, firestore_db: any) -> None:
        self.firestore_db = firestore_db

    def recharge(self, user_id: str, amount: int) -> None:
        user_ref = self.firestore_db.collection("delivery_men").document(user_id)
        if user_ref.get().exists:
            user_data = user_ref.get().to_dict()
            user_balance = user_data["balance"] if "balance" in user_data else 0
            amount = user_balance + amount

        user_ref.update({"balance": amount})
        return
