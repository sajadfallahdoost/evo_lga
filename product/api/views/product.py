from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.permissions import IsAuthenticated, AllowAny
from product.api.serializers.product import RelatedProductSerializer
from product.models import Product, RelatedProduct, ProductReview
from product.api.serializers import ProductSerializer, ProductReviewSerializer, RelatedProductSerializer
from django.utils import timezone
from rest_framework.pagination import PageNumberPagination
from product.api.serializers import ManufacturerSerializer
from product.models import Manufacturer


class ProductPagination(PageNumberPagination):
    page_size = 72  # Items per page
    page_size_query_param = 'page_size'
    max_page_size = 100  # Optional limit


@swagger_auto_schema(
    method='get',
    manual_parameters=[
        openapi.Parameter('is_external', openapi.IN_QUERY, description="Filter products by external source ('true' or 'false')", type=openapi.TYPE_STRING),
        openapi.Parameter('manufacturer', openapi.IN_QUERY, description="Filter products by manufacturer name", type=openapi.TYPE_STRING),
        openapi.Parameter('color', openapi.IN_QUERY, description="Filter products by color", type=openapi.TYPE_STRING),
        openapi.Parameter('page', openapi.IN_QUERY, description="Page number for pagination", type=openapi.TYPE_INTEGER),
    ],
    responses={200: ProductSerializer(many=True)},
    operation_description="Retrieve a paginated list of all products with optional filtering. Each page contains 50 items.",
    tags=["Product"]
)
@api_view(['GET'])
@permission_classes([AllowAny])
def product_list(request):
    """
    Retrieve a paginated list of products with optional filters for manufacturer, color, and external source.
    """
    manufacturer = request.GET.get('manufacturer')
    color = request.GET.get('color')
    is_external = request.GET.get('is_external')

    products = Product.objects.all()

    if manufacturer:
        products = products.filter(manufacturer__name__icontains=manufacturer)
    if color:
        products = products.filter(color__icontains=color)
    if is_external is not None:
        if is_external.lower() == 'true':
            products = products.filter(is_external=True)
        elif is_external.lower() == 'false':
            products = products.filter(is_external=False)

    paginator = ProductPagination()
    paginated_products = paginator.paginate_queryset(products, request)
    serializer = ProductSerializer(paginated_products, many=True)
    return paginator.get_paginated_response(serializer.data)


@swagger_auto_schema(
    method='get',
    responses={200: ProductSerializer()},
    operation_description="Retrieve details of a specific product by ID",
    tags=["Product"]
)
@api_view(['GET'])
# @permission_classes([AllowAny])
def product_detail(request, pk):
    try:
        product = Product.objects.get(pk=pk)
        serializer = ProductSerializer(product)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Product.DoesNotExist:
        return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)


