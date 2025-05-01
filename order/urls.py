from django.urls import path
from .views import PlaceOrderView, OrderListView, CreateCheckoutSessionView, StripeWebhookView

urlpatterns = [
    path('orders/', OrderListView.as_view(), name='order-list'),
    path('orders/place/', PlaceOrderView.as_view(), name='place-order'),
    path('checkout/<int:order_id>/', CreateCheckoutSessionView.as_view(), name='create-checkout-session'),
    path('webhook/', StripeWebhookView.as_view(), name='stripe-webhook'),
]