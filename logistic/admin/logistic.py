from django.contrib import admin
from logistic.models import LogisticsOrder


@admin.register(LogisticsOrder)
class LogisticsOrderAdmin(admin.ModelAdmin):
    list_display = ("order", "tracking_number", "status", "dispatched_at", "updated_at")
    search_fields = ("order__id", "tracking_number")
    list_filter = ("status",)
