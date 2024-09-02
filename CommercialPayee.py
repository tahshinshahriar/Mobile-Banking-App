from __future__ import annotations
import Payee

class CommercialPayee(Payee.Payee):
    def __init__(self, name: str, description: str, accno: int):
        super().__init__(name, description)
        self.accountNo = accno