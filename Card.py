from __future__ import annotations
import random
import datetime

class Card:
    def __init__(self, paymentNetwork: str="Visa"):
        self.number = [str(random.randint(0, 9)) for i in range(16)]
        self.cvc = random.randint(100, 999)
        self.dateOfcreation = datetime.date.today()
        self.expiryDate = self.dateOfcreation + datetime.timedelta(days=365*4)
        self.paymentNetwork = paymentNetwork
        self.locked = False

    def lockCard(self):
        self.locked = True

    def unlockCard(self):
        self.locked = False