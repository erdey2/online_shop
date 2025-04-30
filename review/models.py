from django.db import models
from products.models import Product
from django.contrib.auth.models import User

class ProductReview(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField()  # 1 to 5 stars
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('product', 'user')  # one review per products per user
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user} review on {self.product}"


