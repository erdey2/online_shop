from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from .models import Inventory
from .models import Product


@receiver(post_save, sender=Inventory)
def check_low_stock(sender, instance, **kwargs):
    if instance.stock <= settings.LOW_STOCK_THRESHOLD:
        # Send an email notification to admins and sellers
        product_title = instance.product.title
        subject = f"Low Stock Alert: {product_title}"
        message = f"The stock for {product_title} is low. Only {instance.stock} units are left."

        # Example: Send an email to admins and sellers
        # For simplicity, assuming admins and sellers have email addresses
        recipients = ['erdeysyoum@gamil.com', 'abelyitagesu@gmail.com']

        send_mail(subject, message, 'no-reply@example.com', recipients)

@receiver(post_save, sender=Product)
def update_product_availability(sender, instance, **kwargs):
    instance.update_status()
