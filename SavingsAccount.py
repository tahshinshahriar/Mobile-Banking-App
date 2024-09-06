import BalanceAccount
import ClientAccount


class SavingsAccount(BalanceAccount.BalanceAccount):
    def __init__(self, master, balance: float = 0, savingsRate: float = 0.06):
        super().__init__(master, balance)
        self.savingsRate = savingsRate
        self.type = "Savings"

    def __str__(self):
        return f"Savings account #{self.accountNumber} of {self.master.name_of_user}"
