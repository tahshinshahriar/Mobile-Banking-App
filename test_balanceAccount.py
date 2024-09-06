import unittest
import datetime
import ClientAccount
import TellerAccount
import WireTransfer
import Payee
import EtransferPayee
import main
import copy


class BalanceAccountTest(unittest.TestCase):
    def setUp(self):
        self.account = ClientAccount.ClientAccount(
            "tahshins",
            "Tahshin Shahriar",
            "abc123",
            "tahshin999@gmail.com",
            "6475223667",
            "123abc St",
        )
        self.chequingAccount = self.account.chequingAccount

        self.teller = TellerAccount.TellerAccount(
            "teller1", "John Wick", "johnwickiscool1"
        )

    def testAddObserver(self):
        # Base case
        self.chequingAccount.addObserver(self.teller)

        self.assertIn(self.teller, self.chequingAccount.observers)

        # Edge case
        self.chequingAccount.addObserver("string")

        self.assertNotIn("string", self.chequingAccount.observers)

    def testRemoveObserver(self):

        # Base case
        self.chequingAccount.addObserver(self.teller)
        self.chequingAccount.removeObserver(self.teller)

        self.assertNotIn(self.teller, self.chequingAccount.observers)

        # Edge case
        self.chequingAccount.removeObserver("i am not in the observers")

        self.assertNotIn("i am not in the observers", self.chequingAccount.observers)

    def testNotifyObservers(self):
        # Just need to make sure the list gets populated, 1 case
        self.chequingAccount.addObserver(self.teller)
        self.chequingAccount.notifyObservers("notification!")

        self.assertIn("notification!", self.teller.notifications)

    def testSetNotifAmount(self):
        # Base case
        self.chequingAccount.setNotifAmount(1000)

        self.assertEqual(self.chequingAccount.notifOnAmount, 1000)

        # Edge case
        self.chequingAccount.setNotifAmount(-10)  # shouldn't work for values <= 0

        self.assertNotEqual(self.chequingAccount.notifOnAmount, -10)

    def testDeposit(self):
        # Base case
        oldbalance = copy.copy(self.chequingAccount.balance)
        self.chequingAccount.deposit(1000)

        self.assertEqual(self.chequingAccount.balance, oldbalance + 1000)

        # Edge case
        oldbalance = copy.copy(self.chequingAccount.balance)
        self.chequingAccount.deposit(-10)

        self.assertEqual(self.chequingAccount.balance, oldbalance)

    def testWithdraw(self):
        # Base case
        oldbalance = copy.copy(self.chequingAccount.balance)
        self.chequingAccount.deposit(100)
        self.chequingAccount.withdraw(20)

        self.assertEqual(self.chequingAccount.balance, oldbalance + 80)

        # Edge case
        oldbalance = copy.copy(self.chequingAccount.balance)
        self.chequingAccount.withdraw(200)  # more than there is in the account

        self.assertEqual(
            self.chequingAccount.balance, oldbalance
        )  # has to remain the same

    def testNewTransaction(self):
        # Just need to make sure the list gets populated
        wireTransfer = WireTransfer.WireTransfer(
            self.chequingAccount, 100, "details", str(self.chequingAccount)
        )
        self.chequingAccount.newTransaction(wireTransfer)

        self.assertIn(wireTransfer, self.chequingAccount.transactions)

    def testTransferBetweenAccounts(self):
        # Case 1 for chequing-credit
        self.chequingAccount.deposit(100)
        self.account.openCreditAccount(1900)
        creditAccount = self.account.creditAccounts[0]
        self.account.openSavingsAccount()
        savingsAccount = self.account.savingsAccounts[0]

        transfer = self.chequingAccount.transferBetweenAccounts(100, creditAccount)

        self.assertEqual(creditAccount.balance, 2000)
        self.assertEqual(self.chequingAccount.balance, 0)
        self.assertIn(transfer, self.chequingAccount.transactions)
        self.assertIn(transfer, creditAccount.transactions)

        # Case 2 for chequing-savings
        savingsAccount.deposit(200)
        transfer = savingsAccount.transferBetweenAccounts(150, self.chequingAccount)

        self.assertEqual(savingsAccount.balance, 50)
        self.assertEqual(self.chequingAccount.balance, 150)
        self.assertIn(transfer, savingsAccount.transactions)
        self.assertIn(transfer, self.chequingAccount.transactions)

        # Edge case
        transfer = self.chequingAccount.transferBetweenAccounts(
            500, creditAccount
        )  # balance should not be enough
        self.assertIsNone(transfer)

    def testSetupAutoPayment(self):
        # Need to make sure the list gets populated
        payee = Payee.Payee("payee1", "desc")
        autoPayment = self.chequingAccount.setupAutoPayment(payee, 100)

        self.assertIn(autoPayment, self.chequingAccount.autoPayments)

    def testSendWireTransfer(self):
        # Base case
        self.chequingAccount.deposit(100)
        wire = self.chequingAccount.sendWireTransfer(100, "desc")

        self.assertEqual(self.chequingAccount.balance, 0)
        self.assertIn(wire, self.chequingAccount.transactions)

        # Edge case
        wire = self.chequingAccount.sendWireTransfer(100, "desc2")

        self.assertEqual(self.chequingAccount.balance, 0)
        self.assertIsNone(wire)

    def testSendEtransfer(self):
        self.account1 = ClientAccount.ClientAccount(
            "chemistryteacher",
            "Walter White",
            "saymyname",
            "walterwhite@gmail.com",
            "3998321786",
            "308 Belmont Avenue, Ontario, California 91764",
        )
        main.AccountInterface.clientAcc.append(self.account1)

        # Case 1 for a user in the same bank
        self.chequingAccount.deposit(500)
        self.account.addPayee(
            EtransferPayee.EtransferPayee(
                "Walter White", "desc", "walterwhite@gmail.com"
            )
        )
        etransfer = self.chequingAccount.sendEtransfer(
            100, "walterwhite@gmail.com", "3998321786"
        )

        self.assertEqual(self.chequingAccount.balance, 400)
        self.assertEqual(self.account1.chequingAccount.balance, 100)
        self.assertIn(etransfer, self.chequingAccount.transactions)
        self.assertIn(etransfer, self.account1.chequingAccount.transactions)

        # Edge case for insufficient funds
        etransfer = self.chequingAccount.sendEtransfer(
            1000, "walterwhite@gmail.com", "3998321786"
        )

        self.assertIsNone(etransfer)

        # Case 2 for a different bank and just e-mail
        self.account.addPayee(
            EtransferPayee.EtransferPayee("dude", "desc", "notinthesamebank@gmail.com")
        )
        etransfer = self.chequingAccount.sendEtransfer(
            100, "notinthesamebank@gmail.com"
        )

        self.assertEqual(self.chequingAccount.balance, 300)
        self.assertIn(etransfer, self.chequingAccount.transactions)

        # Case 3 for a different bank and just phone
        self.account.addPayee(
            EtransferPayee.EtransferPayee("dude", "desc", phone="6421768234")
        )
        etransfer = self.chequingAccount.sendEtransfer(100, phone="6421768234")

        self.assertEqual(self.chequingAccount.balance, 200)
        self.assertIn(etransfer, self.chequingAccount.transactions)

        main.AccountInterface.clientAcc = []

    def testMakePurchase(self):
        # Base case
        self.chequingAccount.deposit(100)
        purchase = self.chequingAccount.makePurchase(
            100, "Bubble Tea", "Bubble Tea Store #1"
        )

        self.assertEqual(self.chequingAccount.balance, 0)
        self.assertIn(purchase, self.chequingAccount.transactions)

        # Edge case
        purchase = self.chequingAccount.makePurchase(
            300, "Something Expensive", "Expensive Store #1"
        )

        self.assertIsNone(purchase)

    def testWithdrawalATM(self):
        # Base case
        self.chequingAccount.deposit(100)
        withdrawal = self.chequingAccount.withdrawATM(100, "Some Other Bank")

        self.assertEqual(self.chequingAccount.balance, 0)
        self.assertIn(withdrawal, self.chequingAccount.transactions)

        # Edge case
        withdrawal = self.chequingAccount.withdrawATM(300)

        self.assertIsNone(withdrawal)


if __name__ == "__main__":
    unittest.main()
