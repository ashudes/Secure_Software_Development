"""This module contains the functions for implementing command line interface (CLI) 
for the user to register, login, and do online shopping """
import json # Used for parsing and manipulating JSON data
import re  # provides support for regular expressions for matching patterns in strings
import bcrypt # Used for hashing and salting passwords to enhance security
from online_shopping_app_main import User # Imports the User class from the main application module
import random # This is needed for generating order number/ID for tracking
global current_user
current_user = None

def main_menu():
    print("Home Page")
    print("1. Register")
    print("2. Login")
    choice = input("Enter your choice: ")
    if choice == '1':
        register()
    elif choice == '2':
        login()

def register():
    try:
        print("Please enter your details to register.")
        first_name = input("Enter your first name: ")
        surname = input("Enter your surname: ")
        email = input("Enter your email: ")
        # Password requirements
        password_pattern = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\W).{8,}$')
        while True:
            password = input("Enter your password: ")
            if not password_pattern.match(password):
                print("Password must be at least 8 characters long with at least one uppercase letter, one lowercase letter, and one special character.")
            else:
               break
        # Payment details requirements
        card_number_pattern = re.compile(r'^\d{16}$')
        expiry_date_pattern = re.compile(r'^(0[1-9]|1[0-2])\/\d{2}$')
        cvv_pattern = re.compile(r'^\d{3}$')
        while True:
            card_number = input("Enter your 16-digit card number: ")
            expiry_date = input("Enter your card's expiry date (MM/YY): ")
            cvv = input("Enter your card's CVV (3 digits): ")
            if not (card_number_pattern.match(card_number) and expiry_date_pattern.match(expiry_date) and cvv_pattern.match(cvv)):
                print("Please enter a correct card number, expiry date, and CVV.")
            else:
                payment_details = {'card_number': card_number, 'expiry_date': expiry_date, 'cvv': cvv}
                break
        # Shipping address requirements
        country = input("Enter your country name: ")
        city = input("Enter your city name: ")
        street_address = input("Enter your street address: ")
        house_number = input("Enter your house number: ")
        if not (country and city and street_address and house_number):
            print("Please enter all the required fields.")
            # Optionally, return to the main menu
        else:
            shipping_address = {'country': country, 'city': city, 'street_address': street_address, 'house_number': house_number}
        
        # Create a new User object with the additional information
        user = User(first_name + " " + surname, email, password, payment_details, shipping_address)
        # Save the new user to a file
        user.save_to_file()
        print(f"User {first_name} {surname} registered successfully.")
        main_menu()

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        main_menu()

def login():
    global current_user
    email = input("Enter your email: ")
    password = input("Enter your password: ")

    try:
        with open('users.txt', 'r') as file:
            users = [json.loads(line) for line in file if line.strip()]
    except json.JSONDecodeError as e:
        print(f"An error occurred while reading the file: {e}")
        return

    for user_data in users:
        if user_data['email'] == email and bcrypt.checkpw(password.encode('utf-8'), user_data['password'].encode('utf-8')):
            current_user = User(user_data['name'], user_data['email'], password, user_data.get('payment_details'), user_data.get('shipping_address'))
            print(f"Welcome back, {current_user.name}!")
            after_login()
            break
    else:
        print("Invalid email or password.")

def after_login():
    global current_user
    print("1. View Product List")
    print("2. Logout")
    choice = input("Enter your choice: ")
    if choice == '1':
        view_product_list(current_user)  # Pass current_user to the view_product_list function
    elif choice == '2':
        # Here you can handle the logout logic
        print("You have been logged out.")
        main_menu()  # Return to the main menu

def view_product_list(current_user):
    # Open and read the products.txt file
    with open('products.txt', 'r') as file:
        products = [line.strip().split(', ') for line in file.readlines()]
    # Print each product with an index
    for i, product in enumerate(products, start=1):
        print(f"{i}. {product[0]}, {product[1]}")
    print("Enter the numbers of the products you want to select separated by commas (e.g., 1,2,3),")
    print("or enter '0' to return to the home page.")
    selected_indices = input("Enter your choice: ")
    if selected_indices.strip() == '0':
        after_login()  # Call the function that shows the post-login options
        return
    # Split the input by commas and convert to integers
    selected_indices = [int(index) for index in selected_indices.split(',') if index.strip().isdigit()]
    # Validate selected indices
    if not all(1 <= i <= len(products) for i in selected_indices):
        print("One or more selected product numbers are invalid.")
        view_product_list(current_user)
        return
    # Confirm selection
    confirm_selection(products, selected_indices, current_user)

