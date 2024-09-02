from __future__ import annotations
import main
import ClientAccount
import UserAccount
import IDGenerator


class TellerAccount(UserAccount.UserAccount):
    def __init__(self, username: str, name: str, password: str):
        super().__init__(username, name, password=password)
        self.employeeID = IDGenerator.IDGenerator.generateEmployeeID()

    def registerClient(self, username: str, name: str, email: str, phone: str, address: str, password: str = UserAccount.UserAccount.passwordGenerator()):
        #Iterate over all the clients
        for client in main.AccountInterface.clientAcc:
            if client.getUserName() == username:
                return None #if a client with the same username exists, return None
        client = ClientAccount.ClientAccount(username, name, password, email, phone, address)
        main.AccountInterface.clientAcc.append(client)
        return client
    
    def findClient(self, accountNumber: int):
        for client in main.AccountInterface.clientAcc:
            if client.getAccountNumber() == accountNumber:
                return client
        return None

    def __str__(self):
        return f" Username={self.username} \n Name={self.name_of_user} \n EmployeeID={self.employeeID} \n "
