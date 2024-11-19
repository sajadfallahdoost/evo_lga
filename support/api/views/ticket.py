from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from drf_yasg.utils import swagger_auto_schema
from support.models import Ticket
from support.api.serializers.ticket import TicketSerializer


@swagger_auto_schema(
    method='get',
    tags=['support'],
    responses={200: TicketSerializer(many=True)},
    operation_description="Retrieve all tickets",
    operation_summary="Get list of tickets",
)
@swagger_auto_schema(
    method='post',
    tags=['support'],
    request_body=TicketSerializer,
    responses={
        201: TicketSerializer,
        400: "Bad Request - Invalid data",
    },
    operation_description="Create a new ticket",
    operation_summary="Create ticket",
)
@api_view(['GET', 'POST'])
@permission_classes([permissions.IsAuthenticated])
def ticket_title(request):
    """
    Handle listing and creating tickets
    """
    if request.method == 'GET':
        tickets = Ticket.objects.all()
        serializer = TicketSerializer(tickets, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = TicketSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(
    method='get',
    tags=['support'],
    responses={200: TicketSerializer},
    operation_description="Retrieve a single ticket by ID",
    operation_summary="Get ticket by ID",
)
@swagger_auto_schema(
    method='put',
    tags=['support'],
    request_body=TicketSerializer,
    responses={
        200: TicketSerializer,
        400: "Bad Request - Invalid data",
    },
    operation_description="Update a ticket by ID",
    operation_summary="Update ticket",
)
@swagger_auto_schema(
    method='delete',
    tags=['support'],
    responses={204: "No Content"},
    operation_description="Delete a ticket by ID",
    operation_summary="Delete ticket",
)
@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([permissions.IsAuthenticated])
def ticket_detail(request, pk):
    """
    Retrieve, update, or delete a ticket instance.
    """
    try:
        ticket = Ticket.objects.get(pk=pk)
    except Ticket.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = TicketSerializer(ticket)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = TicketSerializer(ticket, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        ticket.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
