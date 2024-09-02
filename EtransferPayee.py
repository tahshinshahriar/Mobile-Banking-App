from __future__ import annotations
import Payee

class EtransferPayee(Payee.Payee):
    def __init__(self, name: str, description: str, email: str=None, phone: str=None):
        super().__init__(name, description)
        self.email = email
        self.phone = phone