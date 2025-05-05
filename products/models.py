from django.db import models
from django.contrib.auth.models import User
from uuid import uuid4

class Category(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    title = models.CharField(max_length=200, blank=True, null=True, db_index=True)
    slug = models.SlugField(max_length=200, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('title',)
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return f"{self.title} - {self.slug}"

class Product(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE, default="")
    # owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="products")
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, db_index=True, unique=True)
    description = models.TextField(blank=True)
    current_price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    status = models.CharField(
        max_length=20,
        choices=[('in_stock', 'In Stock'), ('limited_stock', 'Limited Stock'), ('out_of_stock', 'Out of Stock')],
        default='in_stock'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('name', )
        indexes = [
            models.Index(fields=['id', 'slug'])
        ]

    @staticmethod
    def generate_uuid(self):
        return str(uuid4())[:8]

    def __str__(self):
        return f"{self.name} - {self.category} - {self.current_price} "

    def update_status(self):
        """Update the products availability status based on stock"""
        if self.stock == 0:
            self.availability_status = 'out_of_stock'
        elif self.stock < 10:
            self.availability_status = 'limited_stock'
        else:
            self.availability_status = 'in_stock'
        self.save()

class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to="products/%Y/%m/%d", blank=True, null=True)
    alt_text = models.CharField(max_length=255, blank=True)

class ProductTag(models.Model):
    products = models.ManyToManyField(Product, blank=True)
    name = models.CharField(max_length=32)
    slug = models.SlugField(max_length=48, null=True)
    description = models.TextField(blank=True, null=True)
    active = models.BooleanField(default=True)

class ProductPriceHistory(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='price_history')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.product.name} - {self.price} on {self.effective_date.strftime('%Y-%m-%d')}"

class Inventory(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE)
    stock = models.PositiveIntegerField(default=0)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.product.name} - {self.stock} in stock"






