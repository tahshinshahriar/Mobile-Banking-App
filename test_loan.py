import unittest
import datetime
import Loan


class LoanTest(unittest.TestCase):
    def setUp(self):
        self.loan = Loan.Loan(
            10000,
            "Car",
            datetime.datetime.today(),
            datetime.datetime.today() + datetime.timedelta(days=365),
        )

    def testPay(self):

        # Edge case
        result = self.loan.pay(11000)
        self.assertEqual(result, -1)

        # Base case 1
        result = self.loan.pay(2000)
        self.assertEqual(self.loan.getRemainingPayment(), 8000)

        # Base case 2
        result = self.loan.pay(8000)
        self.assertEqual(self.loan.getRemainingPayment(), 0)


if __name__ == "__main__":
    unittest.main()
