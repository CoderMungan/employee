from django.db import models
from django.utils.timezone import now
from datetime import timedelta, date


class Holiday(models.Model):
    name = models.CharField(max_length=100)
    date = models.DateField(unique=True)

    def __str__(self):
        return f"{self.name} - {self.date}"
