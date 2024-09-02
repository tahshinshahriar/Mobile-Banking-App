from __future__ import annotations
import Transaction
import BalanceAccount

class SelfTransaction(Transaction.Transaction):
    def __init__(self, master: BalanceAccount.BalanceAccount, amount: float, sender: str="", receiver: str=""):
        super().__init__(master, amount, sender, receiver)