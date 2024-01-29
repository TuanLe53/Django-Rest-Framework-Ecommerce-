from django.db import models
import uuid
from auth_api.models import CustomUser
from user.models import PaymentMethod, Address
from product.models import Product

# Create your models here.
class Order(models.Model):
    status_choices = (
        ("processing","Processing"),
        ("delivering", "Delivering"),
        ("received", "Received"),
    )
    
    id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, primary_key=True)
    created_by = models.ForeignKey(CustomUser, related_name="order", on_delete=models.CASCADE)
    payment = models.ForeignKey(PaymentMethod, on_delete=models.SET_NULL, related_name="order", null=True)
    address = models.ForeignKey(Address, on_delete=models.SET_NULL, related_name="order", null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=15, decimal_places=3)
    status = models.CharField(max_length=25, choices=status_choices)
    
class OrderItem(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, primary_key=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="ordered")
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    quantity = models.IntegerField()
    total_price = models.DecimalField(max_digits=15, decimal_places=3)
    created_at = models.DateTimeField(auto_now_add=True)