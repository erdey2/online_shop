from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Cart, CartItem
from .serializers import CartItemSerializer
from drf_spectacular.utils import extend_schema, OpenApiResponse

def get_user_cart(user):
    if user.is_authenticated:
        cart, _ = Cart.objects.get_or_create(user=user)
        return cart
    return None  # Anonymous users don’t get a DB cart

class CartItemListView(generics.ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = CartItemSerializer

    def get_queryset(self):
        cart = get_user_cart(self.request.user)
        if cart:
            return cart.items.select_related('products')
        return []

    @extend_schema(
        tags=["Cart"],
        summary="List Cart Items",
        description="Returns the current user's cart items with products details.",
        responses={200: CartItemSerializer(many=True)},
    )
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

class AddToCartView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        tags=["Cart"],
        summary="Add Product to Cart",
        description="Adds a products to the authenticated user's cart. If the products already exists, its quantity will be updated.",
        request=CartItemSerializer,
        responses={
            201: CartItemSerializer,
            400: OpenApiResponse(description="Invalid input data"),
        },
    )
    def post(self, request):
        cart = get_user_cart(request.user)
        serializer = CartItemSerializer(data=request.data)
        if serializer.is_valid():
            product = serializer.validated_data['products']
            quantity = serializer.validated_data['quantity']
            item, created = CartItem.objects.get_or_create(cart=cart, product=product)
            if not created:
                item.quantity += quantity
            else:
                item.quantity = quantity
            item.save()
            return Response(CartItemSerializer(item).data, status=201)
        return Response(serializer.errors, status=400)

class UpdateCartItemView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CartItemSerializer

    def get_queryset(self):
        cart = get_user_cart(self.request.user)
        return cart.items.all()

    @extend_schema(
        tags=["Cart"],
        summary="partial Update Cart Item",
        description="Updates the quantity of an existing item in the user's cart.",
        request=CartItemSerializer,
        responses={
            200: CartItemSerializer,
            400: OpenApiResponse(description="Invalid data"),
            404: OpenApiResponse(description="Cart item not found"),
        },
    )
    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    @extend_schema(
        tags=["Cart"],
        summary="Full Update Cart Item",
        description="Updates the product in the user's cart.",
        request=CartItemSerializer,
        responses={
            200: CartItemSerializer,
            400: OpenApiResponse(description="Invalid data"),
            404: OpenApiResponse(description="Cart item not found"),
        },
    )
    def put(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

class RemoveFromCartView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        cart = get_user_cart(self.request.user)
        return cart.items.all()

    @extend_schema(
        tags=["Cart"],
        summary="Remove item from cart",
        description="Deletes a specific item from the user's cart based on the item ID.",
        responses={
            204: OpenApiResponse(description="Item successfully removed from cart"),
            404: OpenApiResponse(description="Cart item not found"),
        },
    )
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


