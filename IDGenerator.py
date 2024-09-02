#Class for generating unique IDs
class IDGenerator:
    userAccountID = 10000
    balanceAccountID = 100000
    transactionID = 100000
    payeeID = 1000
    employeeID = 100
    atmID = 100
    
    @classmethod
    def generateUserAccountID(cls):
        cls.userAccountID += 1
        return cls.userAccountID
    
    @classmethod
    def generateBalanceAccountID(cls):
        cls.balanceAccountID += 1
        return cls.balanceAccountID
    
    @classmethod
    def generateTransactionID(cls):
        cls.transactionID += 1
        return cls.transactionID
    
    @classmethod
    def generatePayeeID(cls):
        cls.payeeID += 1
        return cls.payeeID
    
    @classmethod
    def generateEmployeeID(cls):
        cls.employeeID += 1
        return cls.employeeID
    
    @classmethod
    def generateAtmID(cls):
        cls.atmID += 1
        return cls.atmID