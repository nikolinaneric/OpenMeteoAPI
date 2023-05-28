from django.db import models
from typing import Dict

# Create your models here.


class WeatherData(models.Model):
    city = models.CharField(max_length=255)
    date = models.DateField()
    max_temperature = models.DecimalField(max_digits=4, decimal_places=2)
    min_temperature = models.DecimalField(max_digits=4, decimal_places=2)
    temperature_units = models.CharField(max_length=255, default="°C")
    wind_speed = models.DecimalField(max_digits=4, decimal_places=2)
    wind_speed_units = models.CharField(max_length=255, default="km/h")
    precipitation_sum = models.DecimalField(max_digits=4, decimal_places=2)
    precipitation_units = models.CharField(max_length=255, default="mm")
    type = models.CharField(
        max_length=255, choices=[
            ("measured", "measured"), ("forecast", "forecast")])

    class Meta:
        db_table = "weather_data"
        app_label = "weather_retriever"

    def get_weather_diff(self, measured_weather):
        max_temp_diff = abs(
            round(self.max_temperature - measured_weather.max_temperature, 2)
        )

        min_temp_diff = abs(
            round(self.min_temperature - measured_weather.min_temperature, 2)
        )

        max_wind_speed_diff = abs(
            round(
                self.wind_speed - measured_weather.wind_speed,
                2))

        precipitation_sum_diff = abs(
            round(
                self.precipitation_sum - measured_weather.precipitation_sum,
                2))
        
        return max_temp_diff, min_temp_diff, max_wind_speed_diff, precipitation_sum_diff

   

