import unittest
from OnlineShoppingApp_Main import User

class TestSecureLogin(unittest.TestCase):

    def setUp(self):
        # Create a user with known credentials
        self.user = User('Test User', 'test@example.com', 'CorrectPassword123')

    def test_login_with_correct_credentials(self):
        # Simulate logging in with correct credentials
        result = self.user.check_password('CorrectPassword123')
        self.assertTrue(result)

    def test_login_with_incorrect_credentials(self):
        # Simulate logging in with incorrect credentials
        result = self.user.check_password('WrongPassword')
        self.assertFalse(result)

if __name__ == '__main__':
    unittest.main()