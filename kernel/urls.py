from django.contrib import admin
from django.urls import path, include
from azbankgateways.urls import az_bank_gateways_urls
from config.swagger import schema_view
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/user/', include('account.api.urls')),
    path('api/payments/', include('payments.api.urls')),
    path('api/product/', include('product.api.urls')),
    path('api/basket/', include('basket.api.urls')),
    path('api/logistic/', include('logistic.api.urls')),
    path("bankgateways/", az_bank_gateways_urls(), name='bankgateways'),
    # path("api/payment/all_bank/", include('services.payment.payment_all_bank.api.urls')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
    path('api/otp/', include('services.otp.api.urls')),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
