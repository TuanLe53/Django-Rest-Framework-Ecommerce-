from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .serializers import OrderSerializer
from auth_api.models import CustomUser
from product.models import Product
from user.models import Address, PaymentMethod
from .models import Order, OrderItem

# Create your views here.
class OrderView(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated, ]
    
    def get_queryset(self):
        user = self.request.user
        return Order.objects.filter(created_by=user)
    
    def post(self, request):
        user = CustomUser.objects.get(id=request.user.id)
        try:
            payment = PaymentMethod.objects.get(id=request.data["payment"])
            address = Address.objects.get(id=request.data["address"])
            
            order = Order.objects.create(
                created_by = user,
                payment = payment,
                address = address,
                status = "processing",
                total_price = 0
            )
            
            total_price = 0
            pd_list = request.data["products"]
            for item in pd_list:
                pd = Product.objects.get(id=item["product_id"])
                order_pd_price = pd.price * item["quantity"]
                
                order_pd = OrderItem.objects.create(
                    product = pd,
                    order = order,
                    quantity = item["quantity"],
                    total_price = order_pd_price
                )
                
                total_price += order_pd_price
                
            order.total_price = total_price
            order.save()
            
            print(order.total_price)
            
            serializer= OrderSerializer(order)
            
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"Error": f"Missing field {e}"}, status=status.HTTP_400_BAD_REQUEST)