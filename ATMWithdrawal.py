from __future__ import annotations
import IDGenerator
import Transaction
import BalanceAccount


class ATMWithdrawal(Transaction.Transaction):
    def __init__(
        self,
        master: BalanceAccount.BalanceAccount,
        amount: float,
        bank: str = "T Bank",
        sender: str = "",
        receiver: str = "",
    ):
        super().__init__(master, amount, sender, receiver)
        self.ATMID = IDGenerator.IDGenerator.generateAtmID()
        self.bank = bank
