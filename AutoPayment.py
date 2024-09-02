from __future__ import annotations
import datetime
import Payee

class AutoPayment:
    def __init__(self, payee: Payee.Payee, paymentRate: datetime.timedelta, amount: int):
        self.payee = payee
        self.paymentRate = paymentRate
        self.amount = amount

    def changeAmount(self, newAmount: int):
        if newAmount <= 0:
            return False
        self.amount = newAmount
        return newAmount

    def changeRate(self, newRate: datetime.timedelta):
        if newRate < datetime.timedelta(days=1): 
            return False
        self.paymentRate = newRate
        return newRate