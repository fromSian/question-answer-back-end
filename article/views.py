from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import api_view, action, permission_classes
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from comment.filters import CommentFilter
from rest_framework.mixins import ListModelMixin, CreateModelMixin, DestroyModelMixin
from rest_framework.views import APIView
from .models import Article
from .serializers import ArticleReadSerializer, ArticleWriteSerializer, TagSerializer
from rest_framework.permissions import (
    IsAuthenticated,
    IsAuthenticatedOrReadOnly,
    AllowAny,
)
from taggit.serializers import TagListSerializerField, TaggitSerializer
from rest_framework import status
from comment.models import Comment
from comment.serializers import (
    CommentReadSerializer,
    CommentWriteSerializer,
    CommentReadWithArticleSerializer,
)
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.conf import settings

from account.pagination import CustomPagination
from denounce.models import Denounce
from taggit.models import Tag
from .filters import ArticleFilter
from denounce.serializers import (
    DenounceWriteSerializer,
    DenounceReadWithArticleSerializer,
)

from datetime import datetime


@swagger_auto_schema(
    method="POST",
    operation_description="浏览量+1",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=["article"],
        properties={
            "article": openapi.Schema(type=openapi.TYPE_INTEGER, description="文章id"),
        },
    ),
)
@api_view(["POST"])
@permission_classes([AllowAny])
def add_view_count(request):
    """
    问题浏览量+1
    """
    try:
        articleid = request.data.get("article", "")
        object = Article.objects.filter(id=articleid).first()
        if not object:
            raise Exception("文章不存在")
        object.views = object.views + 1
        object.save()
        return Response(
            {"status": True, "message": "浏览量+1成功"}, status=status.HTTP_202_ACCEPTED
        )
    except Exception as e:
        return Response(
            {"status": False, "message": str(e)}, status=status.HTTP_400_BAD_REQUEST
        )


class ArticleViewSet(ModelViewSet):
    """
    问题视图集
    包括增删改查查+我的问题
    """

    queryset = Article.objects.all().order_by("-views")

    permission_classes = (IsAuthenticatedOrReadOnly,)

    filterset_class = ArticleFilter

    def is_denounce(self, n):
        return not n["denounce"]

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(
                filter(self.is_denounce, serializer.data)
            )

        serializer = self.get_serializer(queryset, many=True)
        return Response(filter(self.is_denounce, serializer.data))

    def get_serializer_class(self):
        if (
            self.action == "create"
            or self.action == "update"
            or self.action == "partial_update"
        ):
            return ArticleWriteSerializer
        else:
            return ArticleReadSerializer

    @swagger_auto_schema(
        operation_description="获取我的文章",
    )
    @action(
        methods=["GET"],
        detail=False,
        permission_classes=[IsAuthenticated],
        filterset_class=None,
    )
    def mine(self, request):
        """
        查询我的问题
        """
        user = request.user
        queryset = Article.objects.filter(author=user)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(True)


class CommentViewSet(
    GenericViewSet, ListModelMixin, CreateModelMixin, DestroyModelMixin
):
    """
    回答视图集
    包括增删改查+我的回答
    """

    queryset = Comment.objects.all()
    serializer_class = CommentReadSerializer
    filterset_class = CommentFilter

    def get_serializer_class(self):
        if (
            self.action == "create"
            or self.action == "update"
            or self.action == "partial_update"
        ):
            return CommentWriteSerializer
        elif self.action == "mine":
            return CommentReadWithArticleSerializer
        else:
            return CommentReadSerializer

    @swagger_auto_schema(
        operation_description="获取我的评论",
    )
    @action(
        methods=["GET"],
        detail=False,
        permission_classes=[IsAuthenticated],
        filterset_class=None,
    )
    def mine(self, request):
        """
        查询我的回答
        """
        user = request.user
        queryset = Comment.objects.filter(author=user)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(True)

    @swagger_auto_schema(
        operation_description="设置/取消优秀作答",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=["comment"],
            properties={
                "comment": openapi.Schema(
                    type=openapi.TYPE_INTEGER, description="评论id"
                ),
            },
        ),
    )
    @action(
        methods=["POST"],
        detail=False,
        permission_classes=[IsAuthenticated],
        filterset_class=None,
    )
    def great(self, request):
        """
        设置/取消优秀作答
        """
        try:
            commentid = request.data.get("comment", 1)
            user = request.user

            object = Comment.objects.filter(id=commentid).first()

            if not object:
                raise Exception("评论不存在")

            if user != object.article.author:
                raise Exception("该用户没有权限设置此评论为优秀作答")
            if not object.is_great:
                object.is_great = True
                object.save()
                object.author.coins = object.author.coins + 2
                object.author.save()
                return Response(
                    {"status": True, "message": "设置优秀作答成功"},
                    status=status.HTTP_202_ACCEPTED,
                )
            else:
                object.is_great = False
                object.save()
                return Response(
                    {"status": True, "message": "取消优秀作答成功"},
                    status=status.HTTP_202_ACCEPTED,
                )
        except Exception as e:
            return Response(
                {"status": False, "message": str(e)}, status=status.HTTP_400_BAD_REQUEST
            )


class DenounceViewSet(GenericViewSet, CreateModelMixin):
    """
    举报视图集
    包括增+我的举报
    """

    queryset = Denounce.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_serializer_class(self):
        if (
            self.action == "create"
            or self.action == "update"
            or self.action == "partial_update"
        ):
            return DenounceWriteSerializer
        elif self.action == "mine":
            return DenounceReadWithArticleSerializer

    @swagger_auto_schema(
        operation_description="获取我的举报",
    )
    @action(methods=["GET"], detail=False)
    def mine(self, request):
        """
        查询我的举报
        """
        user = request.user
        queryset = Denounce.objects.filter(user=user)
        # queryset = Denounce.objects.all()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(True)


class TagView(GenericViewSet, ListModelMixin):
    """
    标签视图集
    查询所有标签
    """

    queryset = Tag.objects.all()
    serializer_class = TagSerializer

    def list(self, request, *args, **kwargs):
        try:
            queryset = self.get_queryset()
            tags = [element.name for element in queryset]
            serializer = self.get_serializer({"tags": tags})
            return Response(
                {"status": True, "message": "获取标签成功", **serializer.data}
            )

        except Exception:
            return Response(
                {"status": False, "message": "获取标签失败"},
                status=status.HTTP_400_BAD_REQUEST,
            )
