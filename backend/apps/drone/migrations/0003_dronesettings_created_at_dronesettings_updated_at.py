# Generated by Django 4.2.6 on 2023-12-09 18:24

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):
    dependencies = [
        ("drone", "0002_alter_dronesettings_canals"),
    ]

    operations = [
        migrations.AddField(
            model_name="dronesettings",
            name="created_at",
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name="dronesettings",
            name="updated_at",
            field=models.DateTimeField(auto_now=True),
        ),
    ]