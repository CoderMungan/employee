from django.urls import path, include
from .views import LeaveRequestViewSet
from rest_framework.routers import DefaultRouter

app_name = "api/leaverequest"

router = DefaultRouter()
router.register(r"leave-requests", LeaveRequestViewSet, basename="leave-requests")

urlpatterns = [
    path("", include(router.urls)),
]
