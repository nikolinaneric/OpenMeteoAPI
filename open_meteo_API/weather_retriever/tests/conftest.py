from datetime import date

import pytest

from weather_retriever.models import WeatherData

from weather_retriever.pydantic_models import WeatherDataModel

from weather_retriever.open_meteo_wrapper import OpenMeteoWrapper

@pytest.fixture
def create_weather_data():
    city_name = "TestPlace"
    date1 = date(2022, 1, 1)
    date2 = date(2022, 1, 2)

    w1 = WeatherData.objects.create(
        city=city_name,
        date=date1,
        max_temperature=20,
        min_temperature=5,
        wind_speed=10.5,
        precipitation_sum=2.2,
        type="forecast",
    )
    w2 = WeatherData.objects.create(
        city=city_name,
        date=date1,
        max_temperature=22,
        min_temperature=7,
        wind_speed=14.5,
        precipitation_sum=0.0,
        type="measured",
    )
    w3 = WeatherData.objects.create(
        city=city_name,
        date=date2,
        max_temperature=24.5,
        min_temperature=11,
        wind_speed=10,
        precipitation_sum=5.6,
        type="forecast",
    )
    w4 = WeatherData.objects.create(
        city=city_name,
        date=date2,
        max_temperature=22.5,
        min_temperature=9,
        wind_speed=11,
        precipitation_sum=8.5,
        type="forecast",
    )

    yield w1, w2, w3, w4

    w1.delete()
    w2.delete()
    w3.delete()
    w4.delete()

@pytest.fixture
def create_mock_data():
    mock_data = {
        "latitude": 43.98,
        "longitude": 21.26,
        "generationtime_ms": 0.003,
        "utc_offset_seconds": 1,
        "timezone": "UTC",
        "timezone_abbreviation": "UTC",
        "elevation": 2,
        "daily_units": {
            "time": "iso8601",
            "temperature_2m_max": "°C",
            "precipitation_sum": "mm",
            "windspeed_10m_max": "km/h",
        },
        "daily": {
            "time": ["2023-05-10", "2023-05-11"],
            "temperature_2m_max": [22.5, 20.0],
            "temperature_2m_min": [10.0, 12.5],
            "windspeed_10m_max": [10.0, 12.5],
            "precipitation_sum": [2.5, 0.0],
        },
    }

    yield mock_data

@pytest.fixture
def get_data_dict_from_mock_data(create_mock_data):
    mock_data = create_mock_data
    data = WeatherDataModel.parse_obj(mock_data)
    weather_data_retriever = OpenMeteoWrapper()
    weather_data_retriever.weather_data = data
    place_name = "TestPlace"
    data_dict = weather_data_retriever.organize_data(place_name)
    yield data_dict, weather_data_retriever, data, place_name