from django.utils.decorators import method_decorator

from cart.models import Cart, CartItem
from cart.views import get_user_cart
from .models import Order, OrderItem
from .serializers import OrderSerializer, CheckoutSessionRequestSerializer, CheckoutSessionResponseSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics, status
from rest_framework.decorators import api_view
import stripe
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiParameter

# Set the Stripe secret key
stripe.api_key = settings.STRIPE_SECRET_KEY

class PlaceOrderView(APIView):
    """ """

    permission_classes = [IsAuthenticated]

    @extend_schema(
        tags=['Orders'],
        summary="Place an order",
        description="Places an order for the authenticated user based on the current cart items. Clears the cart after order is placed.",
        responses={
            201: OpenApiResponse(response=OrderSerializer, description="Order placed successfully"),
            400: OpenApiResponse(description="Cart is empty")
        }
    )
    def post(self, request):
        cart = get_user_cart(request.user)
        items = cart.items.select_related('products')
        if not items.exists():
            return Response({"error": "Cart is empty"}, status=400)

        total = sum([item.get_total_price() for item in items])
        order = Order.objects.create(user=request.user, total=total)

        for item in items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price
            )

        # Clear cart after order
        items.delete()

        return Response(OrderSerializer(order).data, status=201)

class OrderListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = OrderSerializer

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).prefetch_related('items__product')

    @extend_schema(
        tags=['Orders'],
        summary="List User Orders",
        description="Returns a list of all orders placed by the authenticated user, including related order items and products.",
        responses={200: OpenApiResponse(response=OrderSerializer(many=True), description="List of user orders"), }
    )
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

class CreateCheckoutSessionView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CheckoutSessionRequestSerializer  # just for schema; data comes from URL

    @extend_schema(
        tags=["Orders"],
        summary="Create Stripe Checkout Session",
        description="Creates a Stripe Checkout session for the given order. Only works if the order is in 'pending' status.",
        parameters=[
            OpenApiParameter(
                name='order_id',
                description='ID of the order to create a Stripe session for',
                required=True,
                type=int,
                location=OpenApiParameter.PATH
            ),
        ],
        responses={
            200: OpenApiResponse(description="Checkout session created successfully", response=CheckoutSessionResponseSerializer),
            400: OpenApiResponse(description="Order already processed or invalid"),
            404: OpenApiResponse(description="Order not found"),
        }
    )
    def post(self, request, order_id):
        try:
            order = Order.objects.get(id=order_id, user=request.user)
            if order.status != "pending":
                return Response({"error": "Order already processed"}, status=400)

            line_items = [
                {
                    "price_data": {
                        "currency": "usd",
                        "product_data": {"name": item.product.name},
                        "unit_amount": int(item.price * 100),
                    },
                    "quantity": item.quantity,
                }
                for item in order.items.all()
            ]

            session = stripe.checkout.Session.create(
                payment_method_types=["card"],
                line_items=line_items,
                mode="payment",
                success_url="https://yourdomain.com/success?session_id={CHECKOUT_SESSION_ID}",
                cancel_url="https://yourdomain.com/cancel",
                metadata={"order_id": order.id},
            )
            return Response({"checkout_url": session.url})
        except Order.DoesNotExist:
            return Response({"error": "Order not found"}, status=404)

@method_decorator(csrf_exempt, name='dispatch')
class StripeWebhookView(APIView):
    authentication_classes = []  # no authentication; Stripe sends this
    permission_classes = []

    @extend_schema(
        tags=["Orders"],
        summary="Stripe Webhook Listener",
        description=(
            "Endpoint for handling Stripe webhook events, specifically `checkout.session.completed`. "
            "Validates the event signature and marks the related order as paid if verified."
        ),
        request=None,
        responses={
            200: OpenApiResponse(description="Webhook processed successfully"),
            400: OpenApiResponse(description="Invalid Stripe signature or malformed event"),
        },
    )
    def post(self, request, *args, **kwargs):
        payload = request.body
        sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
        webhook_secret = 'whsec_...'  # Replace with your real webhook secret securely

        try:
            event = stripe.Webhook.construct_event(payload, sig_header, webhook_secret)
        except stripe.error.SignatureVerificationError:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        if event['type'] == 'checkout.session.completed':
            session = event['data']['object']
            order_id = session['metadata'].get('order_id')
            try:
                order = Order.objects.get(id=order_id)
                order.status = 'paid'
                order.save()
            except Order.DoesNotExist:
                pass

        return Response(status=status.HTTP_200_OK)

