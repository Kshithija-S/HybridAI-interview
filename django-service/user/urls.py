from django.urls import path
from .views import UserCreateAPIView, UserLoginAPIView, UserActivityAPIView

urlpatterns = [
    path('register/', UserCreateAPIView.as_view(), name='create_user'),
    path('login/', UserLoginAPIView.as_view(), name='login_user'),
    path('activity/', UserActivityAPIView.as_view(), name='user_activity'),
]