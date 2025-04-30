from django.urls import path
from .views import (
    CartItemListView, AddToCartView, UpdateCartItemView, RemoveFromCartView
)

urlpatterns = [
    path('', CartItemListView.as_view(), name='cart-list'),
    path('add/', AddToCartView.as_view(), name='cart-add'),
    path('<int:pk>/update/', UpdateCartItemView.as_view(), name='cart-update'),
    path('<int:pk>/remove/', RemoveFromCartView.as_view(), name='cart-remove'),
]