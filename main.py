class AccountInterface:
    clientAcc = []
    tellerAcc = []

    def login(self, username, password, accType):
        if accType == "cl":
            for x in self.clientAcc:
                if x.username == username and x._password == password:
                    return x
            return False
        elif accType == "bt":
            for x in self.tellerAcc:
                if x.username == username and x._password == password:
                    return x
            return False
        else:
            return False
    
    # Remove the clientAccount from the array and return true else return False
    def closeAccount(self, username, password):
        for x in self.clientAcc:
            if x.username == username and x._password == password:
                self.clientAcc.remove(x)
                return True
        return False


