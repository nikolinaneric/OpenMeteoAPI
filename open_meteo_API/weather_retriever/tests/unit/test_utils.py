from datetime import datetime

import pytest

from weather_retriever.models import WeatherData
from weather_retriever.pydantic_models import WeatherDataModel
from weather_retriever.utils import get_location_from_name, organize_data


@pytest.mark.parametrize(
    "place_name, expected_output",
    [
        ("Rogatica", (43.80, 19.00)),
        ("Arandjelovac", (44.31, 20.56)),
        ("Jagodina", (43.98, 21.26)),
    ],
)
def test_get_location_from_name(place_name, expected_output):
    # Testing with towns or smaller cities since the coordinates
    # of larger places tend to vary slightly
    result = get_location_from_name(place_name)
    assert result == expected_output


def test_get_location_from_name_invalid():
    with pytest.raises(ValueError):
        get_location_from_name("Invalid Place Name")


@pytest.mark.django_db
def test_organize_data():
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
            "temperature_2m_max": ["22.5", "20.0"],
            "temperature_2m_min": ["10.0", "12.5"],
            "windspeed_10m_max": ["10.0", "12.5"],
            "precipitation_sum": ["2.5", "0.0"],
        },
    }

    data = WeatherDataModel.parse_obj(mock_data)

    place_name = "TestPlace"
    organize_data(data, place_name)

    saved_data = WeatherData.objects.filter(city=place_name)
    assert len(saved_data) == len(data.daily.time)

    for i, d in enumerate(saved_data):
        date = d.date.strftime("%Y-%m-%d")

        assert d.city == place_name
        assert (
            d.max_temperature ==
            f"{data.daily.temperature_2m_max[i]} {data.daily_units.temperature_2m_max}")
        assert (
            d.min_temperature ==
            f"{data.daily.temperature_2m_min[i]} {data.daily_units.temperature_2m_max}")
        assert (
            d.wind_speed ==
            f"{data.daily.windspeed_10m_max[i]} {data.daily_units.windspeed_10m_max}")
        assert (
            d.precipitation_sum ==
            f"{data.daily.precipitation_sum[i]} {data.daily_units.precipitation_sum}")
        if datetime.strptime(date, "%Y-%m-%d")\
                <= datetime.now():
            assert d.type == "measured"
        else:
            assert d.type == "forecast"
