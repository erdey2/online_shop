from rest_framework import serializers
from .models import Product, Category, Inventory, ProductImage, ProductTag

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = '__all__'

class ProductTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductTag
        fields = '__all__'

class ProductStockAvailabilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['stock', 'status']

class InventorySerializer(serializers.ModelSerializer):
    product_details = ProductSerializer(source='product', read_only=True)
    stock = serializers.IntegerField()

    class Meta:
        model = Inventory
        fields = ['id', 'product_details', 'stock', 'last_updated']
