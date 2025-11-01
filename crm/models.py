from django.db import models
from django.core.validators import RegexValidator, MinValueValidator


class Customer(models.Model):
    name= models.CharField(max_length=100)
    email=models.EmailField(unique=True)
    phone = models.CharField(
        max_length=20, 
        blank=True, 
        validators=[RegexValidator(
            regex=r'^(\+\d{1,3}[- ]?)?\d{3}[- ]?\d{3}[- ]?\d{4}$',
            message="Phone must be in format +1234567890 or 123-456-7890"
        )]
    )
    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0.01)])
    stock = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name
class Order(models.Model):
    class StatusChoices(models.TextChoices):
        PENDING = 'Pending'
        CONFIRMED = 'Confirmed'
        CANCELLED = 'Cancelled'

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='orders')
    products = models.ManyToManyField(Product, through='OrderProduct',related_name='orders')
    order_date = models.DateTimeField(auto_now_add=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    status = models.CharField(
        max_length=10,
        choices=StatusChoices.choices,
        default=StatusChoices.PENDING
    )

    def calculate_total_amount(self):
        total=sum(op.product.price*op.quantity for op in self.order_products.all())
        self.total_amount=total
        self.save(update_fields=['total_amount'])
        

    def __str__(self):
        return f"Order {self.id} - {self.customer.name}"

class OrderProduct(models.Model):
    order=models.ForeignKey(Order,on_delete=models.CASCADE,related_name='order_products')
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity=models.PositiveIntegerField(default=1)
    def __str__(self):
        return f"{self.product.name} x {self.quantity} for {self.order.id}"
