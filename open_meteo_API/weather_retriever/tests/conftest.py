import pytest
from datetime import date

from weather_retriever.models import WeatherData


@pytest.fixture
def create_weather_data():
    city_name = 'TestPlace'
    date1 = date(2022, 1, 1)
    date2 = date(2022, 1, 2)
    
    w1 = WeatherData.objects.create(city=city_name, date=date1, max_temperature='20 °C', min_temperature='5 °C', \
                               wind_speed='10.5 km/h', precipitation_sum='2.2 mm', type='forecast')
    w2 = WeatherData.objects.create(city=city_name, date=date1, max_temperature='22 °C', min_temperature='7 °C', \
                               wind_speed='14.5 km/h', precipitation_sum='0.0 mm', type='measured')
    w3 = WeatherData.objects.create(city=city_name, date=date2, max_temperature='24.5 °C', min_temperature='11 °C',\
                                wind_speed='10 km/h', precipitation_sum='5.6 mm',type='forecast')
    w4 = WeatherData.objects.create(city=city_name, date=date2, max_temperature='22.5 °C', min_temperature='9 °C',\
                                wind_speed='11 km/h', precipitation_sum='8.5 mm', type='forecast')
  
    yield w1, w2, w3, w4

    w1.delete()
    w2.delete()
    w3.delete()
    w4.delete()
    


