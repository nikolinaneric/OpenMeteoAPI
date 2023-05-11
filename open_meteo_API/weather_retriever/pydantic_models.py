from pydantic import BaseModel, validator
from typing import List


class LocationModel(BaseModel):
    """
    A Pydantic model representing a geographic location.

    Attributes: latitude, longitude

    """
    latitude: float
    longitude: float

    @validator('latitude')
    def validate_latitude(cls, value):
        """
        A Pydantic validator to ensure that the latitude 
        of the location is within a valid range.

        Returns: float
            The latitude of the location, if it is within the valid range.

        Raises: AssertionError
            If the latitude is not within the valid range.
        """
        assert -90 <= value <= 90, f'Invalid latitude value: {value}'
        return value

    @validator('longitude')
    def validate_longitude(cls, value):
        """
        A Pydantic validator to ensure that the longitude 
        of the location is within a valid range.

        Returns: float
            The longitude of the location, if it is within the valid range.

        Raises: AssertionError
            If the longitude is not within the valid range.
        """
        assert -180 <= value <= 180, f'Invalid longitude value: {value}'
        return value
    

class DailyData(BaseModel):
    """
    Pydantic model for checking if the JSON response object 
    contains the daily weather data for specific date
    """
    time: List[str]
    temperature_2m_max: List[float]
    temperature_2m_min: List[float]
    precipitation_sum: List[float]
    windspeed_10m_max: List[float]

class DailyUnits(BaseModel):
    """
    Pydantic model for checking if the JSON response object 
    contains the units for daily weather forecast 
    """
    time: str = 'iso8601'
    temperature_2m_max: str = '°C'
    temperature_2m_min: str = '°C'
    precipitation_sum: str = 'mm'
    windspeed_10m_max: str = 'km/h'

class WeatherDataModel(BaseModel):
    """
    Pydantic model for validating the API response
    given the expected response values
    """
    latitude: float
    longitude: float
    generationtime_ms: float
    utc_offset_seconds: int
    timezone: str
    timezone_abbreviation: str
    elevation: float
    daily_units: DailyUnits
    daily: DailyData
