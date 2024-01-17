from core.domain.entities.transaction import Transaction, TransactionResult


class SendTransactionService:
    async def send(transaction: Transaction) -> TransactionResult:
        pass
