import unittest
import UserAccount

class UserAccountTest(unittest.TestCase):
    def setUp(self):
        self.account = UserAccount.UserAccount("username1", "Daniel", "password123")

    def testUpdate(self):
        #Just need to test if the list got populated
        self.account.update("notif")
        self.assertIn("notif", self.account.notifications)

    def testLogin(self):
        #Wrong both
        status = self.account.login("wronglogin", "wrongpassword")
        self.assertFalse(status)

        #Wrong login
        status = self.account.login("wronglogin", "password123")
        self.assertFalse(status)

        #Wrong password
        status = self.account.login("username1", "wrongpassword")
        self.assertFalse(status)
        
        #Successful login
        status = self.account.login("username1", "password123")
        self.assertTrue(status)

    def testChangePassword(self):
        #Wrong password
        self.account.changePassword("username1", "wrongpassword", "NEWPASS")
        self.assertNotEqual(self.account.getPassword(), "NEWPASS")

        #Wrong username
        self.account.changePassword("wrongusername", "password123", "NEWPASS")
        self.assertNotEqual(self.account.getPassword(), "NEWPASS")

        #Successful change
        self.account.changePassword("username1", "password123", "NEWPASS")
        self.assertEqual(self.account.getPassword(), "NEWPASS")

if __name__ == '__main__':
    unittest.main()