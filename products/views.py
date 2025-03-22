from rest_framework import generics
from .models import Product, Category, Inventory
from .serializers import ProductSerializer, CategorySerializer, InventorySerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

# Category Views
class CategoryListCreateView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class CategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

# Product Views
class ProductListCreateView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

# Inventory Views
class InventoryListView(generics.ListAPIView):
    queryset = Inventory.objects.all()
    serializer_class = InventorySerializer

class UpdateInventoryView(APIView):
    def post(self, request, product_id):
        try:
            inventory = Inventory.objects.get(product_id=product_id)
            new_stock = request.data.get("stock", inventory.stock)
            inventory.stock = new_stock
            inventory.save()
            return Response({"message": "Stock updated successfully!"}, status=status.HTTP_200_OK)
        except Inventory.DoesNotExist:
            return Response({"error": "Product not found in inventory"}, status=status.HTTP_404_NOT_FOUND)
