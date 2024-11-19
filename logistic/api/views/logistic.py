import requests
from django.utils import timezone
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from logistic.api.serializers import OrderDispatchSerializer
from logistic.models import LogisticsOrder
from basket.models import Order

LOGISTICS_API_ENDPOINT = "https://logistics-provider.example.com/api/dispatch"

# Define Swagger response examples
order_dispatch_success_response = openapi.Response(
    description="Order dispatched successfully",
    examples={
        "application/json": {
            "message": "Order dispatched successfully",
            "tracking_number": "1234567890"
        }
    }
)

order_dispatch_failure_response = openapi.Response(
    description="Failed to dispatch order",
    examples={
        "application/json": {
            "error": "Failed to dispatch order"
        }
    }
)

order_not_found_response = openapi.Response(
    description="Order not found",
    examples={
        "application/json": {
            "error": "Order not found"
        }
    }
)


@swagger_auto_schema(
    method='post',
    operation_description="Dispatch an order to the logistics provider",
    operation_summary="Dispatch Order",
    tags=["Logistics"],
    manual_parameters=[
        openapi.Parameter(
            "order_id",
            openapi.IN_PATH,
            description="ID of the order to dispatch",
            type=openapi.TYPE_INTEGER
        )
    ],
    responses={
        200: order_dispatch_success_response,
        404: order_not_found_response,
        502: order_dispatch_failure_response
    }
)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def dispatch_order(request, order_id):
    """
    Dispatch an order to the logistics provider. This endpoint sends order
    details to the logistics provider for processing and tracking.
    """
    try:
        order = Order.objects.get(id=order_id, user=request.user)
    except Order.DoesNotExist:
        return Response({"error": "Order not found"}, status=status.HTTP_404_NOT_FOUND)

    serializer = OrderDispatchSerializer(order)
    data = serializer.data

    # Send order data to logistics provider
    response = requests.post(LOGISTICS_API_ENDPOINT, json=data)

    if response.status_code == 200:
        tracking_number = response.json().get("tracking_number")
        LogisticsOrder.objects.create(
            order=order,
            tracking_number=tracking_number,
            status="dispatched",
            dispatched_at=timezone.now(),
        )
        order.status = "shipped"
        order.save()
        return Response({"message": "Order dispatched successfully", "tracking_number": tracking_number})
    else:
        LogisticsOrder.objects.create(order=order, status="failed")
        return Response({"error": "Failed to dispatch order"}, status=status.HTTP_502_BAD_GATEWAY)
