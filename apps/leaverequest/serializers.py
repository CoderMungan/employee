from rest_framework import serializers
from apps.users.models import CustomUser
from .models import LeaveRequest


class LeaveRequestSerializer(serializers.ModelSerializer):
    user_name = serializers.SerializerMethodField()

    class Meta:
        model = LeaveRequest
        fields = ["id", "start_date", "end_date", "reason", "status", "user_name"]

    def get_user_name(self, obj):
        request = self.context.get("request")
        if request and request.user.is_manager:
            return [
                f"{user.first_name} {user.last_name}" for user in obj.leaverequest.all()
            ]
        return None


class CreateLeaveRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = LeaveRequest
        fields = ["start_date", "end_date", "reason"]

    def validate(self, data):
        # Kullanıcının yeterli yıllık izin gününün olup olmadığını kontrol et
        user = self.context["request"].user
        leave_days = (data["end_date"] - data["start_date"]).days + 1

        if leave_days > (user.annual_leave_days - user.used_leave_days):
            raise serializers.ValidationError("Yeterli yıllık izin gününüz yok.")

        return data


class CustomUserSerializerForLeaveRequest(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            "email",
            "first_name",
            "last_name",
            "annual_leave_days",
            "used_leave_days",
            "is_manager",
        ]
