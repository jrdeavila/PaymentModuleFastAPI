from core.domain.services.recharge_user_balance_service import (
    RechargeUserBalanceService,
)
from core.infrastructure.firebase.services.firebase_recharge_user_balance_service import (
    FirebaseRechargeUserBalanceService,
)
from core.infrastructure.injection.inject_firestore import inject_firestore


def inject_recharge_user_balance_service() -> RechargeUserBalanceService:
    return FirebaseRechargeUserBalanceService(
        firestore_db=inject_firestore(),
    )
