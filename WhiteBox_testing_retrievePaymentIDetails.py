import unittest
from unittest.mock import patch
from cli import retrieve_payment_details, User

class TestRetrievePaymentDetails(unittest.TestCase):

    def setUp(self):
        # Set up a user with complete payment details
        self.user_with_complete_details = User('Test User', 'test@example.com', 'Password123')
        self.user_with_complete_details.payment_details = {
            'card_number': '1234567890123456',
            'card_holder': 'Test User',
            'expiry_date': '01/23',
            'cvv': '123'
        }


    @patch('builtins.print')
    def test_retrieve_payment_details_with_complete_data(self, mock_print):
        # Test retrieving payment details with complete data
        retrieve_payment_details(self.user_with_complete_details)
        # Check that the payment details were printed correctly
        expected_print_calls = [
            unittest.mock.call("Your current payment details:"),
            unittest.mock.call("Card Number: 1234567890123456"),
            unittest.mock.call("Card Holder: Test User"),
            unittest.mock.call("Expiry Date: 01/23"),
            unittest.mock.call("CVV: 123")
        ]
        mock_print.assert_has_calls(expected_print_calls, any_order=False)

    

if __name__ == '__main__':
    unittest.main()