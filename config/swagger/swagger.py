from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="HamrahCell API",
        default_version='v0',
        description="API documentation for the HamrahCell Online Shop",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="fallahdoostsajad@gmail.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)
