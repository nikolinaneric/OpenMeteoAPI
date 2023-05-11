# Generated by Django 4.2.1 on 2023-05-09 17:43

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("weather_retriever", "0002_rename_winds_speed_weatherdata_wind_speed"),
    ]

    operations = [
        migrations.AlterField(
            model_name="weatherdata",
            name="type",
            field=models.CharField(
                choices=[("measured", "measured"), ("forecast", "forecast")],
                max_length=255,
            ),
        ),
    ]
