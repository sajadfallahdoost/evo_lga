from django.db.models.signals import post_save
from django.dispatch import receiver
from basket.models import Order, Basket


@receiver(post_save, sender=Order)
def clear_basket_after_order_creation(sender, instance, created, **kwargs):
    if created:
        Basket.objects.filter(user=instance.user).update(items=[])
