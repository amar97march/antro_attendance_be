# Generated by Django 5.0.3 on 2024-03-21 04:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0005_remove_user_username'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_superuser',
            field=models.BooleanField(default=False),
        ),
    ]
