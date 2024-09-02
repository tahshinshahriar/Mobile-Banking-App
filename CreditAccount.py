from __future__ import annotations
import BalanceAccount

class CreditAccount(BalanceAccount.BalanceAccount):
    def __init__(self, master, balance: float=2000, yearlyRate: float=0.15, cashAdvanceFee: float=0.18):
        super().__init__(master, balance, paymentNetwork="MasterCard")
        self.yearlyRate = yearlyRate
        self.cashAdvanceFee = cashAdvanceFee
        self.nextPaymentDate = None
        self.minimumPaymentAmount = None
        self.type = "Credit"

    def __str__(self):
        return f'Credit account #{self.accountNumber} of {self.master.name_of_user}'