"""This module contains the classes and functions for the Online Shopping Application. 
 It includes user authentication, product management, and utilities for handling
two-factor authentication and email notifications"""
import os
import json
import smtplib
from email.mime.text import MIMEText
import bcrypt
# Function to load data from .txt file
def load_data(filename):
    try:
        with open(filename, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}
def save_data(filename, data):
    print(f"Appending data to {filename}...")
    with open(filename, 'a') as file:
        json.dump(data, file)
    print(f"Data appended to {filename}")
class User:
    def __init__(self, name, email, password, payment_details=None, shipping_address=None):
        self.name = name
        self.email = email
        self.password = self.hash_password(password)  # Hash the password before storing
        self.payment_details = payment_details
        self.shipping_address = shipping_address
    def hash_password(self, password): # Hash a password using bcrypt
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        return hashed_password.decode('utf-8')  # Convert bytes to string before returning
    def check_password(self, password): # Check if a password matches the stored hashed password
        return bcrypt.checkpw(password.encode('utf-8'), self.password.encode('utf-8'))
    def send_2fa_code(self, email): # This method sends a 2FA code to the user's email.
        code = os.urandom(6).hex()
        self._2fa_code = code  # Store the code securely
        # Send the code via email (simplified example)
        msg = MIMEText(f"Your 2FA code is: {code}")
        msg['Subject'] = 'Your 2FA Code'
        msg['From'] = 'noreply@example.com'
        msg['To'] = email
        # Note: SMTP settings need to be configured
        s = smtplib.SMTP('localhost')
        s.send_message(msg)
        s.quit()
    def check_2fa_code(self, code):
        # This method checks the provided 2FA code against the stored one
        return code == self._2fa_code
    def save_to_file(self):
        """Saves data to the file """
        user_data = {
            'name': self.name,
            'email': self.email,
            'password': self.password,
            'payment_details': self.payment_details,
            'shipping_address': self.shipping_address
        }
        print(f"Saving user data: {user_data}") # Print the data that's being saved
        with open('users.txt', 'a') as file:
            file.write(json.dumps(user_data) + "\n")  # Write the user data
        print("User data saved.") # Confirm that the data has been saved
class Administrator(User): #The Administrator inherits properties of the user class above.
    def __init__(self, name, email, password):
        super().__init__(name, email, password)
    def add_product(self, product_list, product):
        product_list.add_product(product)
    def remove_product(self, product_list, product):
        if product in product_list.products:
            product_list.products.remove(product)
        else:
            print("Product not found in the list.")
class Product:
    def __init__(self, name, price):
        self.name = name
        self.price = price
class ProductList:
    """Handles a list of products and saves them to a file."""    
    def __init__(self, filename):
        self.products = []
        self.filename = filename
    def add_product(self, product):
        self.products.append(product)
        self.save_to_file()
    def save_to_file(self):
        try:
            with open(self.filename, 'w') as file:
                print(f"Creating file at: {os.path.abspath(self.filename)}")
                for product in self.products:
                    file.write(f'{product.name}, {product.price}\n')
        except Exception as e:
            print(f"An error occurred while writing to the file: {e}")  
class ShoppingCart:
    """This is the shopping cart class where users checkout and place order"""
    def __init__(self, user):
        self.user = user
        self.items = []
    def add_item(self, product):
        self.items.append(product)
    def checkout(self): # This method would handle the checkout process
        if not self.user._2fa_code or not self.user.check_2fa_code(input("Enter your 2FA code: ")):
            raise Exception("Invalid 2FA code!")
        # Proceed with checkout
class Order:
    def __init__(self, shopping_cart):
        self.shopping_cart = shopping_cart
class Payment:
    def __init__(self, order, payment_type):
        self.order = order
        self.payment_type = payment_type
class Shipping:
    def __init__(self, order, address):
        self.order = order
        self.address = address
"""Allows the admin to add product list via terminal."""
def add_product_via_terminal(product_list):
    while True:
        # Prompt the user for product details
        name = input("Enter the product name (or 'exit' to finish): ")
        if name.lower() == 'exit':
            break
        price = float(input("Enter the product price: "))
        # Create a Product object
        product = Product(name, price)
        # Add the product to the product list
        print(f"Adding product {name} to the list...")
        product_list.add_product(product)
        print(f"Product {name} added.")
def check_product_in_file(filename):
    # Load data from the file
    data = load_data(filename)
    # Print the data
    print(f"Data in {filename}:")
    print(data)
# Create a ProductList
product_list = ProductList('products.txt')

# Add a product via terminal
#add_product_via_terminal(product_list)