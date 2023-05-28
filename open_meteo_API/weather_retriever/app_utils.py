from typing import Dict, Type

from django.db.models import Count

from .models import WeatherData


def get_measured_and_forecast_on_same_date(
    Model: Type[WeatherData], city_name: str
) -> Dict:
    """
    Finds in the database table dates for requested city
    that appears more than one time.
    Checks if there are both the measured and the forecast
    conditions for these dates.

    Parameters:
        Model: the database model to use for retrieving
        weather data
        city_name (str): the name of the city to retrieve
        weather data for

    Returns: Dict
        A dictionary where the keys are dates and the values
        are dictionaries containing the latest
        forecast and measured weather conditions for that date.
    """
    dates = (
        Model.objects.filter(city=city_name)
        .values_list("date", flat=True)
        .annotate(date_count=Count("date"))
        .filter(date_count__gt=1)
    ) 

    weather_on_dates = {}
    for date in dates:
        weather_on_dates[date] = {
            "latest_forecast": Model.objects.filter(city=city_name)
            .filter(date=date)
            .filter(type="forecast")
            .last(),
            "measured": Model.objects.filter(city=city_name)
            .filter(date=date)
            .filter(type="measured")
            .last()
        }

    measured_and_forecast_on_dates = {
        k: v
        for k, v in weather_on_dates.items()
        if all(val is not None for val in v.values())
    }
    return measured_and_forecast_on_dates


def calculate_weather_data_diff(measured_and_forecast_on_dates: Dict) -> Dict:
        """
        Calculate the difference between the latest forecast
        and measured weather conditions for each date.

        Parameters:
            measured_and_forecast_on_dates (dict): a dictionary
            where the keys are dates and the values are
            dictionaries containing the latest forecast and
            measured weather conditions for that date.

        Returns: Dict
            A dictionary where the keys are dates and the values
            are dictionaries containing the difference
            between the latest forecast and measured weather conditions
            for that date.
        """
        weather_on_dates_diff = {}
        for date, weather_conditions in measured_and_forecast_on_dates.items():
            forecast_object =  weather_conditions["latest_forecast"]
            measured_object =  weather_conditions["measured"]
            (max_temp_diff, min_temp_diff,
            max_wind_speed_diff, precipitation_sum_diff) =\
            forecast_object.get_weather_diff(measured_object)
            
            weather_on_dates_diff[date] = {
            "date": date,
            "max_temp_forecast": 
            f"{forecast_object.max_temperature} {forecast_object.temperature_units}",
            "max_temp_measured": 
            f"{measured_object.max_temperature} {measured_object.temperature_units}",
            "max_temp_diff": f"{max_temp_diff} {measured_object.temperature_units}",
            "min_temp_forecast": 
            f"{forecast_object.min_temperature} {forecast_object.temperature_units}",
            "min_temp_measured": 
            f"{measured_object.min_temperature} {measured_object.temperature_units}",
            "min_temp_diff": f"{min_temp_diff} {measured_object.temperature_units}",
            "max_wind_speed_forecast":
            f"{forecast_object.wind_speed} {forecast_object.wind_speed_units}",
            "max_wind_speed_measured":
            f"{measured_object.wind_speed} {measured_object.wind_speed_units}",
            "max_wind_speed_diff":
            f"{max_wind_speed_diff} {measured_object.wind_speed_units}",
            "precipitation_sum_forecast":
            f"{forecast_object.precipitation_sum} {forecast_object.precipitation_units}",
            "precipitation_sum_measured":
            f"{measured_object.precipitation_sum} {measured_object.precipitation_units}",
            "precipitation_sum_diff":
            f"{precipitation_sum_diff} {measured_object.precipitation_units}",
        }
        return weather_on_dates_diff