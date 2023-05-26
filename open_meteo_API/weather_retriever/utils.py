from typing import Tuple

from geopy.geocoders import Nominatim

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


