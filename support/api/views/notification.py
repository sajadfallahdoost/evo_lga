from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from drf_yasg.utils import swagger_auto_schema
from support.models import Notification
from support.api.serializers.notification import NotificationSerializer


@swagger_auto_schema(
    method='get',
    tags=['support'],
    responses={200: NotificationSerializer(many=True)},
    operation_description="Retrieve all notifications",
    operation_summary="Get list of notifications",
)
@swagger_auto_schema(
    method='post',
    tags=['support'],
    request_body=NotificationSerializer,
    responses={
        201: NotificationSerializer,
        400: "Bad Request - Invalid data",
    },
    operation_description="Create a new notification",
    operation_summary="Create notification",
)
@api_view(['GET', 'POST'])
# @permission_classes([permissions.IsAuthenticated])
def notification_title(request):
    """
    Handle listing and creating notifications
    """
    if request.method == 'GET':
        notifications = Notification.objects.all()
        serializer = NotificationSerializer(notifications, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = NotificationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(
    method='get',
    tags=['support'],
    responses={200: NotificationSerializer},
    operation_description="Retrieve a single notification by ID",
    operation_summary="Get notification by ID",
)
@swagger_auto_schema(
    method='put',
    tags=['support'],
    request_body=NotificationSerializer,
    responses={
        200: NotificationSerializer,
        400: "Bad Request - Invalid data",
    },
    operation_description="Update a notification by ID",
    operation_summary="Update notification",
)
@swagger_auto_schema(
    method='delete',
    tags=['support'],
    responses={204: "No Content"},
    operation_description="Delete a notification by ID",
    operation_summary="Delete notification",
)
@api_view(['GET', 'PUT', 'DELETE'])
# @permission_classes([permissions.IsAuthenticated])
def notification_detail(request, pk):
    """
    Retrieve, update, or delete a notification instance.
    """
    try:
        notification = Notification.objects.get(pk=pk)
    except Notification.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = NotificationSerializer(notification)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = NotificationSerializer(notification, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        notification.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
