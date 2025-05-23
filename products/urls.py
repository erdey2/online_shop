from .views import (CategoryListCreateView, CategoryDetailView, ProductListCreateView, ProductDetailView,
                    UpdateInventoryView, LowStockProductsView, ProductImageListView, ProductImageDetailView,
                    ProductTagListView, ProductTagDetailView, ProductAvailabilityView, PriceHistoryView)

from django.urls import path

urlpatterns = [
    path('', ProductListCreateView.as_view(), name='product-list-create'),
    path('<uuid:pk>/', ProductDetailView.as_view(), name='products-detail'),

    path('categories/', CategoryListCreateView.as_view(), name='category-list-create'),
    path('categories/<uuid:pk>/', CategoryDetailView.as_view(), name='category-detail'),

    path('images/', ProductImageListView.as_view(), name='products-images'),
    path('images/<uuid:pk>/', ProductImageDetailView.as_view(), name='products-images'),
    
    path('tags/', ProductTagListView.as_view(), name='tag-list'),
    path('tags/<uuid:pk>/', ProductTagDetailView.as_view(), name='tag-details'),

    path('<uuid:product_id>/update-inventory/', UpdateInventoryView.as_view(), name='update-inventory'),

    path('low-stock', LowStockProductsView.as_view(), name='low_stock'),
    path('<uuid:product_id>/availability/', ProductAvailabilityView.as_view(), name='products-availability'),
    path('<uuid:product_id>/price-history/', PriceHistoryView.as_view(), name='price-history'),

]

