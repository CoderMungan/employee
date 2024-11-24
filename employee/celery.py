from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from datetime import timedelta

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "employee.settings")

app = Celery("employee")

app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks()

app.conf.beat_schedule = {
    "update-monthly-reports": {
        "task": "apps.users.tasks.calculate_monthly_reports",
        "schedule": timedelta(days=30),
    },
    "send-notifications": {
        "task": "apps.users.tasks.send_notifications",
        "schedule": timedelta(minutes=1),
    },
}
