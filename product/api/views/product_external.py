from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser
from rest_framework import status
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from fetch_save_data_api.logic.fetch_sava_all_data import fetch_and_bulk_save_products


@swagger_auto_schema(
    method='post',
    responses={200: openapi.Response('Products fetched and saved successfully.')},
    operation_description="Fetch products from the external API and save them to the database.",
    tags=["Product"]
)
@api_view(['POST'])
# @permission_classes([IsAdminUser])
def fetch_products_from_external_api(request):
    """
    Fetch products from the external API and save them to the database.
    """
    fetch_and_bulk_save_products()
    return Response({"detail": "Products fetched and saved successfully."}, status=status.HTTP_200_OK)
