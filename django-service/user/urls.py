from django.urls import path
from .views import UserCreateAPIView, UserLoginAPIView, ProtectedResourceAPIView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('register/', UserCreateAPIView.as_view(), name='create_user'),
]