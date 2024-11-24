from django.db import models
from apps.utils.models import TimestampModel
from django.utils.timezone import now
from datetime import timedelta


class WorkLog(TimestampModel):
    date = models.DateField(default=now)
    check_in_time = models.TimeField(null=True, blank=True)
    check_out_time = models.TimeField(null=True, blank=True)
    late_minutes = models.PositiveIntegerField(default=0)
    is_holiday = models.BooleanField(default=False)
    total_worked_hours = models.FloatField(default=0.0)
    is_late_deducted = models.BooleanField(default=False)

    def calculate_late_minutes(self):
        company_start_time = timedelta(hours=8)
        company_end_time = timedelta(hours=18)

        if self.check_in_time:
            check_in = timedelta(
                hours=self.check_in_time.hour, minutes=self.check_in_time.minute
            )

            if company_start_time <= check_in <= company_end_time:
                if check_in > company_start_time:
                    self.late_minutes = int(
                        (check_in - company_start_time).total_seconds() / 60
                    )
                else:
                    self.late_minutes = 0
            else:
                self.late_minutes = 0

    def calculate_total_worked_hours(self):
        if self.check_in_time and self.check_out_time:
            check_in = timedelta(
                hours=self.check_in_time.hour, minutes=self.check_in_time.minute
            )
            check_out = timedelta(
                hours=self.check_out_time.hour, minutes=self.check_out_time.minute
            )
            self.total_worked_hours = round(
                (check_out - check_in).total_seconds() / 3600, 2
            )

    def is_weekend(self):
        return self.date.weekday() >= 5

    def check_holiday(self):
        return Holiday.objects.filter(date=self.date).exists()

    def save(self, *args, **kwargs):
        self.is_holiday = self.is_weekend() or self.check_holiday()
        self.calculate_late_minutes()
        self.calculate_total_worked_hours()
        super().save(*args, **kwargs)

    class Meta:
        unique_together = ("date",)
        ordering = ["-date"]

    def __str__(self):
        return f"{self.date}"
