from re import search
from unicodedata import category
from django.db.models import Q
from drf_spectacular.types import OpenApiTypes
from rest_framework import generics
from .models import Product, Category, Inventory, ProductImage, ProductTag, ProductPriceHistory
from .serializers import (ProductSerializer, CategorySerializer, InventorySerializer, ProductImageSerializer,
                          ProductTagSerializer, ProductStockAvailabilitySerializer, ProductPriceHistorySerializer)
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample, OpenApiResponse
from django.db.models.signals import post_save
from django.dispatch import receiver
from uuid import UUID

# Category Views
class CategoryListCreateView(generics.ListCreateAPIView):
    """ List all categories or create a new one."""
    serializer_class = CategorySerializer

    def get_queryset(self):
        qs = Category.objects.all()
        title = self.request.GET.get('title')

        if title:
            qs = qs.filter(name__icontains=title)
        return qs

    @extend_schema(
        tags=['Category'],
        summary="List Categories",
        description="Retrieve a list of all products categories. You can filter categories by name.",
        parameters=[
            OpenApiParameter(
                name="title",
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
        tags=['Category'],
        summary="Create a New Category",
        description="Create a new category by providing category details.",
        request=CategorySerializer,
        responses={201: CategorySerializer},
    )
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

class CategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    """ Retrieve, update, or delete a category."""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    @extend_schema(
        tags=['Category'],
        summary="Retrieve a Category",
        description="Fetch a single category by its ID.",
        responses={200: CategorySerializer},
    )
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    @extend_schema(
        tags=['Category'],
        summary="Update a Category",
        description="Fully update a category by replacing all its fields.",
        request=CategorySerializer,
        responses={200: CategorySerializer},
    )
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    @extend_schema(
        tags=['Category'],
        summary="Partially Update a Category",
        description="Partially update a category with only the provided fields.",
        request=CategorySerializer,
        responses={200: CategorySerializer},
    )
    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    @extend_schema(
        tags=['Category'],
        summary="Delete a Category",
        description="Delete a category by its ID.",
        responses={204: None},
    )
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

# Product Views
class ProductListCreateView(generics.ListCreateAPIView):
    """ List all products or create a new one"""
    serializer_class = ProductSerializer

    def get_queryset(self):
        qs = Product.objects.all()

        # Get the search parameters from the request
        query = self.request.GET.get('search')

        if query:
            search_conditions = Q(title__icontains=query) | Q(category__icontains=query) | Q(price__lte=query) | Q(stock__lte=query)
            qs = qs.filter(search_conditions)

        return qs

    @extend_schema(
        tags=["Product"],
        summary="List Products",
        description="Retrieve a list of products. You can optionally filter products using the `search` query parameter. "
                    "It will match title, category, price (less than or equal), or stock (less than or equal).",
        parameters=[
            OpenApiParameter(
                name='search',
                type=str,
                location=OpenApiParameter.QUERY,
                description="Search string to filter products by title, category, price, or stock. Example: `?search=shoes` or `?search=100`."
            ),
        ],
        responses={200: ProductSerializer(many=True)},
    )
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    @extend_schema(
        tags=["Product"],
        summary="Create a New Product",
        description="Create a new products by providing the required fields (e.g., title, category, price, stock, etc.).",
        request=ProductSerializer,
        responses={201: ProductSerializer}
    )
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    """ Retrieve, update, or delete a products."""
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    @extend_schema(
        tags=['Product'],
        summary="Retrieve a Product",
        description="Get detailed information about a single products by its ID.",
        responses={200: ProductSerializer},
    )
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    @extend_schema(
        tags=['Product'],
        summary="Update a Product",
        description="Replace the entire products record with new data.",
        request=ProductSerializer,
        responses={200: ProductSerializer},
    )
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    @extend_schema(
        tags=['Product'],
        summary="Partially Update a Product",
        description="Update specific fields of a products without modifying the entire record.",
        request=ProductSerializer,
        responses={200: ProductSerializer},
    )
    def patch(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    @extend_schema(
        tags=['Product'],
        summary="Delete a Product",
        description="Remove a products from the database by its ID.",
        responses={204: None},
    )
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

class ProductImageListView(generics.ListCreateAPIView):
    """Endpoint to list and create products images. """
    serializer_class = ProductImageSerializer
    queryset = ProductImage.objects.all()

    @extend_schema(
        tags = ['Product Image'],
        operation_id="list_product_images",
        responses=ProductImageSerializer(many=True),
        parameters=[
            OpenApiParameter('product_id', type=str, description='The UUID of the products to filter images by',
                             required=False)
        ]
    )
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    @extend_schema(
        tags=['Product Image'],
        operation_id="create_product_image",
        request=ProductImageSerializer,
        responses=OpenApiResponse(response=ProductImageSerializer)
    )
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

class ProductImageDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Endpoint to retrieve, update, partially update or delete products images. """
    @extend_schema(
        tags=['Product Image'],
        operation_id="get_product_image",
        responses=ProductImageSerializer,
        description="Retrieve a single products image by its ID."
    )
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    @extend_schema(
        tags=['Product Image'],
        operation_id="update_product_image",
        request=ProductImageSerializer,
        responses=OpenApiResponse(response=ProductImageSerializer),
        description="Update a products image."
    )
    def put(self, request, *args, **kwargs):
        return self.put(request, *args, **kwargs)

    @extend_schema(
        tags=['Product Image'],
        operation_id="partial_update_product_image",
        request=ProductImageSerializer,
        responses=OpenApiResponse(response=ProductImageSerializer),
        description="Partially update a products image."
    )
    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    @extend_schema(
        tags=['Product Image'],
        operation_id="delete_product_image",
        responses=OpenApiResponse(response=None),
        description="Delete a products image."
    )
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

class ProductTagListView(generics.ListCreateAPIView):
    """List all products tags or create a new one. """
    serializer_class = ProductTagSerializer
    queryset = ProductTag.objects.all()

    @extend_schema(
        tags=['Product Tag'],
        summary="List Product Tags",
        description="Retrieve a list of all available products tags.",
        responses={200: ProductTagSerializer(many=True)},
    )
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    @extend_schema(
        tags=['Product Tag'],
        summary="Create Product Tag",
        description="Create a new products tag by providing necessary fields.",
        request=ProductTagSerializer,
        responses={201: ProductTagSerializer},
    )
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

class ProductTagDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update, or delete a products tag by ID. """
    serializer_class = ProductTagSerializer
    queryset = ProductTag.objects.all()

    @extend_schema(
        tags=['Product Tag'],
        summary="Retrieve Product Tag",
        description="Get a single products tag by its ID.",
        responses={200: ProductTagSerializer},
    )
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    @extend_schema(
        tags=['Product Tag'],
        summary="Update Product Tag",
        description="Update a products tag by providing all fields.",
        request=ProductTagSerializer,
        responses={200: ProductTagSerializer},
    )
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    @extend_schema(
        tags=['Product Tag'],
        summary="Partially Update Product Tag",
        description="Update a products tag by providing only the fields to change.",
        request=ProductTagSerializer,
        responses={200: ProductTagSerializer},
    )
    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    @extend_schema(
        tags=['Product Tag'],
        summary="Delete Product Tag",
        description="Delete a products tag by its ID.",
        responses={204: None},
    )
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

class PriceHistoryView(generics.ListAPIView):
    """Return the price history of a products given its ID."""
    serializer_classes = ProductPriceHistorySerializer

    def get_queryset(self):
        product_id = self.kwargs.get('product_id')
        return ProductPriceHistory.objects.filter(product_id=product_id).order_by('updated_at')

    @extend_schema(
        tags=['Price History'],
        summary="List products price history",
        description="Returns a list of historical price changes for a given products ID.",
        parameters=[
            OpenApiParameter(
                name='product_id',
                type=int,
                location=OpenApiParameter.PATH,
                description='ID of the products'
            )
        ],
        responses=ProductPriceHistorySerializer(many=True),
    )
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

# Inventory Views
class UpdateInventoryView(APIView):
    """ Update stock for a specific products in the inventory."""
    @extend_schema(
        tags=['Inventory'],
        summary="Update Inventory Stock",
        description="Update the stock level of a specific products using its product_id.",
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
    def patch(self, request, product_id):
        try:
            inventory = Inventory.objects.get(product_id=product_id)
            new_stock = request.data.get("stock", inventory.stock)
            inventory.stock = new_stock
            inventory.save()
            return Response({"message": "Stock updated successfully!"}, status=status.HTTP_200_OK)
        except Inventory.DoesNotExist:
            return Response({"error": "Product not found in inventory"}, status=status.HTTP_404_NOT_FOUND)


class ProductAvailabilityView(APIView):
    """Check products availability by products ID """
    @extend_schema(
        tags=["Product"],
        summary="Check Product Availability",
        description="Retrieve availability and details of a products by providing its ID.",
        responses={
            200: OpenApiResponse(response=ProductStockAvailabilitySerializer, description='Product data retrieved successfully'),
            404: OpenApiResponse(description='Product not found')
        },
    )
    def get(self, request, product_id):
        try:
            product = Product.objects.get(id=product_id)
            serializer = ProductSerializer(product)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Product.DoesNotExist:
            return Response({'detail': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)

class LowStockProductsView(APIView):
    """Returns a list of products with inventory below the stock threshold. """
    @extend_schema(
        tags=['Product'],
        summary="Low Stock Products",
        description="Returns all inventory items with stock below the threshold (default is 15).",
        parameters=[
            OpenApiParameter(
                name='threshold',
                description='Stock threshold to filter low-stock products',
                required=False,
                type=int
            )
        ],
        responses={
            200: InventorySerializer(many=True)
        },
        examples=[
            OpenApiExample(
                "Low stock response example",
                value=[
                    {
                        "id": 4,
                        "product_details": {
                            "id": "3cf835f8-fb50-471d-8dce-c9647dfea984",
                            "title": "Book",
                            "description": "The power of mind",
                            "price": "450.00",
                            "stock": 10,
                            "image": None,
                            "created_at": "2025-04-04T12:01:50.993428Z",
                            "updated_at": "2025-04-04T12:01:50.993445Z",
                            "category": "428ad45c-2698-40c0-889b-8633a2742189"
                        },
                        "stock": 10,
                        "last_updated": "2025-04-04T12:58:13.728500Z"
                    }
                ]
            )
        ]

    )
    def get(self, request):
        threshold = 15  # Or dynamic
        low_stock_items = Inventory.objects.filter(stock__lt=threshold)
        serializer = InventorySerializer(low_stock_items, many=True)
        return Response(serializer.data)

@receiver(post_save, sender=Inventory)
def update_product_stock(sender, instance, **kwargs):
    product = instance.product 
    product.stock = instance.stock  # Update products stock to match inventory stock
    product.save()