import ClientAccount
import unittest
import datetime
import AutoPayment
import Payee

class AutoPaymentTest(unittest.TestCase):
    def setUp(self):
        self.account = ClientAccount.ClientAccount(
            "tahshins", "Tahshin Shahriar", "abc123", "tahshin999@gmail.com", "6475223667", "123abc St")
        self.payee = Payee.Payee("Slava", "description")
        self.autoPayment = AutoPayment.AutoPayment(self.payee, datetime.timedelta(days=30), 100)

    def testChangeAmount(self):
        #Base case
        self.autoPayment.changeAmount(500)
        self.assertEqual(self.autoPayment.amount, 500)
        
        #Edge case (if 0 do nothing)
        self.autoPayment.changeAmount(0)
        self.assertNotEqual(self.autoPayment.amount, 0) #has to remain the same
    
    def testChangeRate(self):
        newRate = datetime.timedelta(days=50)
        wrongRate = datetime.timedelta(days=0)

        #Base case
        self.autoPayment.changeRate(newRate)
        self.assertEqual(self.autoPayment.paymentRate, newRate)

        #Edge case
        self.autoPayment.changeRate(wrongRate)
        self.assertNotEqual(self.autoPayment.paymentRate, wrongRate) #has to remain the same

if __name__ == '__main__':
    unittest.main()