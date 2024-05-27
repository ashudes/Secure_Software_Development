import unittest
from online_shopping_app_main import ShoppingCart, Product

class TestShoppingCart(unittest.TestCase):
    def setUp(self):
        # Create a test user and a shopping cart
        self.cart = ShoppingCart('Test User')

        # Create some test products
        self.product1 = Product('Product 1', 10.99)
        self.product2 = Product('Product 2', 12.99)

    def test_add_product_to_cart(self):
        # Test adding a single product to the cart
        self.cart.add_item(self.product1)
        self.assertIn(self.product1, self.cart.items, "Product should be in the cart")

    def test_add_multiple_products_to_cart(self):
        # Test adding multiple products to the cart
        self.cart.add_item(self.product1)
        self.cart.add_item(self.product2)
        self.assertIn(self.product1, self.cart.items, "Product 1 should be in the cart")
        self.assertIn(self.product2, self.cart.items, "Product 2 should be in the cart")

    def test_product_quantity_in_cart(self):
        # Test the quantity of products in the cart
        self.cart.add_item(self.product1)
        self.cart.add_item(self.product1)  # Add the same product again
        quantity = self.cart.items.count(self.product1)
        self.assertEqual(quantity, 2, "There should be two of Product 1 in the cart")

# Add more tests as needed to cover different scenarios

if __name__ == '__main__':
    unittest.main()