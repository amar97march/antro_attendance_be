# Generated by Django 5.0.3 on 2024-04-05 05:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0010_rename_today_tasks_completed_attendance_today_tasks_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attendance',
            name='today_tasks_status',
            field=models.BooleanField(blank=True, null=True),
        ),
    ]