def confirm_selection(products, selected_indices, current_user):
    selected_products = [products[i-1] for i in selected_indices]
    total_price = sum(float(product[1]) for product in selected_products)
    print("\nYou have selected the following products:")
    for product in selected_products:
        print(f"{product[0]}, {product[1]}")
    print(f"Total price: {total_price}")
    print("\nConfirm your selection:")
    print("1. Confirm")
    print("2. Cancel")
    choice = input("Enter your choice: ")
    if choice == '1':
        after_selection(selected_products, total_price, current_user)
    elif choice == '2':
        view_product_list(current_user)

shopping_cart = []

def after_selection(selected_products, total_price, current_user):
    print("\nSelected products:")
    for product in selected_products:
        print(f"{product[0]}, {product[1]}")
    print(f"Total price: {total_price}")
    print("\nWhat would you like to do next?")
    print("1. Send to cart")
    print("2. Remove products")
    print("3. Add more products to selection")
    print("4. Return to product selection page")
    choice = input("Enter your choice: ")
    if choice == '1':
        send_to_cart(selected_products, current_user)
    elif choice == '2':
        remove_product(selected_products, current_user)
    elif choice == '3':
        view_product_list(current_user)  # Redirect back to the product list
    elif choice == '4':
        view_product_list(current_user)

def send_to_cart(selected_products, current_user):
    # Add the selected products to the global shopping cart
    global shopping_cart
    shopping_cart.extend(selected_products)
    print("Selected products have been added to the cart.")
    view_cart(current_user)


def remove_product(selected_products):
    # Display the selected products with an index
    for i, product in enumerate(selected_products, start=1):
        print(f"{i}. {product[0]}, {product[1]}")
    indices_to_remove = input("Enter the numbers of the products you want to remove separated by commas (e.g., 1,2,3): ")
    # Split the input by commas and convert to integers
    indices_to_remove = [int(index) for index in indices_to_remove.split(',')]
    # Remove the selected products by index
    for index in sorted(indices_to_remove, reverse=True):
        if 1 <= index <= len(selected_products):
            removed_product = selected_products.pop(index-1)
            print(f"Removed: {removed_product[0]}")
        else:
            print(f"No product found at index: {index}")
    # After removing products, you may want to call a function to display the updated list or go back to the menu
    after_selection(selected_products, sum(float(product[1]) for product in selected_products))

def add_product():
    # Prompt the user for product details
    name = input("Enter the product name: ")
    price = input("Enter the product price: ")
    # Add the new product to the global shopping cart
    global shopping_cart
    shopping_cart.append((name, price))
    print(f"Added product {name} to the cart.")
    # After adding a product, you may want to call a function to display the cart or go back to the menu
    view_cart()

def view_cart(current_user):
    # Display the products in the global shopping cart
    global shopping_cart
    print("\nShopping Cart:")
    for i, product in enumerate(shopping_cart, start=1):
        print(f"{i}. {product[0]}, {product[1]}")
    # Display the total price of the products in the cart
    total_price = sum(float(product[1]) for product in shopping_cart)
    print(f"Total price: {total_price}")
    # Provide options for the next steps
    print("\nWhat would you like to do next?")
    print("1. Checkout")
    print("2. Remove products")
    print("3. Add more products")
    print("4. Empty cart")
    print("5. Return to product selection page")
    choice = input("Enter your choice: ")
    if choice == '1':
        checkout(current_user)
    elif choice == '2':
        remove_product(shopping_cart, current_user)
    elif choice == '3':
        add_product(current_user)
    elif choice == '4':
        shopping_cart.clear()
        print("Cart has been emptied.")
        view_product_list(current_user)
    elif choice == '5':
        view_product_list(current_user)


def checkout(current_user):
    global shopping_cart
    print("\nCheckout Page:")
    for i, product in enumerate(shopping_cart, start=1):
        print(f"{i}. {product[0]}, {product[1]}")
    total_price = sum(float(product[1]) for product in shopping_cart)
    print(f"Total price: {total_price}")

    print("\nWould you like to proceed with your order?")
    print("1. Yes, proceed to order")
    print("2. No, return to cart")
    choice = input("Enter your choice: ")
    if choice == '1':
        proceed_to_order(current_user)
    elif choice == '2':
        view_cart(current_user)


def proceed_to_order(current_user):
    # This function transitions the user from the cart to the ordering process
    print("\nOrdering Page:")
    pay(current_user)  # Pass the user object to the pay function

def pay(current_user):
    # This function handles the payment process
    print("\nPayment Page:")
    # Displays several next options to the user
    print("Please choose an option to continue:")
    print("1. Add/modify delivery address")
    print("2. Add payment details")
    print("3. Retrieve payment details")
    choice = input("Enter your choice: ")
    if choice == '1':
        add_modify_address(current_user)
    elif choice == '2':
        add_payment_details(current_user)
    elif choice == '3':
        retrieve_payment_details(current_user)