@swagger_auto_schema(
    method='get',
    responses={200: ProductSerializer(many=True)},
    operation_description="Retrieve a list of all products fetched from the external API",
    tags=["Product"]
)
@api_view(['GET'])
# @permission_classes([AllowAny])
def external_product_list(request):
    """
    Retrieve a list of products fetched from the external API.
    """
    products = Product.objects.filter(is_external=True)
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@swagger_auto_schema(
    method="post",
    request_body=RelatedProductSerializer,
    responses={201: RelatedProductSerializer()},
    operation_description="Add a related product",
    tags=["Related Products"]
)
@api_view(["POST"])
# @permission_classes([IsAuthenticated])
def add_related_product(request):
    serializer = RelatedProductSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(
    method="get",
    responses={200: RelatedProductSerializer(many=True)},
    operation_description="List all related products for a specific product",
    tags=["Related Products"]
)
@api_view(["GET"])
# @permission_classes([AllowAny])
def list_related_products(request, product_id):
    related_products = RelatedProduct.objects.filter(product_id=product_id)
    serializer = RelatedProductSerializer(related_products, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@swagger_auto_schema(
    method="post",
    request_body=ProductReviewSerializer,
    responses={201: ProductReviewSerializer()},
    operation_description="Add a review to a product",
    tags=["Product Reviews"]
)
@api_view(["POST"])
# @permission_classes([IsAuthenticated])
def add_product_review(request, product_id):
    data = request.data.copy()
    data["product"] = product_id
    data["user"] = request.user.id  # Automatically set the user to the logged-in user
    serializer = ProductReviewSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(
    method="get",
    responses={200: ProductReviewSerializer(many=True)},
    operation_description="List all reviews for a specific product",
    tags=["Product Reviews"]
)
@api_view(["GET"])
# @permission_classes([AllowAny])
def list_product_reviews(request, product_id):
    reviews = ProductReview.objects.filter(product_id=product_id)
    serializer = ProductReviewSerializer(reviews, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@swagger_auto_schema(
    method='get',
    manual_parameters=[
        openapi.Parameter('in_stock', openapi.IN_QUERY, description="Filter products by in stock status ('true' or 'false')", type=openapi.TYPE_STRING),
        openapi.Parameter('has_discount', openapi.IN_QUERY, description="Filter products by active discounts ('true' or 'false')", type=openapi.TYPE_STRING),
        openapi.Parameter('min_price', openapi.IN_QUERY, description="Minimum price filter", type=openapi.TYPE_NUMBER),
        openapi.Parameter('max_price', openapi.IN_QUERY, description="Maximum price filter", type=openapi.TYPE_NUMBER)
    ],
    responses={
        200: openapi.Response(
            description="List of filtered products.",
            examples={
                "application/json": [
                    {
                        "name": "Product 1",
                        "final_price": 12000000,
                        "in_stock": True,
                        "description": "A short description of Product 1"
                    },
                    {
                        "name": "Product 2",
                        "final_price": 14000000,
                        "in_stock": False,
                        "description": "A short description of Product 2"
                    }
                ]
            }
        )
    },
    operation_description="Retrieve a list of all products with optional filtering by stock status, discounts, and price range.",
    tags=["Product"]
)
@api_view(['GET'])
# @permission_classes([AllowAny])
def filtered_product_list(request):
    """
    Retrieve a list of products with optional filters for stock status, active discounts, and price range.
    """
    in_stock = request.GET.get('in_stock')
    has_discount = request.GET.get('has_discount')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')

    products = Product.objects.all()

    if in_stock is not None:
        products = products.filter(in_stock=(in_stock.lower() == 'true'))

    if has_discount is not None and has_discount.lower() == 'true':
        current_time = timezone.now()
        products = products.filter(
            discounts__is_active=True,
            discounts__start_date__lte=current_time,
            discounts__end_date__gte=current_time
        ).distinct()

    if min_price is not None and max_price is not None:
        try:
            min_price = float(min_price)
            max_price = float(max_price)
            products = products.filter(final_price__gte=min_price, final_price__lte=max_price)
        except ValueError:
            return Response({"error": "Invalid price values"}, status=status.HTTP_400_BAD_REQUEST)

    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@swagger_auto_schema(
    method='get',
    responses={200: ManufacturerSerializer(many=True)},
    operation_description="Retrieve a list of all manufacturers",
    tags=["brand"]
)
@api_view(['GET'])
@permission_classes([AllowAny])
def brand(request):
    """
    Retrieve a list of all manufacturers.
    """
    manufacturers = Manufacturer.objects.filter(is_active=True)
    serializer = ManufacturerSerializer(manufacturers, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@swagger_auto_schema(
    method='get',
    manual_parameters=[
        openapi.Parameter(
            'page',
            openapi.IN_QUERY,
            description="Page number for pagination",
            type=openapi.TYPE_INTEGER
        ),
    ],
    responses={
        200: openapi.Response(
            description="Retrieve a paginated list of in-stock products",
            schema=ProductSerializer(many=True),
            examples={
                "application/json": [
                    {
                        "id": 1,
                        "name": "Sample Product 1",
                        "price": "120.00",
                        "final_price": "130.00",
                        "in_stock": True,
                        "description": "Sample description"
                    },
                    {
                        "id": 2,
                        "name": "Sample Product 2",
                        "price": "150.00",
                        "final_price": "165.00",
                        "in_stock": True,
                        "description": "Another sample description"
                    }
                ]
            }
        )
    },
    operation_description="Retrieve a paginated list of all in-stock products. Each page contains 24 items by default.",
    tags=["Product"]
)
@api_view(['GET'])
@permission_classes([AllowAny])
def in_stock_product_list(request):
    """
    Retrieve a paginated list of all in-stock products.
    """
    products = Product.objects.filter(in_stock=True)

    # Apply pagination
    paginator = ProductPagination()
    paginated_products = paginator.paginate_queryset(products, request)

    # Serialize paginated results
    serializer = ProductSerializer(paginated_products, many=True)

    return paginator.get_paginated_response(serializer.data)


# @swagger_auto_schema(
#     method='get',
#     manual_parameters=[
#         openapi.Parameter('in_stock', openapi.IN_QUERY, description="Filter products by in-stock status ('true' or 'false')", type=openapi.TYPE_STRING),
#         openapi.Parameter('has_discount', openapi.IN_QUERY, description="Filter products by active discounts ('true' or 'false')", type=openapi.TYPE_STRING),
#         openapi.Parameter('min_price', openapi.IN_QUERY, description="Minimum price filter", type=openapi.TYPE_NUMBER),
#         openapi.Parameter('max_price', openapi.IN_QUERY, description="Maximum price filter", type=openapi.TYPE_NUMBER)
#     ],
#     responses={200: ProductSerializer(many=True)},
#     operation_description="Retrieve a list of products with optional filtering by stock status, discounts, and price range.",
#     tags=["Product"]
# )
# @api_view(['GET'])
# @permission_classes([AllowAny])
# def filtered_product_list(request):
#     """
#     Retrieve a list of products with optional filters:
#     - Filter by stock status ('in_stock').
#     - Filter by active discounts ('has_discount').
#     - Filter by price range ('min_price' to 'max_price').
#     """
#     in_stock = request.GET.get('in_stock')
#     has_discount = request.GET.get('has_discount')
#     min_price = request.GET.get('min_price')
#     max_price = request.GET.get('max_price')

#     products = Product.objects.all()

#     if in_stock is not None:
#         products = products.filter(in_stock=(in_stock.lower() == 'true'))

#     if has_discount is not None and has_discount.lower() == 'true':
#         current_time = timezone.now()
#         products = products.filter(
#             discounts__is_active=True,
#             discounts__start_date__lte=current_time,
#             discounts__end_date__gte=current_time
#         ).distinct()

#     if min_price is not None and max_price is not None:
#         try:
#             min_price = float(min_price)
#             max_price = float(max_price)
#             products = products.filter(final_price__gte=min_price, final_price__lte=max_price)
#         except ValueError:
#             return Response({"error": "Invalid price values"}, status=status.HTTP_400_BAD_REQUEST)

#     serializer = ProductSerializer(products, many=True)
#     return Response(serializer.data, status=status.HTTP_200_OK)
