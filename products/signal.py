from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from .models import Inventory, Product, ProductPriceHistory

@receiver(post_save, sender=Inventory)
def check_low_stock(sender, instance, **kwargs):
    if instance.stock <= settings.LOW_STOCK_THRESHOLD:
        # Send an email notification to admins and sellers
        product_name = instance.product.name
        subject = f"Low Stock Alert: {product_name}"
        message = f"The stock for {product_name} is low. Only {instance.stock} units are left."

        # Example: Send an email to admins and sellers
        recipients = ['erdeysyoum@gamil.com', 'abelyitagesu@gmail.com']

        send_mail(subject, message, 'no-reply@example.com', recipients)

@receiver(post_save, sender=Product)
def update_product_availability(sender, instance, **kwargs):
    instance.update_status()

@receiver(pre_save, sender=Product)
def log_price_change(sender, instance, **kwargs):
    if instance.pk:
        try:
            previous = Product.objects.get(pk=instance.pk)
            if previous.current_price != instance.current_price:
                print(f"Price changed from {previous.current_price} to {instance.current_price}")

                ProductPriceHistory.objects.create(product=instance, price=previous.current_price)
        except Product.DoesNotExist:
            pass

