from __future__ import annotations
import unittest
import datetime
import ClientAccount
import Payee
import Etransfer
import BalanceAccount
import main

class ClientAccountTest(unittest.TestCase):

    def setUp(self):
        self.account = ClientAccount.ClientAccount(
            "tahshins",
            "Tahshin Shahriar",
            "abc123",
            "tahshin999@gmail.com",
            "6475223667",
            "123abc St",
        )

    def test_changeEmail(self):
        result = self.account.changeEmail("tahshin89@gmail.com")
        self.assertTrue(result)
        newEmail = self.account.e_mail
        self.assertEqual(newEmail, "tahshin89@gmail.com")

        result = self.account.changeEmail("")
        self.assertFalse(result)

    def test_changePhone(self):
        # Base Testcase
        result = self.account.changePhone("6471239999")
        self.assertTrue(result)
        newPhone = self.account.phone_no
        self.assertEqual(newPhone, "6471239999")

        # Edge Testcase
        result = self.account.changePhone(None)
        self.assertFalse(result)

    def test_changeAddress(self):
        # Base Testcase
        result = self.account.changeAddress("60 shuter St")
        self.assertTrue(result)
        newAddr = self.account.address
        self.assertEqual(newAddr, "60 shuter St")

        # Edge Testcase
        result = self.account.changeAddress("")
        self.assertFalse(result)

    def test_applyLoan(self):
        # Base Testcase
        amount = 1000
        type = "Car Loan"
        startDate = datetime.datetime.now()
        endDate = datetime.datetime(2024, 4, 3)
        result = self.account.applyLoan(amount, type, startDate, endDate)
        self.assertEqual(len(self.account.loans), 1)
        self.assertEqual(self.account.loans[0].amount, amount)
        self.assertEqual(self.account.loans[0].type, type)
        self.assertEqual(self.account.loans[0].startDate, startDate)
        self.assertEqual(self.account.loans[0].endDate, endDate)

        # edge Test
        startDate = datetime.datetime.now()
        endDate = startDate + datetime.timedelta(days=1)
        amount = 0.01
        self.account.applyLoan(amount, type, startDate, endDate)
        self.assertEqual(len(self.account.loans), 2)
        self.assertEqual(self.account.loans[1].amount, amount)
        self.assertEqual(self.account.loans[1].type, type)
        self.assertEqual(self.account.loans[1].startDate, startDate)
        self.assertEqual(self.account.loans[1].endDate, endDate)

    def test_openSavingsAccount(self):
        # Base Testcase
        initial_length = len(self.account.savingsAccounts)
        result = self.account.openSavingsAccount()
        self.assertTrue(result)
        self.account.openSavingsAccount()
        self.assertEqual(len(self.account.savingsAccounts), initial_length + 2)

        # Edge Testcase
        initial_length = len(self.account.savingsAccounts)
        for i in range(5):
            self.account.openSavingsAccount()
        self.assertEqual(len(self.account.savingsAccounts), initial_length + 5)

    def test_openCreditAccount(self):
        # Base Testcase
        result = self.account.openCreditAccount(1000)
        self.assertTrue(result)
        self.assertEqual(len(self.account.creditAccounts), 1)
        self.assertEqual(self.account.creditAccounts[0].balance, 1000)

        # Edge Testcase
        result = self.account.openCreditAccount(0)
        self.assertFalse(result)
        self.assertEqual(len(self.account.creditAccounts), 1)

    def test_addPayee(self):
        payee1 = Payee.Payee("Slava", "")
        payee2 = ("Fardin", "Whatever")

        # Base Test
        self.account.addPayee(payee1)
        self.assertIn(payee1, self.account.payees)

        # Edge Test
        result = self.account.addPayee(payee2)
        self.assertFalse(result)

    def test_acceptEtransfer(self):
        eTransfer = Etransfer.Etransfer(
            self.account.chequingAccount,
            500,
            "slava@gmail.com",
            "6475143556",
            "Tahshin",
            "Slava",
        )
        self.account.incomingEtransfers.append(eTransfer)
        result = self.account.acceptEtransfer(eTransfer)
        self.assertTrue(result)
        self.assertNotIn(eTransfer, self.account.incomingEtransfers)

    def test_requestMoney(self):
        account2 = ClientAccount.ClientAccount(
            "john98",
            "John Menkes",
            "password123",
            "johnmenkes@torontomu.ca",
            "6477733305",
            "180 Sherbourne St, Toronto, Ontario",
        )
        account2.chequingAccount.deposit(100)
        main.AccountInterface.clientAcc.append(account2)  # Add to the database

        # Edge case (insufficient amount)
        request1 = self.account.requestMoney(500, account2)
        self.assertIn(request1, account2.incomingRequests)

        result1 = account2.fulfillRequest(request1)
        self.assertFalse(result1)
        self.assertIn(request1, account2.incomingRequests)

        # Base case
        request2 = self.account.requestMoney(100, account2)
        self.assertIn(request2, account2.incomingRequests)

        result2 = account2.fulfillRequest(request2)
        self.assertTrue(result2)
        self.assertNotIn(
            request2, account2.incomingRequests
        )  # Supposed to get removed from the list

        main.AccountInterface.clientAcc = []

    def test_cancel_balance_account(self):
        self.account.openSavingsAccount()
        self.account.openCreditAccount(1000)
        account = self.account.creditAccounts[0]
        # Base case
        result = self.account.cancelBalanceAccount(account)
        self.assertTrue(result)
        # Edge Case
        account = BalanceAccount.BalanceAccount(
            ClientAccount.ClientAccount(
                "john98",
                "John Menkes",
                "password123",
                "johnmenkes@torontomu.ca",
                "6477733305",
                "180 Sherbourne St, Toronto, Ontario",
            ),
            500,
        )
        result = self.account.cancelBalanceAccount(account)
        self.assertFalse(result)

    def test_makeLoanPayment(self):
        self.account.chequingAccount.balance = 1000
        amount = 500
        type = "Education Loan"
        startDate = datetime.datetime.now()
        endDate = datetime.datetime(2024, 4, 3)
        self.account.applyLoan(amount, type, startDate, endDate)

        result = self.account.makeLoanPayment(
            self.account.chequingAccount, 500, self.account.loans[0]
        )
        self.assertTrue(result)
        self.assertEqual(self.account.chequingAccount.balance, 500)


if __name__ == "__main__":
    unittest.main()
