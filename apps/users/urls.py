from django.urls import path

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import UserInformation

app_name = "api/users"

urlpatterns = [
    path("login/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("login/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("user-info/", UserInformation.as_view(), name="user-info"),
]
