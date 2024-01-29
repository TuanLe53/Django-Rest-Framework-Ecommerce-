import uuid
from django.db import models
from auth_api.models import CustomUser
# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name

class Inventory(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    quantity = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add = True)
    last_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.id}: {self.quantity}"

class Product(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4, unique=True)
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="products")
    name = models.CharField(max_length=1024)
    sku = models.CharField()
    description = models.TextField()
    price = models.DecimalField(max_digits=12, decimal_places=3)
    inventory = models.OneToOneField(Inventory, on_delete=models.CASCADE, related_name="product")
    category = models.ForeignKey(Category, related_name="products", on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    
    def get_avg_rating(self):
        if self.reviews.count() == 0:
            return 0

        total_rating = 0
        for review in self.reviews.all():
            total_rating += review.rating
        return total_rating / self.reviews.count()
    
    def __str__(self):
        return self.name
    
class ProductImages(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to="product")
    
    def __str__(self):
        return self.product.name
    
class Review(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4, unique=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="reviews")
    created_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
    rating = models.DecimalField(max_digits=2, decimal_places=1)
    comment = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add = True)
    
    def __str__(self):
        return f"{self.created_by}'s review for {self.product}"