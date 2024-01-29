from rest_framework.response import Response
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from auth_api.models import CustomUser
from .models import Address, CartItem, PaymentMethod, PaymentType
from .serializers import AddressSerializer, CartItemSerializer, CreatePaymentSerializer, GetPaymentSerializer
from utils.permissions import IsOwner
from datetime import datetime

# Create your views here.
class AddressesView(generics.ListCreateAPIView):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer
    permission_classes = [IsAuthenticated, ]
    
    def get_queryset(self):
        user = self.request.user
        return Address.objects.filter(created_by=user)
    
    def post(self, request):
        user = CustomUser.objects.get(id=request.user.id)
        serializer = AddressSerializer(data=request.data)

        if serializer.is_valid():
            #add user to serializer
            serializer.save(created_by = user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
class AddressView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = AddressSerializer
    queryset = Address.objects.all()
    permission_classes = [IsAuthenticated, IsOwner]
    
class CartView(generics.ListCreateAPIView):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated, ]
    
    def get_queryset(self):
        user = self.request.user
        return CartItem.objects.filter(created_by=user)
    
    def post(self, request):
        user = CustomUser.objects.get(id=request.user.id)
        serializer = CartItemSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(created_by=user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
class CartItemView(generics.DestroyAPIView):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated, IsOwner]
    
class Payments(generics.ListCreateAPIView):
    queryset = PaymentMethod.objects.all()
    permission_classes = [IsAuthenticated, ]
    
    def get_serializer_class(self):
        if self.request.method == "GET":
            return GetPaymentSerializer
        return CreatePaymentSerializer
        
    
    def get_queryset(self):
        user = self.request.user
        return PaymentMethod.objects.filter(created_by=user)
    
    def post(self, request):
        user = CustomUser.objects.get(id=request.user.id)
        payment_type = PaymentType.objects.get(name=request.data["payment_type"])
        
        request.data["payment_type"] = payment_type.id
        request.data["expiry_date"] = datetime.strptime(request.data["expiry_date"], "%m-%y")
        
        serializer = CreatePaymentSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save(created_by=user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)