from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from drf_yasg.utils import swagger_auto_schema
from support.models import Comment
from support.api.serializers.comment import CommentSerializer


@swagger_auto_schema(
    method='get',
    tags=['support'],
    responses={200: CommentSerializer(many=True)},
    operation_description="Retrieve all comments",
    operation_summary="Get list of comments",
)
@swagger_auto_schema(
    method='post',
    tags=['support'],
    request_body=CommentSerializer,
    responses={
        201: CommentSerializer,
        400: "Bad Request - Invalid data",
    },
    operation_description="Create a new comment",
    operation_summary="Create comment",
)
@api_view(['GET', 'POST'])
@permission_classes([permissions.IsAuthenticated])
def comment_title(request):
    """
    Handle listing and creating comments
    """
    if request.method == 'GET':
        comments = Comment.objects.all()
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(
    method='get',
    tags=['support'],
    responses={200: CommentSerializer},
    operation_description="Retrieve a single comment by ID",
    operation_summary="Get comment by ID",
)
@swagger_auto_schema(
    method='put',
    tags=['support'],
    request_body=CommentSerializer,
    responses={
        200: CommentSerializer,
        400: "Bad Request - Invalid data",
    },
    operation_description="Update a comment by ID",
    operation_summary="Update comment",
)
@swagger_auto_schema(
    method='delete',
    tags=['support'],
    responses={204: "No Content"},
    operation_description="Delete a comment by ID",
    operation_summary="Delete comment",
)
@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([permissions.IsAuthenticated])
def comment_detail(request, pk):
    """
    Retrieve, update, or delete a comment instance.
    """
    try:
        comment = Comment.objects.get(pk=pk)
    except Comment.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = CommentSerializer(comment)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = CommentSerializer(comment, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
