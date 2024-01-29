from django.urls import path
from .views import ProductsView, ProductByIDView, InventoryView, CreateReviewView, ProductReviews, ProductsByCategory

urlpatterns = [
    path("products/", ProductsView.as_view(), name="products"),
    path("products/<str:category>/", ProductsByCategory.as_view(), name="products_by_category"),
    path("product/<uuid:pk>/", ProductByIDView.as_view(), name="product"),
    path("product/review/<uuid:pk>", ProductReviews.as_view(), name="reviews"),
    path("reviews/", CreateReviewView.as_view(), name="review"),
    path("product/inventory/<uuid:pk>/", InventoryView.as_view(), name="inventory"),
]
