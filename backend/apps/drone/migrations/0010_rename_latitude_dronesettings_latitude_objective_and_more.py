# Generated by Django 4.2.6 on 2024-03-10 19:56

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("drone", "0009_dronesettings_altitude_objective_and_more"),
    ]

    operations = [
        migrations.RenameField(
            model_name="dronesettings",
            old_name="latitude",
            new_name="latitude_objective",
        ),
        migrations.RenameField(
            model_name="dronesettings",
            old_name="longitude",
            new_name="longitude_objective",
        ),
    ]