from __future__ import annotations
import datetime #Module for working with Dates and Times
import UserAccount
import BalanceAccount
import ChequingAccount
import SavingsAccount
import CreditAccount
import Etransfer
import Loan
import Payee



class ClientAccount(UserAccount.UserAccount):
    def __init__(self, username: str, name: str, password: str, email: str, phone: str, address: str):
        super().__init__(username, name, password)
        self.e_mail = email
        self.phone = phone
        self.address = address
        self.loans = []
        self.payees = []
        self.incomingRequests = []
        self.incomingEtransfers = []
        self.chequingAccount = ChequingAccount.ChequingAccount(self)
        self.savingsAccounts = []
        self.creditAccounts = []
        self.balanceAccounts = [self.chequingAccount] + \
            self.savingsAccounts + self.creditAccounts
    
    #This method takes 'newEmail' as a parameter and replaces the previous email addresss of the client with a new email address.
    def changeEmail(self, newEmail: str):
        if newEmail == "" or newEmail == None:
            return False
        self.e_mail = newEmail
        return True
    
    #This method takes 'newPhone' as a parameter and replaces the previous phone number of the client with a new phone number.
    def changePhone(self, newPhone: str):
        if newPhone == "" or newPhone == None:
            return False
        self.phone_no = newPhone
        return True
    
    #This method takes 'newAddr' as a parameter and replaces the previous Address of the client with a new Address.
    def changeAddress(self, newAddr: str):
        if newAddr == "" or newAddr == None:
            return False
        self.address = newAddr
        return True
    
    
    #This method allows the client to apply for a loan.
    def applyLoan(self, amount: float, type: str, startDate: datetime.datetime, endDate: datetime.datetime):
        loan = Loan.Loan(amount, type, startDate, endDate)
        self.loans.append(loan)
        return True
    
    #This method allows the client to add Payee for paying bills.
    def addPayee(self, payee: Payee.Payee):
        if not isinstance(payee, Payee.Payee):
            return False
        self.payees.append(payee)
        return True
    
    #This method allows the client to apply for a new credit account and if eligibile gets a new Credit Account.
    def openCreditAccount(self, balance: float = 2000):
        if balance < 500:
            return False       
        credit = CreditAccount.CreditAccount(self, balance)
        self.creditAccounts.append(credit)
        return True
    
    #This method allows the client to open a new Savings account.
    def openSavingsAccount(self):
        savings = SavingsAccount.SavingsAccount(self)
        self.savingsAccounts.append(savings)
        return True
    
    #This method allows the client to accept e-transfers if dedicated to the client.
    def acceptEtransfer(self, etransfer: Etransfer.Etransfer):
        if etransfer in self.incomingEtransfers:
            self.incomingEtransfers.remove(etransfer)
            self.chequingAccount.deposit(etransfer.amount)
            return True
        return False
    
    #This method allows the client to request Money from designated contacts.
    def requestMoney(self, amount, requestee):
        import main
        if requestee in main.AccountInterface.clientAcc:
            requestee.incomingRequests.append(
                (self, amount))
            return (self, amount)
        return None  
    
    #This method allows the client to Fulfill Incoming Money request from other users if funds are available.
    def fulfillRequest(self, request):
        requester, amount = request
        if self.chequingAccount.balance < amount:
            return False  # not enough funds
        self.chequingAccount.balance -= amount
        # requester.chequingAccount.balance += amount
        self.incomingRequests.remove(request)
        return True
    
    #This method allows the client to cancel/close their accounts
    def cancelBalanceAccount(self, account: BalanceAccount.BalanceAccount):
        if account == self.chequingAccount:
            self.chequingAccount= None
            return True
        elif account in self.savingsAccounts:
            self.savingsAccounts.remove(account)
            return True
        elif account in self.creditAccounts:
            self.creditAccounts.remove(account)
            return True
        return False  

    def makeLoanPayment(self, account: BalanceAccount.BalanceAccount, amount: int, loan: Loan.Loan):
        if amount > account.balance:
            return False
        account.withdraw(amount)
        loan.pay(amount)
        if loan.getRemainingPayment() == 0:
            self.loans.remove(loan)
        return True

    def __str__(self):
        return f"Client Account of {self.name_of_user}"
