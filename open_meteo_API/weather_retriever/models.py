from django.db import models

# Create your models here.


class WeatherData(models.Model):
    city = models.CharField(max_length=255)
    date = models.DateField()
    max_temperature = models.CharField(max_length=255)
    min_temperature = models.CharField(max_length=255)
    wind_speed = models.CharField(max_length=255)
    precipitation_sum = models.CharField(max_length=255)
    type = models.CharField(max_length=255, choices = [('measured', 'measured'), ('forecast', 'forecast')])

    class Meta:
        db_table = 'weather_data'
        app_label = 'weather_retriever'
  
