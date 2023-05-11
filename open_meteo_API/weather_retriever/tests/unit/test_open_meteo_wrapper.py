import pytest
from weather_retriever.open_meteo_wrapper import OpenMeteoWrapper
from weather_retriever.pydantic_models import WeatherDataModel

def test_get_weather_data(mocker):
    mock_wrapper = OpenMeteoWrapper()
    mock_requests = mocker.patch("requests.get")
    mock_requests.return_value.ok = True
    mock_data = {'latitude': 43.75, 'longitude': 19.0625, 
                    'generationtime_ms': 0.286102294921875, 
                    'utc_offset_seconds': 0, 'timezone': 'UTC',
                    'timezone_abbreviation': 'UTC', 'elevation': 538.0,
                    'daily_units': {'time': 'iso8601', 'temperature_2m_max': '°C',
                    'temperature_2m_min': '°C', 'precipitation_sum': 'mm',
                    'windspeed_10m_max': 'km/h'}, 'daily': {'time': ['2023-05-06'],
                    'temperature_2m_max': [21.8], 'temperature_2m_min': [4.8],
                    'precipitation_sum': [0.0], 'windspeed_10m_max': [9.6]}}
                   
    mock_requests.return_value.json.return_value= mock_data

    data = mock_wrapper.get_weather_data(40.22, 20.1, '2022-01-01',
                         '2022-01-01')
    mock_requests.assert_called_with("https://api.open-meteo.com/v1/forecast",\
                                     params={'latitude': 40.22, 'longitude': 20.1, 'start_date': '2022-01-01',
                                              'end_date': '2022-01-01', 'timezone': 'UTC', 
                                              'daily': 'temperature_2m_max,temperature_2m_min,precipitation_sum,windspeed_10m_max'})
    weather_data = WeatherDataModel.parse_obj(data)
    mock_weather_data = WeatherDataModel.parse_obj(mock_data)
    assert  weather_data == mock_weather_data