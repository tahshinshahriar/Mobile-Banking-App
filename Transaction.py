from __future__ import annotations
import random
import datetime
import IDGenerator
import BalanceAccount


class Transaction:
    def __init__(
        self,
        master: BalanceAccount.BalanceAccount,
        amount: float,
        sender: str = "",
        receiver: str = "",
    ):
        self.master = master
        self.sender = sender
        self.receiver = receiver
        self.id = IDGenerator.IDGenerator.generateTransactionID()
        self.amount = amount
        self.dateTime = datetime.datetime.now()
        self.transactionId = random.randint(10000, 99999)

    def __str__(self):
        return f"Transaction ID: {self.transactionId}\nAmount: {self.amount}\nDate and Time: {self.dateTime}"
