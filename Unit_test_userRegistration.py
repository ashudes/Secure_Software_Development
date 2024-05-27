import unittest
from OnlineShoppingApp_Main import User

class TestUserRegistration(unittest.TestCase):

    def setUp(self):
        # Setup a test user with known values
        self.test_user = User('John Doe', 'john@example.com', 'Password123!', payment_details={'card_number': '1234567890123456'}, shipping_address={'street': '123 Main St'})

    def test_user_creation(self):
        # Test that the user's name, email, and other details are correctly set
        self.assertEqual(self.test_user.name, 'John Doe')
        self.assertEqual(self.test_user.email, 'john@example.com')
        self.assertEqual(self.test_user.payment_details['card_number'], '1234567890123456')
        self.assertEqual(self.test_user.shipping_address['street'], '123 Main St')

if __name__ == '__main__':
    unittest.main()