import unittest
import TellerAccount
import ClientAccount
import main

class TellerAccountTest(unittest.TestCase):
    def setUp(self):
        self.account = TellerAccount.TellerAccount("iamateller", "Nikita", "teller123")
        main.AccountInterface.clientAcc = []

    def testRegisterClient(self):
        #Base case
        client = self.account.registerClient("john98", "John Menkes", "johnmenkes@torontomu.ca", "6477733305", "180 Sherbourne St, Toronto, Ontario")
        self.assertIn(client, main.AccountInterface.clientAcc)

        #Edge case (attempt to register a client with the same username (john98))
        client = self.account.registerClient("john98", "John Acrey", "johnacrey@torontomu.ca", "6421787306", "160 Mutual St, Toronto, Ontario")
        self.assertIsNone(client)

    def testFindClient(self):
        #Base case
        client = self.account.registerClient("john98", "John Menkes", "johnmenkes@torontomu.ca", "6477733305", "180 Sherbourne St, Toronto, Ontario")
        
        resultOfSearch = self.account.findClient(client.getAccountNumber())
        self.assertEqual(resultOfSearch, client)

        #Edge case (this client doesn't exist)
        resultOfSearch = self.account.findClient(12345)
        self.assertIsNone(resultOfSearch)

if __name__ == '__main__':
    unittest.main()