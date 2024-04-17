from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views 


urlpatterns = [
    path('login/', views.account_login, name='account-login'),
    path('register/', views.account_registration, name="account-registration"),
    path('info/', views.user_info, name="user-info"),
]