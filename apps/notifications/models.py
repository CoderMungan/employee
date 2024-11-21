from django.db import models
from apps.users.models import CustomUser

# Create your models here.


class Notification(models.Model):
    # Yetkiliye bildirimler
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification for {self.user.username} - {self.created_at}"
