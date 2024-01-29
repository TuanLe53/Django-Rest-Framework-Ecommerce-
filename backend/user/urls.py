from django.urls import path
from .views import AddressesView, AddressView, CartItemView, CartView, Payments

urlpatterns = [
    path("addresses/", AddressesView.as_view(), name="addresses"),
    path("address/<uuid:pk>/", AddressView.as_view(), name="address"),
    path("cart/", CartView.as_view(), name="cart"),
    path("cart-item/<uuid:pk>/", CartItemView.as_view(), name="cart_item"),
    path("payments/", Payments.as_view(), name="payments")
]

