import pytest
from datetime import datetime
from weather_retriever.open_meteo_wrapper import OpenMeteoWrapper
from weather_retriever.pydantic_models import WeatherDataModel
from weather_retriever.models import WeatherData


def test_get_weather_data(mocker, create_mock_data):
    mock_wrapper = OpenMeteoWrapper()
    mock_requests = mocker.patch("requests.get")
    mock_requests.return_value.ok = True
    mock_data = create_mock_data
    mock_requests.return_value.json.return_value = mock_data
    mock_wrapper.get_weather_data(
        40.22, 20.1, "2022-01-01", "2022-01-01")
    mock_requests.assert_called_with(
        "https://api.open-meteo.com/v1/forecast",
        params={
            "latitude": 40.22,
            "longitude": 20.1,
            "start_date": "2022-01-01",
            "end_date": "2022-01-01",
            "timezone": "UTC",
            "daily": "temperature_2m_max,temperature_2m_min,precipitation_sum,windspeed_10m_max",
        },
    )
    weather_data = mock_wrapper.weather_data
    mock_weather_data = WeatherDataModel.parse_obj(mock_data)
    assert weather_data == mock_weather_data


def test_organize_data(get_data_dict_from_mock_data):
    data_dict, _, _, _ = get_data_dict_from_mock_data
    for place_name, place_data in data_dict.items():
        assert isinstance(place_name, str)
        assert place_name == 'TestPlace'
        assert isinstance(place_data, dict)
        assert place_data["2023-05-10"]["max_temperature"] == 22.5

@pytest.mark.django_db
def test_save_data(get_data_dict_from_mock_data):
    (data_dict, weather_data_retriever,
    data, place_name ) = get_data_dict_from_mock_data

    weather_data_retriever.save_data(data_dict)
    saved_data = WeatherData.objects.filter(city=place_name)
    assert len(saved_data) == len(data.daily.time)

    for i, d in enumerate(saved_data):
        date = d.date.strftime("%Y-%m-%d")

        assert d.city == place_name
        assert (
            d.max_temperature ==
            data.daily.temperature_2m_max[i])
        assert (
            d.min_temperature ==
            data.daily.temperature_2m_min[i])
        assert (
            d.wind_speed ==
            data.daily.windspeed_10m_max[i])
        assert (
            d.precipitation_sum ==
            data.daily.precipitation_sum[i])
        if datetime.strptime(date, "%Y-%m-%d")\
                <= datetime.now():
            assert d.type == "measured"
        else:
            assert d.type == "forecast"
