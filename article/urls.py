from django.urls import path, include 
from rest_framework.routers import DefaultRouter

from . import views 

router = DefaultRouter()
router.register('article', views.ArticleViewSet, basename='article')
router.register('comment', views.CommentViewSet, basename='comment')
router.register('tags', views.TagView)

urlpatterns = [
    path('', include(router.urls)),
    path('views/', views.add_view_count, name='add-view'),
    path('comment/great/', views.set_great_comment, name='set_great_comment'),
    path('denounce/', views.denounce, name='denounce'),
]