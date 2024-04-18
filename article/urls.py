from django.urls import path, include 
from rest_framework.routers import DefaultRouter

from . import views 

article_router = DefaultRouter()
article_router.register('article', views.ArticleViewSet, basename='article')
article_router.register('tags', views.TagView)

urlpatterns = [
    path('', include(article_router.urls)),
    path('views/', views.add_view_count, name='add-view'),
    path('comment/great/', views.set_great_comment, name='set_great_comment'),
    path('denounce/', views.denounce, name='denounce'),
    path('comment/', views.CommentAPIView.as_view(), name='comment'),
]