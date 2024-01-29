from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.pagination import LimitOffsetPagination
from .models import Product, ProductImages, Inventory, Category, Review
from .serializers import ProductSerializer, InventorySerializer, ReviewSerializer
from utils.permissions import IsOwner, IsInventoryOwner
from auth_api.models import CustomUser

# Create your views here.
class ProductsView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    parser_classes = [MultiPartParser]
    pagination_class = LimitOffsetPagination
    
    def get_permissions(self):
        if self.request.method == "GET":
            self.permission_classes = [AllowAny, ]
        else:
            self.permission_classes = [IsAuthenticated, ]
        return super(ProductsView, self).get_permissions()
    
    def post(self, request):
        user = CustomUser.objects.get(id=request.user.id)
        category = Category.objects.get(name=request.data["category"])
        inventory = Inventory.objects.create(quantity=request.data["quantity"])
        serializer = ProductSerializer(data=request.data)

        if serializer.is_valid():
            product = serializer.save(
                created_by = user,
                category = category,
                inventory=inventory
            )
            for file in request.FILES.getlist("images"):
                ProductImages.objects.create(product=product, image=file)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
class ProductByIDView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    parser_classes = [MultiPartParser]
    
    def get_permissions(self):
        if self.request.method == "GET":
            self.permission_classes = [AllowAny, ]
        else:
            self.permission_classes = [IsAuthenticated, IsOwner]
        
        return super(ProductByIDView, self).get_permissions()

class ProductsByCategory(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [AllowAny, ]
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        category = Category.objects.get(name=self.kwargs["category"])
        return Product.objects.filter(category=category)
    

class InventoryView(generics.UpdateAPIView):
    queryset = Inventory.objects.all()
    serializer_class = InventorySerializer
    permission_classes = [IsAuthenticated, IsInventoryOwner]
    
class CreateReviewView(generics.CreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated, ]

    def post(self, request):
        user = CustomUser.objects.get(id=request.user.id)
        
        serializer = ReviewSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(created_by=user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
class ProductReviews(generics.ListAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [AllowAny, ]
    
    def get_queryset(self):
        product = Product.objects.get(id=self.kwargs["pk"])
        return Review.objects.filter(product=product)