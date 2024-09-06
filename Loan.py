import datetime


class Loan:
    def __init__(
        self,
        amount: float,
        type: str,
        startDate: datetime.datetime,
        endDate: datetime.datetime,
        yearlyRate: float = 0.10,
        paymentRate: datetime.timedelta = datetime.timedelta(days=30),
    ):
        self.amount = amount
        self.type = type
        self.remainingPayment = amount
        self.yearlyRate = yearlyRate
        self.paymentRate = paymentRate
        self.startDate = startDate
        self.endDate = endDate

    def getRemainingPayment(self):
        return self.remainingPayment

    def pay(self, amount: float):
        # Don't want to charge the client more than needed
        if amount > self.remainingPayment:
            return -1

        self.remainingPayment -= amount
        return self.remainingPayment
