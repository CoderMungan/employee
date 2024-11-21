from django.db import models
from apps.users.models import CustomUser
from datetime import timedelta


class WorkLog(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    check_in_time = models.DateTimeField(null=True, blank=True)
    check_out_time = models.DateTimeField(null=True, blank=True)
    late_duration = models.DurationField(default=timedelta)  # Geç kalınan süre

    def calculate_late_duration(self, start_time):
        # Geç kalma süresini hesaplar
        if self.check_in_time and self.check_in_time > start_time:
            self.late_duration = self.check_in_time - start_time
        else:
            self.late_duration = timedelta(0)
        self.save()


class MonthlyReport(models.Model):
    # Aylık çalışma saat raporları
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    month = models.DateField()  # Hangi aya ait olduğu
    total_work_hours = models.DecimalField(max_digits=6, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.user.username} - {self.month.strftime('%B %Y')}"
