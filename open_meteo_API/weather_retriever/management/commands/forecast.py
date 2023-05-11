import argparse
from typing import Dict
from weather_retriever.utils import get_location_from_name, organize_data
from datetime import datetime
from django.core.management.base import BaseCommand, CommandError
from datetime import timedelta
from weather_retriever.open_meteo_wrapper import OpenMeteoWrapper


class ValidateDateAction(argparse.Action):
    """
    An argparse action that validates that a given date string is in the
    format 'YYYY-MM-DD' and falls within an acceptable range of dates.
    """

    def __call__(self, parser, namespace, values, option_string=None):
        try:
            date = datetime.strptime(values, "%Y-%m-%d").date()
        except ValueError:
            msg = f"Invalid date format: '{values}'. Must be in the format YYYY-MM-DD."
            parser.error(msg)
        if date > datetime.now().date() + timedelta(days=16):
            msg = f"The date: '{values}' is too far ahead to have a forecast."
            parser.error(msg)
        if date < datetime.now().date() - timedelta(days=106):
            msg = f"The date: '{values}' is too far away to have a forecast history."
            parser.error(msg)
        else:
            setattr(namespace, self.dest, values)

class Command(BaseCommand):
    """
    A Django management command that calls 
    the get_location_from_name that returns coordinates based
    on the place name.

    Instantiates the client for OpetMeteoApi and invokes the get_weather_data
    the method that will return the validated object from the API response.

    Finally, it calls the organize_data that will extract values from 
    the response and store it in the database.
    
    Raises:
        ValueError: If the end date is earlier than the start date.
    """
    def add_arguments(self, parser):
        parser.add_argument(
            "place_name", type=str, help="City name with hyphens if there are more than one word (Novi-Sad)")
        parser.add_argument("start_date", type=str,
                            help="Start date of data range (YYYY-MM-DD)", action=ValidateDateAction)
        parser.add_argument("end_date", type=str,
                            help="End date of data range (YYYY-MM-DD)", action=ValidateDateAction)

    def handle(self, *args, **options):
        if options["start_date"] > options["end_date"]:
            raise ValueError(f"End date must be greater than or equal to start date.")
        location = get_location_from_name(options["place_name"])
        weather_data_client = OpenMeteoWrapper()
        data = weather_data_client.get_weather_data(
            *location, options["start_date"], options["end_date"])
        organize_data(data, options["place_name"])