from django.urls import path
from basket.api.views import basket_list_create, order_list_create, checkout, get_user_token

urlpatterns = [
    path('baskets/', basket_list_create, name='basket-list-create'),
    path('orders/', order_list_create, name='order-list-create'),
    path('checkout/', checkout, name='checkout'),
    path('get_user_token/', get_user_token, name='get_user_token'),
]
