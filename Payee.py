from __future__ import annotations
import IDGenerator

class Payee:
    def __init__(self, name: str, description: str):
        self.payeeID = IDGenerator.IDGenerator.generatePayeeID()
        self.name = name
        self.description = description
    
    #This method takes 'name' parameter and replaces the old value with a new one.
    # In other words, it changes the name of the Payee.
    def change_name(self, name: str):
        self.name = name
    
    #This method takes 'id' parameter and replaces the old value with a new one.
    #In other words, it changes the PayeeID of the Payee.
    def change_payeeID(self, id: int):
        self.payeeID = id
    
    #This method takes 'descp' parameter and replaces the old value with a new one. 
    #In other words, it changes the description of the Payee.
    def change_description(self, descp: str):
        self.description = descp
    
    #Finally it returns the string representation of the object in the below mentioned format.
    def __str__(self):
        return f"Payee ID #{self.payeeID}, {self.name}"