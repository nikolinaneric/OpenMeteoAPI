from datetime import datetime

import pytest

from weather_retriever.models import WeatherData
from weather_retriever.pydantic_models import WeatherDataModel
from weather_retriever.utils import get_location_from_name


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


