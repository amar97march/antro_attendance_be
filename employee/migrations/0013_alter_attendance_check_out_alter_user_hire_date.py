# Generated by Django 5.0.3 on 2024-03-22 05:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0012_alter_attendance_check_out_alter_user_hire_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attendance',
            name='check_out',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='hire_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]