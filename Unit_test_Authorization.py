import unittest
from OnlineShoppingApp_Main import User, Administrator, Product, ProductList

class TestAuthorization(unittest.TestCase):

    def setUp(self):
        # Set up a regular user and an administrator with different permissions
        self.user = User('Regular User', 'user@example.com', 'UserPassword')
        self.admin = Administrator('Admin User', 'admin@example.com', 'AdminPassword')
        self.product = Product('Test Product', 10.99)  # Create a test product
        self.product_list = ProductList('test_products.txt')  # Create a test product list

    def test_regular_user_access(self):
        # Test that a regular user does not have access to admin-only methods
        with self.assertRaises(AttributeError):
            self.user.add_product(self.product_list, self.product)

    def test_admin_access(self):
        # Test that an administrator has access to admin-only methods
        self.admin.add_product(self.product_list, self.product)
        self.assertIn(self.product, self.product_list.products)

if __name__ == '__main__':
    unittest.main()