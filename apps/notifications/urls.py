from django.urls import path
from .views import NotificationView

app_name = "api/notifications"

urlpatterns = [
    path("", NotificationView.as_view(), name="notifications"),
]
