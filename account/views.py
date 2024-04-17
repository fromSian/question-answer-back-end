from rest_framework.decorators import (
    api_view,
    action,
    authentication_classes,
    permission_classes,
)
from rest_framework.response import Response
from rest_framework import status, views, viewsets
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly

from .models import User
from .serializers import UserSerializer, UserReaderializer

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


@swagger_auto_schema(
    method="POST",
    operation_description="用户注册",
    responses={
        201: UserSerializer,
        400: False,
    },
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=["username", "password"],
        properties={
            "username": openapi.Schema(type=openapi.TYPE_STRING, description="用户名"),
            "password": openapi.Schema(type=openapi.TYPE_STRING, description="密码"),
        },
    ),
)
@api_view(
    [
        "POST",
    ]
)
def account_registration(request):
    try:
        user_data = request.data

        serializer = UserSerializer(data=user_data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(True, status=status.HTTP_201_CREATED)

    except Exception:
        return Response(False, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(
    method="POST",
    operation_description="用户登录",
    responses={
        201: UserReaderializer,
        400: False,
    },
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=["username", "password"],
        properties={
            "username": openapi.Schema(type=openapi.TYPE_STRING, description="用户名"),
            "password": openapi.Schema(type=openapi.TYPE_STRING, description="密码"),
        },
    ),
)
@api_view(
    [
        "POST",
    ]
)
def account_login(request):
    try:
        user_data = request.data
        user = authenticate(username=user_data["username"], password=user_data["password"])
        serializer = UserReaderializer(user)
        jwt_token = RefreshToken.for_user(user)
        serializer_data = serializer.data
        serializer_data["token"] = str(jwt_token.access_token)
        response_data = {
            "user": serializer_data,
        }
        return Response(response_data, status=status.HTTP_202_ACCEPTED)

    except Exception:
        return Response(False, status=status.HTTP_400_BAD_REQUEST)

@swagger_auto_schema(
    method="GET",
    operation_description="获取用户信息",
    responses={
        201: UserReaderializer,
        400: False,
    },
)
@api_view(
    [
        "GET",
    ]
)
@permission_classes(
    [
        IsAuthenticated,
    ]
)
def user_info(request):
    try:
        user = request.user
        print(user)
        if user:
            serializer = UserReaderializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            raise

    except Exception:
        return Response(False, status=status.HTTP_400_BAD_REQUEST)
