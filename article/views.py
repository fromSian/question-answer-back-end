from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import api_view, action, permission_classes
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.mixins import ListModelMixin
from rest_framework.views import APIView
from .models import Article
from .serializers import ArticleReadSerializer, ArticleWriteSerializer
from rest_framework.permissions import (
    IsAuthenticated,
    IsAuthenticatedOrReadOnly,
    AllowAny,
)
from rest_framework import status
from comment.models import Comment
from comment.serializers import CommentReadSerializer, CommentWriteSerializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.conf import settings

from account.pagination import CustomPagination


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
def add_view_count(request, pk):
    try:
        articleid = request.data.get("article", "")
        object = Article.objects.filter(id=articleid).first()
        if not object:
            raise
        object.views = object.views + 1
        object.save()
        return Response(True, status=status.HTTP_202_ACCEPTED)
    except:
        return Response(False, status=status.HTTP_400_BAD_REQUEST)



class ArticleViewSet(ModelViewSet):
    queryset = Article.objects.all().order_by("-views")

    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get_serializer_class(self):
        if self.action == "create":
            return ArticleWriteSerializer
        else:
            return ArticleReadSerializer
        


class CommentAPIView(APIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    @swagger_auto_schema(
        operation_description="获取评论",
        manual_parameters=[openapi.Parameter(name='article',in_=openapi.IN_QUERY, description="文章id",type=openapi.TYPE_INTEGER)]
    )
    def get(self, request):
        try:
            articleid = request.query_params.get("article", 1)
            article = Article.objects.filter(id=articleid).first()
            if not article:
                raise
            comment_queryset = Comment.objects.filter(article=article).order_by("is_great")
            

            paginator = CustomPagination()
            page = paginator.paginate_queryset(queryset=comment_queryset, request=request, view=self)

            if page is not None:
                serializer = CommentReadSerializer(
                    page, many=True, context={"request": request}
                )

                return paginator.get_paginated_response(serializer.data)

            serializer = CommentReadSerializer(
                comment_queryset, many=True, context={"request": request}
            )

            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response(False, status=status.HTTP_400_BAD_REQUEST)
    
    @swagger_auto_schema(
        operation_description="添加评论",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=["article", "content"],
            properties={
                "article": openapi.Schema(type=openapi.TYPE_INTEGER, description="文章id"),
                "content": openapi.Schema(type=openapi.TYPE_STRING, description="评论内容"),
            },
        ),
    )
    def post(self, request):
        try:
            articleid = request.data.get("article", "")
            article = Article.objects.filter(id=articleid).first()
            if not article:
                raise
            author = request.user
            content = request.data.get("content", "")
            comment = Comment.objects.create(
                article=article, author=author, content=content
            )
            return Response(True, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response(False, status=status.HTTP_400_BAD_REQUEST)