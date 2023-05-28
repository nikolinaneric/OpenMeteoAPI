from datetime import datetime
from typing import Dict, List
from weather_retriever.models import WeatherData
from typing import Type

import requests

from .pydantic_models import WeatherDataModel


class OpenMeteoWrapper:
    """
    API client for Open Meteo API that estabilishes connection with the API
    and fetches the requested weather data

    Attributes:
        api_url (str): The base URL of the OpenMeteo API.
        daily_params (List[str]): The list of daily parameters to retrieve
        from the API.

    Methods:
        get_weather_data: Fetches weather data from the OpenMeteo API and
        returns it as a WeatherDataModel object.

        Args:
            latitude (float): The latitude of the location
            longitude (float): The longitude of the location
            start_date (str): The start date of the weather data range
            end_date (str): The end date of the weather data range

        Returns:
            WeatherDataModel: A Pydantic model representing the fetched
            weather data.
            Pydantic model is used for validating API response.

        Raises:
            HTTPError: If an HTTP error occurs while fetching data
            from the API.
            ValidationError: If the API response JSON does not match
            the expected format.
        
        organize_data: Extractes weather data retrieved from an API,
        organizes it by date

        Args:
            place name: str
        
        Returns:
            data_dict 

        save_data: Unpacks the data_dict and store the weather_data
        object in database

        Args:
            data_dict: Dict

    """

    def __init__(self) -> None:
        self.api_url: str = "https://api.open-meteo.com/v1/forecast"
        self.daily_params: List[str] = [
            "temperature_2m_max",
            "temperature_2m_min",
            "precipitation_sum",
            "windspeed_10m_max",
        ]

    def get_weather_data(
        self,
        latitude: float,
        longitude: float,
        start_date: str,
        end_date: str,
    ) -> None:
        params = {
            "latitude": latitude,
            "longitude": longitude,
            "start_date": start_date,
            "end_date": end_date,
            "timezone": "UTC",
            "daily": ",".join(self.daily_params),
        }

        response = requests.get(self.api_url, params=params)
        response.raise_for_status()
        data = response.json()
        weather_data = WeatherDataModel.parse_obj(data)
        self.weather_data = weather_data
    
    
    def organize_data(self,
        place_name: str
    ) -> Dict:
        place_name = place_name.replace("-", " ")
        temperature_units = self.weather_data.daily_units.temperature_2m_max
        precipitation_units = self.weather_data.daily_units.precipitation_sum
        wind_speed_units = self.weather_data.daily_units.windspeed_10m_max

        date = self.weather_data.daily.time
        max_temperature = self.weather_data.daily.temperature_2m_max
        min_temperature = self.weather_data.daily.temperature_2m_min
        wind_speed = self.weather_data.daily.windspeed_10m_max
        precipitation_sum = self.weather_data.daily.precipitation_sum
        

        data_dict = {
            place_name: {
                date[i]: {
                    "max_temperature":
                    max_temperature[i],
                    "min_temperature":
                    min_temperature[i],
                    "temperature_units":
                    temperature_units,
                    "wind_speed":
                    wind_speed[i],
                    "wind_speed_units":
                    wind_speed_units,
                    "precipitation_sum":
                    precipitation_sum[i],
                    "precipitation_units":
                    precipitation_units,
                    "type": "measured"
                    if datetime.strptime(date[i], "%Y-%m-%d")
                            <= datetime.now()
                    else "forecast",
                }
                for i in range(len(date))
            }
        }
        return data_dict
    
    def save_data(self, 
        data_dict:Dict
        )-> None:
        for place_name, weather_data in data_dict.items():
            for date, weather_data_on_date in weather_data.items():
                weather_data = WeatherData(
                    city=place_name, date=date, **weather_data_on_date
                )
                weather_data.save()

        print(f"{data_dict}\n\n\
            The data has been succesfully stored on your computer!"
            )

