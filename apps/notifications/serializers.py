from rest_framework import serializers
from .models import Notification
from apps.users.serializers import CustomUserSerializer


class NotificationSerializer(serializers.ModelSerializer):
    """
    Bildirimleri serialize eder
    """

    user = CustomUserSerializer(read_only=True)

    class Meta:
        model = Notification
        fields = ["id", "user", "message", "created_at", "is_read"]
