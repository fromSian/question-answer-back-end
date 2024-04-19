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
from comment.serializers import CommentReadSerializer, CommentWriteSerializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.conf import settings

from account.pagination import CustomPagination
from denounce.models import Denounce
from taggit.models import Tag
from .filters import ArticleFilter

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
    queryset = Article.objects.all().order_by("-views")

    permission_classes = (IsAuthenticatedOrReadOnly,)

    filterset_class = ArticleFilter


    def get_serializer_class(self):
        if self.action == "create":
            return ArticleWriteSerializer
        else:
            return ArticleReadSerializer
    
    @swagger_auto_schema(
        operation_description="获取我的文章",
    )
    @action(methods=['GET'], detail=False, permission_classes=[IsAuthenticated], filterset_class=None)
    def mine(self, request):
        user = request.user
        queryset = Article.objects.filter(author=user)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(True)
    

class CommentViewSet(GenericViewSet, ListModelMixin, CreateModelMixin, DestroyModelMixin):
    queryset = Comment.objects.all()
    serializer_class = CommentReadSerializer
    filterset_class = CommentFilter

    def get_serializer_class(self):
        if self.action == "create":
            return CommentWriteSerializer
        else:
            return CommentReadSerializer

    @swagger_auto_schema(
        operation_description="获取我的评论",
    )
    @action(methods=['GET'], detail=False, permission_classes=[IsAuthenticated], filterset_class=None)
    def mine(self, request):
        user = request.user
        queryset = Comment.objects.filter(author=user)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(True)
    



class CommentAPIView(APIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)

    @swagger_auto_schema(
        operation_description="获取文章评论",
        manual_parameters=[
            openapi.Parameter(
                name="article",
                in_=openapi.IN_QUERY,
                description="文章id",
                type=openapi.TYPE_INTEGER,
            )
        ],
    )
    def get(self, request):
        try:
            articleid = request.query_params.get("article", 1)
            article = Article.objects.filter(id=articleid).first()
            if not article:
                raise Exception("文章不存在")
            comment_queryset = Comment.objects.filter(article=article).order_by(
                "is_great"
            )

            paginator = CustomPagination()
            page = paginator.paginate_queryset(
                queryset=comment_queryset, request=request, view=self
            )

            if page is not None:
                serializer = CommentReadSerializer(
                    page, many=True, context={"request": request}
                )

                return paginator.get_paginated_response(serializer.data)

            serializer = CommentReadSerializer(
                comment_queryset, many=True, context={"request": request}
            )

            return Response(
                {"status": True, "message": "查询评论成功", **serializer.data},
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return Response(
                {"status": False, "message": str(e)}, status=status.HTTP_400_BAD_REQUEST
            )

    @swagger_auto_schema(
        operation_description="添加评论",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=["article", "content"],
            properties={
                "article": openapi.Schema(
                    type=openapi.TYPE_INTEGER, description="文章id"
                ),
                "content": openapi.Schema(
                    type=openapi.TYPE_STRING, description="评论内容"
                ),
            },
        ),
    )
    def post(self, request):
        try:
            articleid = request.data.get("article", "")
            article = Article.objects.filter(id=articleid).first()
            if not article:
                raise Exception("文章不存在")
            author = request.user
            content = request.data.get("content", "")
            comment = Comment.objects.create(
                article=article, author=author, content=content
            )
            return Response(
                {"status": True, "message": "发布评论成功"},
                status=status.HTTP_201_CREATED,
            )
        except Exception as e:
            return Response(
                {"status": False, "message": str(e)}, status=status.HTTP_400_BAD_REQUEST
            )

@swagger_auto_schema(
    method="POST",
    operation_description="设置/取消优秀作答",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=["comment"],
        properties={
            "comment": openapi.Schema(type=openapi.TYPE_INTEGER, description="评论id"),
        },
    ),
)
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def set_great_comment(request):
    try:
        commentid = request.data.get("comment", 1)
        user = request.user

        object = Comment.objects.filter(id=commentid).first()

        if not object:
            raise Exception("评论不存在")

        if user != object.author:
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


@swagger_auto_schema(
    method="POST",
    operation_description="举报文章",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=["article"],
        properties={
            "article": openapi.Schema(type=openapi.TYPE_INTEGER, description="文章id"),
        },
    ),
)
@permission_classes([IsAuthenticated])
@api_view(["POST"])
def denounce(request):
    try:
        articleid = request.data.get("article", "")
        user = request.user
        article = Article.objects.filter(id=articleid).first()
        if not article:
            raise Exception("文章不存在")
        d = Denounce.objects.create(article=article, user=user)
        return Response(
            {"status": True, "message": "举报成功，待审核"},
            status=status.HTTP_201_CREATED,
        )
    except Exception as e:
        return Response(
            {"status": False, "message": str(e)}, status=status.HTTP_400_BAD_REQUEST
        )


class TagView(GenericViewSet, ListModelMixin):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer

    def list(self, request, *args, **kwargs):
        try:
            queryset = self.get_queryset()
            tags = [element.name for element in queryset]
            serializer = self.get_serializer({ 'tags': tags })
            return Response({"status": True, "message": "获取标签成功", **serializer.data})
            
        except Exception:
            return Response({"status": False, "message": "获取标签失败"}, status=status.HTTP_400_BAD_REQUEST)