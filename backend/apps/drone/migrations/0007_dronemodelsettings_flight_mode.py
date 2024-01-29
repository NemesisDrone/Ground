# Generated by Django 4.2.6 on 2024-01-29 15:11

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("drone", "0006_remove_dronemodelsettings_prediction_model"),
    ]

    operations = [
        migrations.AddField(
            model_name="dronemodelsettings",
            name="flight_mode",
            field=models.CharField(
                choices=[("manual", "Manual"), ("autonomous", "Autonomous")],
                default="manual",
                max_length=255,
            ),
        ),
    ]
