# Generated by Django 4.2.6 on 2024-01-19 12:18

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("replay", "0003_alter_replaysession_end_time"),
    ]

    operations = [
        migrations.AddField(
            model_name="replaysession",
            name="name",
            field=models.CharField(max_length=255, null=True),
        ),
    ]
