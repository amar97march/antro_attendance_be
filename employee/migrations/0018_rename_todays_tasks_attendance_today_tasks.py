# Generated by Django 5.0.3 on 2024-04-05 06:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0017_remove_attendance_tasks_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='attendance',
            old_name='todays_tasks',
            new_name='today_tasks',
        ),
    ]
