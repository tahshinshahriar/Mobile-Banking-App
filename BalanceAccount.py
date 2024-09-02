from __future__ import annotations
from typing import TYPE_CHECKING
import datetime
import Transaction
import AutoPayment
import Payee
import EtransferPayee
import Card
import IDGenerator

if TYPE_CHECKING:
    import ClientAccount
    import UserAccount

class BalanceAccount:
    def __init__(self, master: ClientAccount.ClientAccount, balance: float, paymentNetwork: str="Visa"):
        self.master = master
        self.accountNumber = IDGenerator.IDGenerator.generateBalanceAccountID()
        self.balance = balance
        self.card = Card.Card(paymentNetwork=paymentNetwork)
        self.transactions = []
        self.autoPayments = []
        self.observers = [master] #add the client account of this balance account to observe by default
        self.notifOnAmount = 500 #notify the subscribers on this amount (the observer pattern)
        self.creationDate = datetime.date.today()

    def addObserver(self, observer: UserAccount.UserAccount):
        import UserAccount
        if isinstance(observer, UserAccount.UserAccount):
            self.observers.append(observer)
    
    def removeObserver(self, observer):
        if observer in self.observers:
            self.observers.remove(observer)

    def notifyObservers(self, notification: str):
        import UserAccount
        for obs in self.observers:
            if isinstance(obs, UserAccount.UserAccount):
                obs.update(notification)

    def setNotifAmount(self, amount: int):
        if amount <= 0:
            return False
        self.notifOnAmount = amount
        return True

     #do not use this method directly!
    def deposit(self, amount: float):
        if amount <= 0:
            return None
        self.balance = self.balance + amount
        return self.balance

    #do not use this method directly!
    def withdraw(self, amount: float):
        if amount > self.balance:
            return None
        if self.notifOnAmount and amount > self.notifOnAmount:
            notification = f'A transaction for amount {amount}CAD has been performed on balance account #{self.accountNumber} of client account #{self.master.getAccountNumber()}'
            self.notifyObservers(notification)
        self.balance -= amount
        return self.balance

    #do not use directly
    def newTransaction(self, transaction: Transaction.Transaction):
        self.transactions.append(transaction)

    def transferBetweenAccounts(self, amount: float, account2: BalanceAccount):
        if amount > self.balance:
            return None

        import SelfTransaction

        transfer = SelfTransaction.SelfTransaction(
            self, amount, str(self), str(account2))
        self.newTransaction(transfer)
        self.withdraw(amount)

        account2.deposit(amount)
        account2.newTransaction(transfer)

        return transfer


    def setupAutoPayment(self, payee: Payee.Payee, amount: float, freq: datetime.timedelta=datetime.timedelta(days=30)):
        autoPayment = AutoPayment.AutoPayment(payee, freq, amount)
        self.autoPayments.append(autoPayment)
        return autoPayment


    def sendWireTransfer(self, amount: float, details: str):
        import WireTransfer
        if amount > self.balance:
            return None
        wire = WireTransfer.WireTransfer(self, amount, details, str(self))
        self.withdraw(amount)
        self.newTransaction(wire)
        return wire
    
    
    def sendEtransfer(self, amount: float, email: str=None, phone: str=None):
        if amount > self.balance:
            return None
            
        
        import main
        import Etransfer
        #Case if both email and phone were given
        if email and phone:
            for payee in self.master.payees:
                if isinstance(payee, EtransferPayee.EtransferPayee) and (payee.email == email or payee.phone == phone):
                    for account in main.AccountInterface.clientAcc:
                        #If found in the same bank (our system)
                        if account.phone == phone or account.e_mail == email:
                            etransfer = Etransfer.Etransfer(self, amount, email, phone, str(self), str(account)) #The receiver argument is a string representation of the receiving account
                            self.withdraw(amount)
                            self.newTransaction(etransfer)
                            account.chequingAccount.newTransaction(etransfer)
                            account.chequingAccount.deposit(amount)
                            return etransfer
                        
                    #If not found, the receiver argument is just the email string
                    etransfer = Etransfer.Etransfer(self, amount, email, phone, str(self), email)
                    self.withdraw(amount)
                    self.newTransaction(etransfer)
                    return etransfer
            
            return None #payee not found in self.payees
        
        #Case if just the email was given
        elif email:
            for payee in self.master.payees:
                if isinstance(payee, EtransferPayee.EtransferPayee) and payee.email == email:
                    for account in main.AccountInterface.clientAcc:
                        if account.e_mail == email:
                            etransfer = Etransfer.Etransfer(self, amount, email, sender=str(self), receiver=str(account))
                            self.withdraw(amount)
                            self.newTransaction(etransfer)
                            account.chequingAccount.newTransaction(etransfer)
                            account.chequingAccount.deposit(amount)
                            return etransfer
                        
                        etransfer = Etransfer.Etransfer(self, amount, email, sender=str(self), receiver=email)
                        self.withdraw(amount)
                        self.newTransaction(etransfer)
                        return etransfer
                    
            return None
        
        #Case if just the phone was given
        elif phone:
            for payee in self.master.payees:
                if isinstance(payee, EtransferPayee.EtransferPayee) and payee.phone == phone:
                    for account in main.AccountInterface.clientAcc:
                        if account.phone == phone:
                            etransfer = Etransfer.Etransfer(self, amount, phone=phone, sender=str(self), receiver=str(account))
                            self.withdraw(amount)
                            self.newTransaction(etransfer)
                            account.chequingAccount.newTransaction(etransfer)
                            account.chequingAccount.deposit(amount)
                            return etransfer
                        
                    etransfer = Etransfer.Etransfer(self, amount, phone=phone, sender=str(self), receiver=phone)
                    self.withdraw(amount)
                    self.newTransaction(etransfer)
                    return etransfer
        
        return None
    

    def makePurchase(self, amount: float, name: str, location: str):
        import Purchase
        if amount > self.balance:
            return None
        purchase = Purchase.Purchase(amount, name, location, str(self))
        self.withdraw(amount)
        self.newTransaction(purchase)
        return purchase
    
    def withdrawATM(self, amount: float, bank: str="T Bank"):
        import ATMWithdrawal
        if amount > self.balance:
            return None
        atmwithdrawal = ATMWithdrawal.ATMWithdrawal(self, amount, bank, str(self), bank)
        self.withdraw(amount)
        self.newTransaction(atmwithdrawal)
        return atmwithdrawal