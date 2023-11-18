from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView, TokenBlacklistView
from rest_framework import routers

from . import views



urlpatterns = [
    path('api/user/token', views.UserLoginView.as_view(), name='token_obtain_pair'),
    path('api/user/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path("api/user/blacklist", TokenBlacklistView.as_view(), name="token_blacklist"),
    path("api/user/data", views.get_user_data, name="user_data"),
]
