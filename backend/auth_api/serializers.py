from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import Token
from .models import CustomUser

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user: CustomUser) -> Token:
        token = super().get_token(user)
        
        #Add user data
        token["username"] = user.username
        token["email"] = user.email
        
        return token

class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=CustomUser.objects.all())]
    )
    
    class Meta:
        model = CustomUser
        fields = ("email", "password", "username")
        extra_kwargs = {"password": {"write_only": True}}
        read_only_fields = ("username", )
        
    def create(self, validated_data):
        user = CustomUser.objects.create(
            email = validated_data["email"],
        )
        
        user.set_password(validated_data["password"])
        user.save()
        
        return user