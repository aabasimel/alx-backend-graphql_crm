from django.core.management.base import BaseCommand
from django.db import transaction
from decimal import Decimal
import random
from datetime import datetime,timedelta
from crm.models import Customer, Product, Order,OrderProduct


class Command(BaseCommand):
    help = "Populate the database with sample customers, products, and orders"

    def handle(self, *args, **options):
        self.stdout.write("Starting database population...")

        customers = self._populate_customers()
        products = self._populate_products()
        self._populate_orders(customers, products)
        self.stdout.write(self.style.SUCCESS("Database successfully populated"))

    @transaction.atomic
    def _populate_customers(self):
        data = [
            {"name": "Alice Johnson", "email": "alice@example.com", "phone": "+4915123456789"},
            {"name": "Bob Smith", "email": "bob@example.com", "phone": "123-456-7890"},
            {"name": "Charlie Brown", "email": "charlie@example.com", "phone": "+447700900123"},
            {"name": "Diana Prince", "email": "diana@example.com", "phone": "456-789-0123"},
        ]
        customers = []
        for c in data:
            obj, _ = Customer.objects.get_or_create(email=c["email"], defaults=c)
            customers.append(obj)
        self.stdout.write(self.style.SUCCESS(f"Added {len(customers)} customers"))
        return customers

    @transaction.atomic
    def _populate_products(self):
        data = [
            {"name": "Laptop", "price": Decimal("899.99"), "stock": 10},
            {"name": "Smartphone", "price": Decimal("699.99"), "stock": 25},
            {"name": "Headphones", "price": Decimal("149.99"), "stock": 40},
            {"name": "Monitor", "price": Decimal("299.99"), "stock": 15},
            {"name": "Keyboard", "price": Decimal("89.99"), "stock": 30},
        ]
        products = []
        for p in data:
            obj, _ = Product.objects.get_or_create(name=p["name"], defaults=p)
            products.append(obj)
        self.stdout.write(self.style.SUCCESS(f"Added {len(products)} products"))
        return products

    @transaction.atomic
    def _populate_orders(self, customers, products):

        statuses = [Order.StatusChoices.PENDING,
                Order.StatusChoices.CONFIRMED,
                Order.StatusChoices.CANCELLED]
        
        for _ in range(5):
            customer = random.choice(customers)
            status=random.choice(statuses)
            days_ago = random.randint(7, 30)
            order_date = datetime.now() - timedelta(days=days_ago)

            order = Order.objects.create(
            customer=customer,
            status=status,
            order_date=order_date  # assign the generated past date
        )

            
            selected_products = random.sample(products, random.randint(2, 4))

            for p in selected_products:
                quantity=random.randint(1,5)
                OrderProduct.objects.create(order=order,product=p,quantity=quantity)
            order.calculate_total_amount()
        self.stdout.write(self.style.SUCCESS("Added 5 random orders."))
