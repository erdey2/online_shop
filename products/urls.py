from .views import CategoryListCreateView, CategoryDetailView, ProductListCreateView, ProductDetailView, InventoryListView, UpdateInventoryView
from django.urls import path

urlpatterns = [
    path('categories/', CategoryListCreateView.as_view(), name='category-list-create'),
    path('categories/<int:pk>/', CategoryDetailView.as_view(), name='category-detail'),
    path('', ProductListCreateView.as_view(), name='product-list-create'),
    path('<uuid:pk>/', ProductDetailView.as_view(), name='product-detail'),
    path('inventory/', InventoryListView.as_view(), name='inventory-list'),
    path('inventory/update/<uuid:product_id>/', UpdateInventoryView.as_view(), name="update-inventory"),

]

