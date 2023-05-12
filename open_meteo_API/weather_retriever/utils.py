from datetime import datetime
from typing import Tuple, Type

from geopy.geocoders import Nominatim

from weather_retriever.models import WeatherData

from .pydantic_models import LocationModel


def get_location_from_name(place_name: str) -> Tuple[float, float]:
    """
    Returns the latitude and longitude of a geographic location
    based on its name, using the geopy.geocode Nominatim class.
    The location format is validated with Pydantic model - LocationModel.


    Returns: Tuple[float, float]
        The latitude and longitude of the geographic location
        rounded up to 2 decimals
        (**Results for larger places can vary from 0,001-0,003
        in contrast to coordinates on OpenMeteoApi)

    Raises: ValueError
        If the location cannot be found.

    """
    nom_loc = Nominatim(user_agent="weather_data_retriever")
    place_name = place_name.replace("-", " ")
    try:
        location = nom_loc.geocode(place_name)
        location_model = LocationModel(
            latitude=location.latitude,
            longitude=location.longitude
        )
        latitude = round(location_model.latitude, 2)
        longitude = round(location_model.longitude, 2)
        return latitude, longitude

    except Exception as e:
        raise ValueError("Error in finding Area & Coordinates.", e)


def organize_data(
        data: Type[WeatherData], place_name: str
) -> None:
    """
    Extractes weather data retrieved from an API,
    organizes it by date and stores it in a database.
    (Using Django model WeatherData)

    Parameters:
        WeatherData(Pydantic model) object that containts
        valited weather data
    """
    place_name = place_name.replace("-", " ")
    temperature_units = data.daily_units.temperature_2m_max
    precipitation_units = data.daily_units.precipitation_sum
    wind_speed_units = data.daily_units.windspeed_10m_max

    date = data.daily.time
    max_temperature = data.daily.temperature_2m_max
    min_temperature = data.daily.temperature_2m_min
    wind_speed = data.daily.windspeed_10m_max
    precipitation_sum = data.daily.precipitation_sum

    data_dict = {
        place_name: {
            date[i]: {
                "max_temperature":
                f"{max_temperature[i]} {temperature_units}",
                "min_temperature":
                f"{min_temperature[i]} {temperature_units}",
                "wind_speed":
                f"{wind_speed[i]} {wind_speed_units}",
                "precipitation_sum":
                f"{precipitation_sum[i]} {precipitation_units}",
                "type": "measured"
                if datetime.strptime(date[i], "%Y-%m-%d")
                        <= datetime.now()
                else "forecast",
            }
            for i in range(len(date))
        }
    }

    for place_name, data in data_dict.items():
        for date, data1 in data.items():
            weather_data = WeatherData(
                city=place_name, date=date, **data1
            )
            weather_data.save()

    print(f"{data_dict}\n\n\
           The data has been succesfully stored on your computer!"
          )
