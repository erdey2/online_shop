from .views import (CategoryListCreateView, CategoryDetailView, ProductListCreateView, ProductDetailView,
                    UpdateInventoryView, LowStockProductsView, ProductImageListView, ProductImageDetailView,
                    ProductTagListView, ProductTagDetailView, ProductAvailabilityView)

from django.urls import path

urlpatterns = [
    path('categories/', CategoryListCreateView.as_view(), name='category-list-create'),
    path('categories/<int:pk>/', CategoryDetailView.as_view(), name='category-detail'),
    path('', ProductListCreateView.as_view(), name='product-list-create'),
    path('<uuid:pk>/', ProductDetailView.as_view(), name='product-detail'),
    path('images/', ProductImageListView.as_view(), name='product-images'),
    path('images/<uuid:pk>/', ProductImageDetailView.as_view(), name='product-images'),
    path('tags/', ProductTagListView.as_view(), name='tag-list'),
    path('tags/<uuid:pk>/', ProductTagDetailView.as_view(), name='tag-details'),
    path('update-inventory/<uuid:product_id>/', UpdateInventoryView.as_view(), name='update-inventory'),
    path('low-stock', LowStockProductsView.as_view(), name='low_stock'),
    path('availability/', ProductAvailabilityView.as_view(), name='product_availability')

]

