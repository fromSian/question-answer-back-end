from django.urls import path, include 
from rest_framework.routers import DefaultRouter

from . import views 

article_router = DefaultRouter()
article_router.register('article', views.ArticleViewSet, basename='article')
# article_router.register('tags', views.TagView)

urlpatterns = [
    path('', include(article_router.urls))
]