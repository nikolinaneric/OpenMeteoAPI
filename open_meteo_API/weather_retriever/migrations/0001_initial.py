# Generated by Django 4.2.1 on 2023-05-09 16:16

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="WeatherData",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("city", models.CharField(max_length=255)),
                ("date", models.DateField()),
                ("max_temperature", models.CharField(max_length=255)),
                ("min_temperature", models.CharField(max_length=255)),
                ("winds_speed", models.CharField(max_length=255)),
                ("precipitation_sum", models.CharField(max_length=255)),
                ("type", models.CharField(max_length=255)),
            ],
        ),
    ]
