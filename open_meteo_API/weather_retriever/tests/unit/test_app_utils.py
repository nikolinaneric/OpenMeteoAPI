import pytest
import datetime
from weather_retriever.models import WeatherData
from weather_retriever.app_utils import get_measured_and_forecast_on_same_date, calculate_weather_data_diff

@pytest.mark.django_db
def test_get_measured_and_forecast_on_same_date(create_weather_data):
    city_name = 'TestPlace'
    result = get_measured_and_forecast_on_same_date(WeatherData, city_name)
    for key,value in result.items():
        assert key == datetime.date(2022, 1, 1)
        key_value1, key_value2 = value.items()
        assert key_value1[0] == 'latest_forecast'
        assert key_value2[0] == 'measured'
        assert (key_value1[1]).city == (key_value2[1]).city==city_name
        if (key_value1[1]).type == 'forecast':
            assert (key_value1[1]).wind_speed == '10.5 km/h'
            assert (key_value1[1]).precipitation_sum == '2.2 mm'
        else:
            assert (key_value1[2]).wind_speed == '10.5 km/h'
            assert (key_value1[2]).precipitation_sum == '2.2 mm'

@pytest.mark.django_db
def test_calculate_weather_data_diff(create_weather_data):
    w1, w2, _, _ = create_weather_data
    input_data = {
        '2022-01-01': {
            'measured': w2,
            'latest_forecast': w1
        }
    }

    result = calculate_weather_data_diff(input_data)

    assert isinstance(result, dict)
    assert result['2022-01-01']['max_temp_diff'] == '2.0 °C'
    assert result['2022-01-01']['min_temp_diff'] == '2.0 °C'
    assert result['2022-01-01']['max_wind_speed_diff'] == '4.0 km/h'
    assert result['2022-01-01']['precipitation_sum_diff'] == '2.2 mm'
  