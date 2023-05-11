import requests
from typing import Dict
from datetime import datetime
from .pydantic_models import DailyData, DailyUnits, WeatherDataModel


class OpenMeteoWrapper():
    """
    API client for Open Meteo API that estabilishes connection with the API
    and fetches the requested weather data

    Attributes:
        api_url (str): The base URL of the OpenMeteo API.
        daily_params (List[str]): The list of daily parameters to retrieve from the API.

    Methods:
        get_weather_data: Fetches weather data from the OpenMeteo API and returns it as a WeatherDataModel object.

        Args:
            latitude (float): The latitude of the location to fetch weather data for.
            longitude (float): The longitude of the location to fetch weather data for.
            start_date (datetime): The start date of the weather data range.
            end_date (datetime): The end date of the weather data range.

        Returns:
            WeatherDataModel: A Pydantic model representing the fetched weather data.
            Pydantic model is used for validating API response.

        Raises:
            HTTPError: If an HTTP error occurs while fetching data from the API.
            ValidationError: If the API response JSON does not match the expected format.

    """

    def __init__(self):
        self.api_url = 'https://api.open-meteo.com/v1/forecast'
        self.daily_params = ["temperature_2m_max", "temperature_2m_min",
                             "precipitation_sum", "windspeed_10m_max"]

    def get_weather_data(self, latitude: float, longitude: float, start_date: datetime,
                         end_date: datetime) -> Dict:
        params = {
            'latitude': latitude,
            'longitude': longitude,
            'start_date': start_date,
            'end_date': end_date,
            'timezone': 'UTC',
            'daily': ','.join(self.daily_params)
        }

        response = requests.get(self.api_url, params=params)
        response.raise_for_status()
        data = response.json()
        weather_data = WeatherDataModel.parse_obj(data)
        return weather_data