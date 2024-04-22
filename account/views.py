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
from rest_framework.permissions import (
    IsAuthenticated,
    IsAuthenticatedOrReadOnly,
    AllowAny,
)

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
@permission_classes(
    [
        AllowAny,
    ]
)
def account_registration(request):
    try:
        user_data = request.data

        serializer = UserSerializer(data=user_data)

        if serializer.is_valid():
            serializer.save()
            return Response(
                {"status": True, "message": "注册成功"}, status=status.HTTP_201_CREATED
            )
        else:
            return Response(
                {"status": False, "message": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )
    except Exception as e:
        print(e)
        return Response(
            {"status": False, "message": "注册失败"}, status=status.HTTP_400_BAD_REQUEST
        )


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
@permission_classes(
    [
        AllowAny,
    ]
)
def account_login(request):
    try:
        user_data = request.data
        user = authenticate(
            username=user_data["username"], password=user_data["password"]
        )
        if not user or not user.groups.values("name").filter(name="普通用户").exists():
            raise Exception("用户名或密码错误")
        serializer = UserReaderializer(user)
        jwt_token = RefreshToken.for_user(user)
        serializer_data = serializer.data
        serializer_data["token"] = str(jwt_token.access_token)
        return Response(
            {"status": True, "message": "登录成功", **serializer_data},
            status=status.HTTP_202_ACCEPTED,
        )

    except Exception as e:
        return Response(
            {"status": False, "message": str(e)}, status=status.HTTP_400_BAD_REQUEST
        )


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
        if user:
            serializer = UserReaderializer(user)
            return Response(
                {"status": True, "message": "用户信息获取成功", **serializer.data},
                status=status.HTTP_200_OK,
            )
        else:
            raise Exception("no user")

    except Exception as e:
        return Response(
            {"status": False, "message": str(e)}, status=status.HTTP_400_BAD_REQUEST
        )


from apscheduler.schedulers.background import BackgroundScheduler


def set_times_monthly():
    print("set times")
    User.objects.update(times=2)


scheduler = BackgroundScheduler()
try:
    scheduler.add_job(
        set_times_monthly,
        "cron",
        day=1,
        hour=0,
        minute=0,
        id="set_times_monthly",
        replace_existing=True,
        timezone="Asia/Shanghai",
    )
    scheduler.start()
except Exception as e:
    print(e)
    scheduler.shutdown()
