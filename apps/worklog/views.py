from rest_framework.views import APIView
from rest_framework.response import Response
from apps.utils.permissions import IsEmployeeWithAuth, IsManagerWithAuth
from rest_framework import status
from .models import WorkLog
from datetime import date, datetime


class CheckInView(APIView):
    permission_classes = [IsEmployeeWithAuth]

    def post(self, request, *args, **kwargs):
        user = request.user
        today = date.today()

        if user.worklog.filter(date=today).exists():
            return Response(
                {"error": "Bugün için zaten giriş yapılmış."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        check_in_time = datetime.now().time()
        worklog = WorkLog.objects.create(date=today, check_in_time=check_in_time)
        user.worklog.add(worklog)

        return Response(
            {"message": "Başarıyla giriş yapıldı.", "check_in_time": check_in_time},
            status=status.HTTP_201_CREATED,
        )


class CheckOutView(APIView):
    permission_classes = [IsEmployeeWithAuth]

    def post(self, request, *args, **kwargs):
        user = request.user
        today = date.today()

        try:
            worklog = user.worklog.get(date=today)
        except WorkLog.DoesNotExist:
            return Response(
                {"error": "Giris Kaydi Bulunamadi."}, status=status.HTTP_400_BAD_REQUEST
            )

        if worklog.check_out_time:
            return Response(
                {"error": "Bugun zaten cikis yapilmis."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        check_out_time = datetime.now().time()
        worklog.check_out_time = check_out_time
        worklog.save()

        user.monthly_working_hours += worklog.total_worked_hours
        user.total_late_minutes += worklog.late_minutes
        user.save()

        return Response(
            {"message": "Basariyla Cikis Yapildi.", "check_out_time": check_out_time},
            status=status.HTTP_200_OK,
        )


class DailySummaryView(APIView):
    permission_classes = [IsManagerWithAuth]

    def get(self, request, *args, **kwargs):
        user = request.user
        today = date.today()

        try:
            worklog = user.worklog.get(date=today)
        except WorkLog.DoesNotExist:
            return Response(
                {"error": "Bugun zaten cikis yapilmis."},
                status=status.HTTP_404_NOT_FOUND,
            )

        data = {
            "date": str(worklog.date),
            "check_in_time": (
                str(worklog.check_in_time) if worklog.check_in_time else None
            ),
            "check_out_time": (
                str(worklog.check_out_time) if worklog.check_out_time else None
            ),
            "total_worked_hours": worklog.total_worked_hours,
            "late_minutes": worklog.late_minutes,
        }

        return Response(data, status=status.HTTP_200_OK)


class MonthlySummaryView(APIView):
    permission_classes = [IsManagerWithAuth]

    def get(self, request, *args, **kwargs):
        user = request.user
        current_month = date.today().month

        worklogs = user.worklog.filter(date__month=current_month)
        total_worked_hours = sum(wl.total_worked_hours for wl in worklogs)
        total_late_minutes = sum(wl.late_minutes for wl in worklogs)

        data = {
            "total_worked_hours": total_worked_hours,
            "total_late_minutes": total_late_minutes,
            "worklogs": [
                {
                    "date": str(wl.date),
                    "check_in_time": (
                        str(wl.check_in_time) if wl.check_in_time else None
                    ),
                    "check_out_time": (
                        str(wl.check_out_time) if wl.check_out_time else None
                    ),
                    "total_worked_hours": wl.total_worked_hours,
                    "late_minutes": wl.late_minutes,
                }
                for wl in worklogs
            ],
        }

        return Response(data, status=status.HTTP_200_OK)
