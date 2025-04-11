from django.db import models
from django.contrib.auth.models import User
from uuid import uuid4
from datetime import timezone

class Category(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    name = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.description}"


class Product(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    # owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="products")
    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    status = models.CharField(
        max_length=20,
        choices=[('in_stock', 'In Stock'), ('limited_stock', 'Limited Stock'), ('out_of_stock', 'Out of Stock')],
        default='in_stock'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    @staticmethod
    def generate_uuid(self):
        return str(uuid4())[:8]

    def __str__(self):
        return self.title

    def update_status(self):
        """Update the product availability status based on stock"""
        if self.stock == 0:
            self.availability_status = 'out_of_stock'
        elif self.stock < 10:
            self.availability_status = 'limited_stock'
        else:
            self.availability_status = 'in_stock'
        self.save()

class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to="products/", blank=True, null=True)
    alt_text = models.CharField(max_length=255, blank=True)

class ProductTag(models.Model):
    products = models.ManyToManyField(Product, blank=True)
    name = models.CharField(max_length=32)
    slug = models.SlugField(max_length=48)
    description = models.TextField(blank=True, null=True)
    active = models.BooleanField(default=True)

class ProductPriceHistory(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='price_history')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    effective_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.product.name} - {self.price} on {self.effective_date.strftime('%Y-%m-%d')}"

class Inventory(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE)
    stock = models.PositiveIntegerField(default=0)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.product.title} - {self.stock} in stock"






