from __future__ import annotations
import random
import string
import datetime
import IDGenerator


class UserAccount:
    def __init__(self, username: str, name: str, password: str):
        self.username = username
        self.name_of_user = name
        self._accountNumber = IDGenerator.IDGenerator.generateUserAccountID()
        self._password = password
        self.notifications = []
        self._creationDate = datetime.date.today()

    def update(self, notification: str):
        self.notifications.append(notification)

    def getAccountNumber(self):
        return self._accountNumber

    def getUserName(self):
        return self.username

    def getAccountNumber(self):
        return self._accountNumber

    def getPassword(self):
        return self._password

    def login(self, login: str, password: str):
        if login == self.username and password == self._password:
            return True
        return False

    def changePassword(self, username: str, oldpasswd: str, newpasswd: str):
        if (
            username == self.username and oldpasswd == self._password
        ):  # Check both credentials
            self._password = newpasswd
            return True
        return False

    def changeName(self, newName: str):
        self.name_of_user = newName

    def getUsername(self):
        return self.username

    @staticmethod
    def passwordGenerator():
        chars = string.ascii_letters + string.digits + string.punctuation
        passwd = "".join(random.choice(chars) for i in range(10))
        return passwd
