from rest_framework import serializers
from .models import Leave, LeavePolicy


class LeaveSerializers(serializers.ModelSerializer):
    class Meta:
        model = Leave
        fields = "__all__"


class LeavePolicySerializer(serializers.ModelSerializer):
    class Meta:
        model = LeavePolicy
        fields = "__all__"
