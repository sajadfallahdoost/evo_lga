from django.db import models
from django.conf import settings
from basket.models import Order


class LogisticsOrder(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name="logistics_info")
    tracking_number = models.CharField(max_length=100, blank=True, null=True)
    status = models.CharField(max_length=50, default="pending")  # e.g., pending, dispatched, failed
    dispatched_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Logistics info for Order {self.order.id}"
