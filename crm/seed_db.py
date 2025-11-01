# seed_db.py
import os
import django
from datetime import datetime
from random import choice, randint

# ---------------------------
# Setup Django environment
# ---------------------------
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'alx_backend_graphql_crm.settings')
django.setup()

from crm.models import Customer, Product, Order

# ---------------------------
# Seed Customers
# ---------------------------
customers_data = [
    {"name": "Alice Smith", "email": "alice@example.com", "phone": "+1234567890"},
    {"name": "Bob Johnson", "email": "bob@example.com", "phone": "+1987654321"},
    {"name": "Carol Davis", "email": "carol@example.com", "phone": "+1122334455"},
    {"name": "David Lee", "email": "david@example.com", "phone": "+1222333444"},
]

for c in customers_data:
    customer, created = Customer.objects.get_or_create(email=c['email'], defaults=c)
    if created:
        print(f"Created customer: {customer.name}")
    else:
        print(f"Customer already exists: {customer.name}")

# ---------------------------
# Seed Products
# ---------------------------
products_data = [
    {"name": "Laptop", "price": 999.99, "stock": 10},
    {"name": "Smartphone", "price": 499.99, "stock": 20},
    {"name": "Headphones", "price": 79.99, "stock": 50},
    {"name": "Keyboard", "price": 49.99, "stock": 15},
]

for p in products_data:
    product, created = Product.objects.get_or_create(name=p['name'], defaults=p)
    if created:
        print(f"Created product: {product.name}")
    else:
        print(f"Product already exists: {product.name}")

# ---------------------------
# Seed Orders
# ---------------------------
all_customers = list(Customer.objects.all())
all_products = list(Product.objects.all())

for i in range(1, 6):  # Create 5 orders
    customer = choice(all_customers)
    products_in_order = [choice(all_products) for _ in range(randint(1, 3))]
    order = Order(customer=customer)
    order.save()  # Must save before setting many-to-many
    order.products.set(products_in_order)
    order.total_amount = sum([p.price for p in products_in_order])
    order.order_date = datetime.now()
    order.save()
    product_names = ", ".join([p.name for p in products_in_order])
    print(f"Created order {order.id} for {customer.name} with products: {product_names}")

print("Seeding completed successfully!")
