# Generated by Django 4.2.1 on 2023-05-09 17:24

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("weather_retriever", "0001_initial"),
    ]

    operations = [
        migrations.RenameField(
            model_name="weatherdata",
            old_name="winds_speed",
            new_name="wind_speed",
        ),
    ]
