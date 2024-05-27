#PythonAddProduct.py

initial_products = [
    "iPhone 14 Pro Max, 1400.0",
    "iPhone 14, 1200.0",
    "Samsung S22 Ultra, 900.0",
    "Samsung S22, 800.0",
    "Samsung S20, 700.0",
    "Samsung A55, 600.0"
]

with open('products.txt', 'w') as file:
    for product in initial_products:
        file.write(product + "\n")


class Product:
    def __init__(self, name, price):
        self.name = name
        self.price = price

class ProductList:
    def __init__(self):
        self.products = []

    def add_product(self, product):
        self.products.append(product)

    def save_to_file(self, filename):
        with open(filename, 'a') as file:
            for product in self.products:
                file.write(f'{product.name}, {product.price}\n')

# Function to add products through CLI
def add_products_cli():
    product_list = ProductList()
    while True:
        name = input("Enter product name (or type 'exit' to finish): ")
        if name.lower() == 'exit':
            break
        price = float(input("Enter product price ($): "))
        product = Product(name, price)
        product_list.add_product(product)
        print(f"Added: {product.name} - ${product.price}")

    return product_list

# Run the function to start adding products
product_list = add_products_cli()

# Save the product list to a file
product_list.save_to_file('products.txt')

# Display the product list
for product in product_list.products:
    print(f'Product Name: {product.name}, Price: ${product.price}')



