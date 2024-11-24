from django.db import models
from apps.users.models import CustomUser
from django.utils.timezone import now


class Notification(models.Model):
    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="notifications"
    )
    message = models.TextField()
    created_at = models.DateTimeField(default=now)
    is_read = models.BooleanField(default=False)
