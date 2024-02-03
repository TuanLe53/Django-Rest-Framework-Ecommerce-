from rest_framework import serializers
from .models import Address, CartItem, PaymentMethod
from product.serializers import ProductSerializer

class AddressSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Address
        fields = "__all__"
        extra_kwargs = {
            "name": {"required": False},
            "created_by": {"required": False}
        }
        
class AddCartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = "__all__"
        extra_kwargs = {
            "created_by": {"required": False}
        }

class GetCartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer()
    class Meta:
        model = CartItem
        fields = "__all__"
        extra_kwargs = {
            "created_by": {"required": False}
        }
        
class CreatePaymentSerializer(serializers.ModelSerializer):   
     
    class Meta:
        model = PaymentMethod
        fields = "__all__"
        extra_kwargs = {
            "created_by": {"required": False},
            "is_default": {"required": False}
        }
        
class GetPaymentSerializer(serializers.ModelSerializer):
    payment_type = serializers.CharField(source="payment_type.name", read_only=True)
    
    class Meta:
        model = PaymentMethod
        fields = "__all__"