# Generated by Django 4.2.7 on 2024-11-23 14:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('leaverequest', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='leaverequest',
            name='reviewed_by',
        ),
        migrations.RemoveField(
            model_name='leaverequest',
            name='user',
        ),
    ]