from rest_framework import generics
from .models import Product, Category, Inventory
from .serializers import ProductSerializer, CategorySerializer, InventorySerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema, OpenApiParameter

# Category Views
class CategoryListCreateView(generics.ListCreateAPIView):
    serializer_class = CategorySerializer

    def get_queryset(self):
        qs = Category.objects.all()
        name = self.request.GET.get('name')

        if name:
            qs = qs.filter(name__icontains=name)
        return qs

    @extend_schema(
        summary="List Categories",
        description="Retrieve a list of all product categories. You can filter categories by name.",
        parameters=[
            OpenApiParameter(
                name="name",
                description="Filter categories by name (case-insensitive)",
                required=False,
                type=str
            ),
        ],
        responses={200: CategorySerializer(many=True)},

    )
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    @extend_schema(
        summary="Create a New Category",
        description="Create a new category by providing category details.",
        request=CategorySerializer,
        responses={201: CategorySerializer},
    )
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

class CategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    @extend_schema(
        summary="Retrieve a Category",
        description="Fetch a single category by its ID.",
        responses={200: CategorySerializer},
    )
    def get(self, request, *args, **kwargs):
        self.retrieve(request, *args, **kwargs)

    @extend_schema(
        summary="Update a Category",
        description="Fully update a category by replacing all its fields.",
        request=CategorySerializer,
        responses={200: CategorySerializer},
    )
    def put(self, request, *args, **kwargs):
        self.update(request, *args, **kwargs)

    @extend_schema(
        summary="Partially Update a Category",
        description="Partially update a category with only the provided fields.",
        request=CategorySerializer,
        responses={200: CategorySerializer},
    )
    def patch(self, request, *args, **kwargs):
        self.partial_update(request, *args, **kwargs)

    @extend_schema(
        summary="Delete a Category",
        description="Delete a category by its ID.",
        responses={204: None},
    )
    def delete(self, request, *args, **kwargs):
        self.destroy(request, *args, **kwargs)

# Product Views
class ProductListCreateView(generics.ListCreateAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        qs = Product.objects.all()
        title = self.request.GET.get('title')
        category = self.request.GET.get('category')
        price = self.request.GET.get('price')
        stock = self.request.GET.get('stock')

        if title:
            qs = qs.filter(name__icontains=title)
        if category:
            qs = qs.filter(category__icontains=category)
        if price:
            qs = qs.filter(price__lte=price)
        if stock:
            qs = qs.filter(stock__lte=stock)
        return qs

    @extend_schema(
        summary="List all Products",
        description="Retrieve a list of products with optional filters for title, category, price, and stock.",
        parameters=[
            OpenApiParameter(name="title", description="Filter by product title", required=False, type=str),
            OpenApiParameter(name="category", description="Filter by category", required=False, type=str),
            OpenApiParameter(name="price", description="Filter products below a price", required=False, type=float),
            OpenApiParameter(name="stock", description="Filter products with stock below a value", required=False, type=int),
        ],
        responses={200: ProductSerializer(many=True)},

    )
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    @extend_schema(
        summary="Create a New Product",
        description="Add a new product to the inventory.",
        request=ProductSerializer,
        responses={201: ProductSerializer},
    )
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    @extend_schema(
        summary="Retrieve a Product",
        description="Get detailed information about a single product by its ID.",
        responses={200: ProductSerializer},
    )
    def get(self, request, *args, **kwargs):
        self.retrieve(request, *args, **kwargs)

    @extend_schema(
        summary="Update a Product",
        description="Replace the entire product record with new data.",
        request=ProductSerializer,
        responses={200: ProductSerializer},
    )
    def put(self, request, *args, **kwargs):
        self.update(request, *args, **kwargs)

    @extend_schema(
        summary="Partially Update a Product",
        description="Update specific fields of a product without modifying the entire record.",
        request=ProductSerializer,
        responses={200: ProductSerializer},
    )
    def patch(self, request, *args, **kwargs):
        self.update(request, *args, **kwargs)

    @extend_schema(
        summary="Delete a Product",
        description="Remove a product from the database by its ID.",
        responses={204: None},
    )
    def delete(self, request, *args, **kwargs):
        self.destroy(request, *args, **kwargs)

# Inventory Views
class InventoryListView(generics.ListAPIView):
    """ List all inventory items. """
    queryset = Inventory.objects.all()
    serializer_class = InventorySerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

class UpdateInventoryView(APIView):
    """ Update stock for a specific product in the inventory."""
    @extend_schema(
        summary="Update Inventory Stock",
        description="Update the stock level of a specific product using its product_id.",
        request={
            "application/json": {
                "example": {"stock": 20}
            }
        },
        responses={
            200: {"example": {"message": "Stock updated successfully!"}},
            404: {"example": {"error": "Product not found in inventory"}},
        },
    )
    def post(self, request, product_id):
        try:
            inventory = Inventory.objects.get(product_id=product_id)
            new_stock = request.data.get("stock", inventory.stock)
            inventory.stock = new_stock
            inventory.save()
            return Response({"message": "Stock updated successfully!"}, status=status.HTTP_200_OK)
        except Inventory.DoesNotExist:
            return Response({"error": "Product not found in inventory"}, status=status.HTTP_404_NOT_FOUND)
