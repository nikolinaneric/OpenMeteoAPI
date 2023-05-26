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
        max_temp_forecast, temp_unit = (
            weather_conditions["latest_forecast"].max_temperature
        ).split(" ")
        max_temp_measured = (weather_conditions["measured"]
                             .max_temperature).strip(" °C"
                                                     )
        max_temp_diff = abs(
            round((float(max_temp_forecast) - float(max_temp_measured)), 2)
        )

        min_temp_forecast = (
            weather_conditions["latest_forecast"].min_temperature
        ).strip(" °C")
        min_temp_measured = (weather_conditions["measured"]
                             .min_temperature).strip(" °C"
                                                     )
        min_temp_diff = abs(
            round((float(min_temp_forecast) - float(min_temp_measured)), 2)
        )

        max_wind_speed_forecast, wind_speed_unit = (
            weather_conditions["latest_forecast"].wind_speed
        ).split(" ")
        max_wind_speed_measured = (
            weather_conditions["measured"].wind_speed).strip(" km/h")
        max_wind_speed_diff = abs(
            round(
                (float(max_wind_speed_forecast) -
                 float(max_wind_speed_measured)),
                2))

        precipitation_sum_forecast, precipitation_sum_unit = (
            weather_conditions["latest_forecast"].precipitation_sum
        ).split(" ")
        precipitation_sum_measured = (
            weather_conditions["measured"].precipitation_sum
        ).strip(" mm")
        precipitation_sum_diff = abs(
            round(
                (float(precipitation_sum_forecast) -
                 float(precipitation_sum_measured)),
                2,))

        weather_on_dates_diff[date] = {
            "date": date,
            "max_temp_forecast": f"{max_temp_forecast} {temp_unit}",
            "max_temp_measured": f"{max_temp_measured} {temp_unit}",
            "max_temp_diff": f"{max_temp_diff} {temp_unit}",
            "min_temp_forecast": f"{min_temp_forecast} {temp_unit}",
            "min_temp_measured": f"{min_temp_measured} {temp_unit}",
            "min_temp_diff": f"{min_temp_diff} {temp_unit}",
            "max_wind_speed_forecast":
            f"{max_wind_speed_forecast} {wind_speed_unit}",
            "max_wind_speed_measured":
            f"{max_wind_speed_measured} {wind_speed_unit}",
            "max_wind_speed_diff":
            f"{max_wind_speed_diff} {wind_speed_unit}",
            "precipitation_sum_forecast":
            f"{precipitation_sum_forecast} {precipitation_sum_unit}",
            "precipitation_sum_measured":
            f"{precipitation_sum_measured} {precipitation_sum_unit}",
            "precipitation_sum_diff":
            f"{precipitation_sum_diff} {precipitation_sum_unit}",
        }
    return weather_on_dates_diff
