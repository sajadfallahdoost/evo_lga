from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from account.models import Address
from basket.logic import create_order_from_basket
from basket.models import Basket, Order
from rest_framework_simplejwt.tokens import RefreshToken
from basket.api.serializers import BasketSerializer, OrderSerializer
from account.models import User


@swagger_auto_schema(
    method='get',
    responses={
        200: openapi.Response(
            description="Retrieve the current access token for the authenticated user",
            examples={
                "application/json": {
                    "access": "eyJhbGciOiJIUzI1NiIs...",
                    "refresh": "eyJhbGciOiJIUzI1NiIs..."
                }
            }
        ),
        401: openapi.Response(description="Authentication credentials were not provided.")
    },
    operation_description="Retrieve the access and refresh tokens for the authenticated user.",
    tags=["Authentication"]
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_token(request):
    """
    Retrieve the access and refresh tokens for the authenticated user.
    """
    user = request.user
    refresh = RefreshToken.for_user(user)
    return Response({
        'access': str(refresh.access_token),
        'refresh': str(refresh)
    })


# Basket List and Create API
@swagger_auto_schema(
    method='get',
    responses={
        200: openapi.Response(
            description="Retrieve a list of all baskets for the authenticated user",
            schema=BasketSerializer(many=True),
            examples={
                "application/json": [
                    {
                        "id": 1,
                        "user": 3,
                        "created_at": "2024-11-13T08:34:20Z",
                        "updated_at": "2024-11-13T08:34:20Z",
                        "items": [
                            {
                                "id": 1,
                                "basket": 1,
                                "product": {
                                    "id": 5,
                                    "name": "Sample Product",
                                    "price": 29.99
                                },
                                "quantity": 2,
                                "added_at": "2024-11-13T08:35:10Z"
                            }
                        ]
                    }
                ]
            }
        )
    },
    operation_description="Retrieve a list of all baskets for the authenticated user",
    tags=["Basket"]
)
@swagger_auto_schema(
    method='post',
    request_body=BasketSerializer,
    responses={
        201: openapi.Response(
            description="Create a new basket for the authenticated user",
            schema=BasketSerializer,
            examples={
                "application/json": {
                    "id": 2,
                    "user": 3,
                    "created_at": "2024-11-13T08:50:35Z",
                    "updated_at": "2024-11-13T08:50:35Z",
                    "items": [
                        {
                            "id": 2,
                            "product": {
                                "id": 5,
                                "name": "Sample Product",
                                "price": 29.99
                            },
                            "quantity": 2,
                            "added_at": "2024-11-13T08:51:00Z"
                        }
                    ]
                }
            }
        )
    },
    operation_description="Create a new basket for the authenticated user",
    tags=["Basket"]
)
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def basket_list_create(request):
    if request.method == 'GET':
        baskets = Basket.objects.filter(user=request.user)
        serializer = BasketSerializer(baskets, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'POST':
        serializer = BasketSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Order List and Create API
@swagger_auto_schema(
    method='get',
    responses={
        200: openapi.Response(
            description="Retrieve a list of all orders for the authenticated user",
            schema=OrderSerializer(many=True),
            examples={
                "application/json": [
                    {
                        "id": 1,
                        "user": 3,
                        "address": {
                            "id": 1,
                            "address_line1": "123 Main St",
                            "city": "City",
                            "postal_code": "12345"
                        },
                        "total_price": 75.97,
                        "discount_applied": 5.00,
                        "logistic_cost": 10.00,
                        "status": "pending",
                        "created_at": "2024-11-13T09:00:00Z",
                        "order_items": [
                            {
                                "product": {
                                    "id": 5,
                                    "name": "Sample Product",
                                    "price": 29.99
                                },
                                "quantity": 2,
                                "price": 29.99
                            }
                        ]
                    }
                ]
            }
        )
    },
    operation_description="Retrieve a list of all orders for the authenticated user",
    tags=["Order"]
)
@swagger_auto_schema(
    method='post',
    request_body=OrderSerializer,
    responses={
        201: openapi.Response(
            description="Create a new order for the authenticated user",
            schema=OrderSerializer,
            examples={
                "application/json": {
                    "id": 2,
                    "user": 3,
                    "address": {
                        "id": 1,
                        "address_line1": "123 Main St",
                        "city": "City",
                        "postal_code": "12345"
                    },
                    "total_price": 65.97,
                    "discount_applied": 5.00,
                    "logistic_cost": 10.00,
                    "status": "pending",
                    "created_at": "2024-11-13T09:05:00Z",
                    "order_items": [
                        {
                            "product": {
                                "id": 5,
                                "name": "Sample Product",
                                "price": 29.99
                            },
                            "quantity": 2,
                            "price": 29.99
                        }
                    ]
                }
            }
        )
    },
    operation_description="Create a new order for the authenticated user",
    tags=["Order"]
)
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def order_list_create(request):
    if request.method == 'GET':
        orders = Order.objects.filter(user=request.user)
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'POST':
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(
    method='post',
    operation_description="Create an order from the items in the user's basket",
    tags=["Order"],
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'address_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID of the shipping address')
        },
        required=['address_id']
    ),
    responses={
        201: openapi.Response(description="Order created successfully"),
        400: openapi.Response(description="Bad Request"),
    }
)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def checkout(request):
    address_id = request.data.get('address_id')
    try:
        address = Address.objects.get(id=address_id, user=request.user)
    except Address.DoesNotExist:
        return Response({"error": "Invalid address ID"}, status=status.HTTP_400_BAD_REQUEST)

    order = create_order_from_basket(request.user, address)
    if not order:
        return Response({"error": "No items in basket to checkout"}, status=status.HTTP_400_BAD_REQUEST)

    return Response({"message": "Order created successfully", "order_id": order.id}, status=status.HTTP_201_CREATED)
