from django.contrib import admin
from .models import Product, Category, Inventory, ProductImage, ProductTag, ProductPriceHistory

admin.site.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name', )}

admin.site.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'current_price', 'status', 'created_at', 'updated_at']
    list_filter = ['status', 'created_at', 'updated_at']
    list_editable = ['current_price', 'status']
    prepopulated_fields = {'slug': ('name', )}

admin.site.register(Inventory)
admin.site.register(ProductImage)
admin.site.register(ProductTag)
admin.site.register(ProductPriceHistory)
