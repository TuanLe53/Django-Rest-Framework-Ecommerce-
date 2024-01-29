from rest_framework import serializers
from .models import ProductImages, Product, Inventory, Review

class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImages
        fields = "__all__"
        
class ProductSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True, read_only=True)
    created_by = serializers.CharField(required=False)
    category = serializers.CharField(required=False)
    inventory = serializers.CharField(required=False)
    rating = serializers.DecimalField(max_digits=2, decimal_places=1, source="get_avg_rating", required=False)
    
    class Meta:
        model = Product
        exclude = ("last_modified", )
        
class InventorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Inventory
        fields = "__all__"
        
class ReviewSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Review
        fields = "__all__"
        extra_kwargs = {
            "created_by": {"required": False}
            }