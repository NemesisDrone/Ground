# Generated by Django 4.2.6 on 2023-12-09 15:44

import apps.drone.models
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("drone", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="dronesettings",
            name="canals",
            field=models.JSONField(default=apps.drone.models.default_canals),
        ),
    ]
