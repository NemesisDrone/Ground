# Generated by Django 4.2.6 on 2024-01-24 23:08

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("drone", "0005_remove_dronesettings_canals_dronemodelsettings_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="dronemodelsettings",
            name="prediction_model",
        ),
    ]
