# Generated by Django 5.0.3 on 2024-03-20 08:07

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0003_rename_check_in_time_attendance_check_in_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='attendance',
            name='check_out',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='attendance',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='employee.user'),
        ),
    ]