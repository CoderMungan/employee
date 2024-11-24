from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import LeaveRequest
from .serializers import LeaveRequestSerializer, CreateLeaveRequestSerializer


class LeaveRequestViewSet(viewsets.ModelViewSet):
    queryset = LeaveRequest.objects.all()
    serializer_class = LeaveRequestSerializer

    def get_queryset(self):
        user = self.request.user
        # Personel kendi izin taleplerini görebilir
        if user.is_employee and not user.is_manager:
            return user.leaverequest.all()
        # Yönetici tüm izin taleplerini görebilir
        elif user.is_manager:
            return LeaveRequest.objects.all()
        return LeaveRequest.objects.none()

    def get_serializer_class(self):
        if self.action == "create":
            return CreateLeaveRequestSerializer
        return LeaveRequestSerializer

    def get_serializer_context(self):
        return {"request": self.request}

    def create(self, request, *args, **kwargs):
        user = request.user
        serializer = self.get_serializer(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        leave_request = serializer.save()
        user.leaverequest.add(leave_request)
        leave_days = (leave_request.end_date - leave_request.start_date).days + 1
        user.used_leave_days += leave_days
        user.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(
        detail=True, methods=["post"], permission_classes=[permissions.IsAuthenticated]
    )
    def approve(self, request, pk=None):
        leave_request = self.get_object()
        if not request.user.is_manager:
            return Response(
                {"detail": "Onaylama yetkiniz yok."}, status=status.HTTP_403_FORBIDDEN
            )
        leave_request.status = "approved"
        leave_request.save()
        return Response({"detail": "İzin talebi onaylandı."}, status=status.HTTP_200_OK)

    @action(
        detail=True, methods=["post"], permission_classes=[permissions.IsAuthenticated]
    )
    def reject(self, request, pk=None):
        leave_request = self.get_object()
        if not request.user.is_manager:
            return Response(
                {"detail": "Reddetme yetkiniz yok."}, status=status.HTTP_403_FORBIDDEN
            )
        leave_request.status = "rejected"
        leave_request.save()
        return Response(
            {"detail": "İzin talebi reddedildi."}, status=status.HTTP_200_OK
        )
