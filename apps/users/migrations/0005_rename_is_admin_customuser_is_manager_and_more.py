# Generated by Django 4.2.7 on 2024-11-22 08:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_remove_customuser_monthly_work_hours'),
    ]

    operations = [
        migrations.RenameField(
            model_name='customuser',
            old_name='is_admin',
            new_name='is_manager',
        ),
        migrations.AddField(
            model_name='customuser',
            name='monthly_working_hours',
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name='customuser',
            name='remaining_leave_days',
            field=models.FloatField(default=15.0),
        ),
        migrations.AddField(
            model_name='customuser',
            name='total_late_minutes',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='customuser',
            name='used_leave_days',
            field=models.FloatField(default=0.0),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='annual_leave_days',
            field=models.FloatField(default=15.0),
        ),
    ]
