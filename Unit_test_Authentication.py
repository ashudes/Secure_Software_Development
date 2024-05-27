import unittest
from OnlineShoppingApp_Main import User

class TestTwoFactorAuthentication(unittest.TestCase):

    def setUp(self):
        # Create a user with known credentials and a mock 2FA code
        self.user = User('Test User', 'test@example.com', 'CorrectPassword123')
        self.user._2fa_code = '123456'  # Mock 2FA code for testing

    def test_2fa_code_check_with_correct_code(self):
        # Simulate checking the 2FA code with the correct code
        result = self.user.check_2fa_code('123456')
        self.assertTrue(result)

    def test_2fa_code_check_with_incorrect_code(self):
        # Simulate checking the 2FA code with an incorrect code
        result = self.user.check_2fa_code('654321')
        self.assertFalse(result)

if __name__ == '__main__':
    unittest.main()