# Generated by Django 4.2.7 on 2024-11-23 15:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_customuser_leaverequest_alter_customuser_worklog'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='remaining_leave_days',
            field=models.FloatField(default=15.0),
        ),
    ]