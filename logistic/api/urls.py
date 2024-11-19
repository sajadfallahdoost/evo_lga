from django.urls import path
from logistic.api.views import dispatch_order

urlpatterns = [
    path("dispatch/<int:order_id>/", dispatch_order, name="dispatch_order")
]
