# Generated by Django 5.0.3 on 2024-04-05 04:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0016_delete_employee'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='attendance',
            name='tasks',
        ),
        migrations.AddField(
            model_name='attendance',
            name='today_tasks_status',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='attendance',
            name='todays_tasks',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='attendance',
            name='tomorrow_tasks',
            field=models.TextField(blank=True, null=True),
        ),
    ]
