from celery import shared_task
from django.db.models import Sum
from datetime import date
from apps.users.models import CustomUser
from apps.notifications.models import Notification
from apps.utils.logger import logger


@shared_task
def calculate_monthly_reports():
    today = date.today()
    users = CustomUser.objects.all()

    for user in users:
        worklog = user.worklog.filter(date__month=today.month, date__year=today.year)

        total_work_hours = (
            worklog.aggregate(Sum("total_worked_hours"))["total_worked_hours__sum"] or 0
        )
        total_late_minutes = (
            worklog.aggregate(Sum("late_minutes"))["late_minutes__sum"] or 0
        )

        if total_late_minutes > 0:
            hours_deducted = total_late_minutes / 60 / 8
            user.annual_leave_days -= hours_deducted
            user.save()

        logger.info(
            f"{user.email}: {total_work_hours} saat çalıştı, {total_late_minutes} dakika geç kaldı."
        )

    return "Aylık hesaplama tamamlandı!"


@shared_task
def send_notification_to_admin():

    users = CustomUser.objects.all()
    for user in users:
        if user.remaining_leave_days < 3:
            admin_user = CustomUser.objects.filter(user_type="admin").first()
            if admin_user:
                existing_notification = Notification.objects.filter(
                    user=admin_user,
                    message=f"{user.first_name} {user.last_name} adlı personelin yıllık izni 3 günden az!",
                ).exists()

                if not existing_notification:
                    Notification.objects.create(
                        user=admin_user,
                        message=f"{user.first_name} {user.last_name} adlı personelin yıllık izni 3 günden az!",
                    )
    return "Notification task worked!"
