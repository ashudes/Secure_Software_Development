import unittest
from unittest.mock import patch, MagicMock
from cli import confirm_selection, User

class TestConfirmSelection(unittest.TestCase):

    def setUp(self):
        self.user = User('Test User', 'test@example.com', 'Password123')
        self.products = [
            ('Product 1', '10.00'),
            ('Product 2', '20.00'),
            ('Product 3', '30.00')
        ]
        # Assuming the user selects the first two products
        self.selected_indices = [1, 2]

    @patch('CLI.view_product_list')  # Mock view_product_list to prevent actual execution
    @patch('builtins.input', side_effect=['2'])
    def test_confirm_selection_cancel(self, mock_input, mock_view_product_list):
        # Test canceling the selection
        confirm_selection(self.products, self.selected_indices, self.user)
        # Check that view_product_list was called after canceling
        mock_view_product_list.assert_called_once()


if __name__ == '__main__':
    unittest.main()