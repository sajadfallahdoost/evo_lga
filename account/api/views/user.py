from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.shortcuts import get_object_or_404
from account.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from account.api.serializers import (
    SimplifiedUserRegistrationSerializer,
    SimplifiedUserProfileSerializer,
    SimplifiedChangePasswordSerializer,
)


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


@swagger_auto_schema(
    method='post',
    request_body=SimplifiedUserRegistrationSerializer,
    responses={201: SimplifiedUserProfileSerializer},
    operation_description="Register or log in a user using phone number and OTP",
    operation_summary="User Registration/Login",
    tags=["Account"],
)
@api_view(['POST'])
# @permission_classes([AllowAny])
def register_or_login_user(request):
    """Register or login user via phone number and OTP"""
    serializer = SimplifiedUserRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        user, created = serializer.get_or_create_user()
        tokens = get_tokens_for_user(user)
        response_data = {**SimplifiedUserProfileSerializer(user).data, **tokens}
        status_code = status.HTTP_201_CREATED if created else status.HTTP_200_OK
        return Response(response_data, status=status_code)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(
    method='get',
    responses={200: SimplifiedUserProfileSerializer},
    operation_description="Retrieve the profile of a user by their ID. Returns full details for the specified user if authenticated.",
    operation_summary="Retrieve User Profile by ID",
    tags=["Account"]
)
@api_view(['GET'])
# @permission_classes([IsAuthenticated])
def user_profile_by_id(request, user_id):
    """Retrieve User Profile by ID"""
    user = get_object_or_404(User, id=user_id)
    serializer = SimplifiedUserProfileSerializer(user)
    return Response(serializer.data, status=status.HTTP_200_OK)


@swagger_auto_schema(
    method='get',
    responses={200: SimplifiedUserProfileSerializer},
    operation_description="Retrieve full profile of the logged-in user, including role, email, national ID, and additional profile details.",
    operation_summary="User Profile",
    tags=["Account"]
)
@api_view(['GET'])
# @permission_classes([IsAuthenticated])
def user_profile(request):
    """User Profile Endpoint - Retrieves profile of logged-in user"""
    serializer = SimplifiedUserProfileSerializer(request.user)
    return Response(serializer.data)


@swagger_auto_schema(
    method='post',
    request_body=SimplifiedChangePasswordSerializer,
    responses={200: openapi.Response('Password changed successfully')},
    operation_description="Change password of the logged-in user",
    operation_summary="Change Password",
    tags=["Account"]
)
@api_view(['POST'])
# @permission_classes([IsAuthenticated])
def change_password(request):
    """Change Password Endpoint"""
    serializer = SimplifiedChangePasswordSerializer(data=request.data)
    if serializer.is_valid():
        if not request.user.check_password(serializer.validated_data['old_password']):
            return Response({"old_password": "Wrong password."}, status=status.HTTP_400_BAD_REQUEST)
        request.user.set_password(serializer.validated_data['new_password'])
        request.user.save()
        return Response({"detail": "Password changed successfully"}, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
