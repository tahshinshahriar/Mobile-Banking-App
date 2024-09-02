from __future__ import annotations
import Transaction

class Purchase(Transaction.Transaction):
    def __init__(self, amount: float, name: str, location: str="", sender: str=""):
        super().__init__(amount, sender, location)
        self.name = name
        self.location = location