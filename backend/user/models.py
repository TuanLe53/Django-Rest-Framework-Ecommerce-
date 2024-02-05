import uuid
from utils.rand_name import rand_name
from django.db import models
from django.core.validators import RegexValidator
from auth_api.models import CustomUser
from product.models import Product

# Create your models here.
phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
class Address(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="address")
    name = models.CharField(max_length=1024, default=rand_name)
    city = models.CharField(max_length=255)
    address = models.CharField(max_length=1024)
    phone_number = models.CharField(validators=[phone_regex], max_length=17)
    is_default = models.BooleanField(default=False)
    
class CartItem(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    created_by =  models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="cart")
    created_at = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)


payment_types = (
    ("paypal", "Paypal"),
    ("cod", "COD"),
)
class PaymentType(models.Model):
    name = models.CharField(max_length=25, choices=payment_types)
    
    def __str__(self):
        return self.name
    
provider_options = (
    ("visa", "Visa"),
    ("mastercard", "Mastercard")
)
class PaymentMethod(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    created_by = models.ForeignKey(CustomUser, related_name="payment_method", on_delete=models.CASCADE)
    payment_type = models.ForeignKey(PaymentType, on_delete=models.CASCADE, related_name="type")
    provider = models.CharField(max_length=125, choices=provider_options)
    account_number = models.CharField()
    expiry_date = models.DateTimeField()
    is_default = models.BooleanField(default=False)