"""Helps user to add/modify delivery address"""
def add_modify_address():# Helps user to add/modify delivery address
    address = input("Please enter your delivery address: ")
    print("Address added/modified successfully.")
    pay()  # Return to the payment options

def add_payment_details():
    # Add code to add payment details
    payment_info = input("Please enter your payment details: ")
    print("Payment details added successfully.")
    confirm_payment()  # Proceed to confirm payment

def retrieve_payment_details(current_user):
    # Retrieve and display the current payment details
    print("Your current payment details:")
    
    # Check if 'payment_details' is a dictionary and not a string
    if isinstance(current_user.payment_details, dict) and current_user.payment_details:
        print(f"Card Number: {current_user.payment_details.get('card_number', 'Not available')}")
        print(f"Card Holder: {current_user.payment_details.get('card_holder', 'Not available')}")
        print(f"Expiry Date: {current_user.payment_details.get('expiry_date', 'Not available')}")
        print(f"CVV: {current_user.payment_details.get('cvv', 'Not available')}")
    else:
        print("Sorry, there are no registered payment details. Please use the edit menu to add payment details.")
        print("\n1. Yes, edit payment details")
        print("2. Return to main menu")
        print("3. Sign out")
        choice = input("Enter your choice: ")
        if choice == '1':
            # Prompt for new details
            card_number = input("Enter new card number: ")
            card_holder = input("Enter new card holder name: ")
            expiry_date = input("Enter new expiry date: ")
            cvv = input("Enter new CVV: ")
            # Update the user's payment details
            current_user.payment_details = {
                'card_number': card_number,
                'card_holder': card_holder,
                'expiry_date': expiry_date,
                'cvv': cvv
            }
            # Save the updated details
            current_user.save_to_file()
            print("Payment details updated successfully.")
            confirm_payment(current_user)
        elif choice == '2':
            main_menu()
        elif choice == '3':
            print("You have been signed out.")
            main_menu()
        return  # Return to exit the function after handling the choices

    # If payment details exist, ask if the user wants to proceed
    print("\nDo you want to proceed with these payment details?")
    print("1. Yes, confirm and proceed to checkout")
    print("2. No, return to payment options")
    choice = input("Enter your choice: ")
    if choice == '1':
        # Generate a random 8-digit tracking number
        tracking_number = ''.join([str(random.randint(0, 9)) for _ in range(8)])
        # Code to confirm the payment and finalize the order
        print(f"Payment confirmed. Order placed successfully. Thanks for Shopping with us! Your tracking number is {tracking_number}.")
        # Provide options for the next steps
        print("1. Return to home page")
        print("2. Sign out")
        choice = input("Enter your choice: ")
        if choice == '1':
            after_login()  # Return to the after login menu
        elif choice == '2':
            print("You have been signed out.")
            main_menu()
    elif choice == '2':
        pay(current_user)  # Return to the payment options

def confirm_payment(current_user):
    # Confirm the payment details with the user
    print("\nPlease review your payment details:")
    if hasattr(current_user, 'payment_details') and current_user.payment_details:
        print(f"Card Number: {current_user.payment_details.get('card_number', 'Not available')}")
        print(f"Card Holder: {current_user.payment_details.get('card_holder', 'Not available')}")
        print(f"Expiry Date: {current_user.payment_details.get('expiry_date', 'Not available')}")
        print(f"CVV: {current_user.payment_details.get('cvv', 'Not available')}")
    else:
        print("Payment details are not available or not in the correct format.")

    # Ask the user if they want to proceed with these payment details
    print("\nDo you want to proceed with these payment details?")
    print("1. Yes, confirm and proceed to checkout")
    print("2. No, return to payment options")
    choice = input("Enter your choice: ")
    if choice == '1':
        # Generate a random 8-digit tracking number
        tracking_number = ''.join([str(random.randint(0, 9)) for _ in range(8)])
        # Code to confirm the payment and finalize the order
        print(f"Payment confirmed. Order placed successfully. Thanks for Shopping with us! Your tracking number is {tracking_number}.")
        # Provide options for the next steps
        print("1. Return to home page")
        print("2. Sign out")
        choice = input("Enter your choice: ")
        if choice == '1':
            after_login()  # Return to the after login menu
        elif choice == '2':
            main_menu()  # Return to the main menu
    elif choice == '2':
        pay(current_user)  # Return to the payment options

if __name__ == "__main__":
    print("Debug: __name__ == '__main__'")  # Debugging print statement
    main_menu()
