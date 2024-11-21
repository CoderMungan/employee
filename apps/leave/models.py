from django.db import models
from apps.utils.models import TimestampModel
from apps.users.models import CustomUser
from datetime import timedelta

# Create your models here.


class Leave(TimestampModel):
    # İzin kayıtları
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    is_approved = models.BooleanField(default=False)  # Yetkili onayı

    @property
    def total_days(self):
        return (self.end_date - self.start_date).days + 1

    def __str__(self):
        return f"{self.user.username} ({self.start_date} - {self.end_date})"


class LeavePolicy(TimestampModel):
    # İzin politikası
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    deduction_hours = models.DurationField(
        default=timedelta
    )  # Geç kalmalardan kesilen süre

    def apply_late_deduction(self):
        if self.deduction_hours.total_seconds() > 0:
            self.user.annual_leave_days -= self.deduction_hours.total_seconds() / (
                60 * 60 * 24
            )
            self.user.save()

    def __str__(self):
        return f"Policy for {self.user.username}"
