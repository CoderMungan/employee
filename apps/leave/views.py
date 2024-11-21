from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from .models import Leave
from .serializers import LeaveSerializers
from apps.utils.permissions import IsAdmin


# Create your views here.


class LeaveViewSet(ModelViewSet):
    queryset = Leave.objects.all()
    serializer_class = LeaveSerializers
    permission_classes = [IsAdmin]
