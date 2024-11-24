from django.db import models
from django.utils.timezone import now


class LeaveRequest(models.Model):

    STATUS_CHOICES = (
        ("pending", "Beklemede"),
        ("approved", "Onaylandı"),
        ("rejected", "Reddedildi"),
    )
    start_date = models.DateField()
    end_date = models.DateField()
    reason = models.TextField(blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="pending")
    created_at = models.DateTimeField(default=now)

    def leave_duration(self):
        return (self.end_date - self.start_date).days + 1
