from rest_framework import serializers
from .models import CustomUser


class CustomUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = [
            "id",
            "email",
            "first_name",
            "last_name",
            "user_type",
            "annual_leave_days",
            "used_leave_days",
            "remaining_leave_days",
            "is_manager",
            "is_employee",
        ]
