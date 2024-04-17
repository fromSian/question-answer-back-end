from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.mixins import ListModelMixin

from .models import Article
from .serializers import ArticleReadSerializer, ArticleWriteSerializer
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
class ArticleViewSet(ModelViewSet):
    queryset = Article.objects.all().order_by('-views')
    
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get_serializer_class(self):
        if self.action == "create":
            return ArticleWriteSerializer
        else:
            return ArticleReadSerializer
        