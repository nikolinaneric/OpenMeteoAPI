# OpenMeteo

Description: The package that creates API client for https://open-meteo.com/en/docs, retrieves max daily temperature, 
min daily temperature, wind speed, precipitation sum, and forecast/measured values label for the wanted time period. 
It can forecast up to 16 days in front and keeps the measured data for approx. 106 days.
Developed REST service with the endpoint /weather/?place=place_name that returns differences between measured and 
forecast values for dates that have both.

Usage:

in Windows: export environment variable PROJECT_DIRECTORY=path/to/downloaded/folder/open_meteo_API

in cmd:

cd path/to/downloaded/folder/open_meteo_API

run_test_windows.bat - for Windows OS

run_test_windows.sh - for Linux OS

This script will create a virtual environment, activate it and install requirements, then run the tests.

For retrieving weather data and storing it locally, in activated venv:

cd path/to/downloaded/folder/open_meteo_API

python manage.py forecast place_name start_date end_date

date format YYYY-MM-DD place_name with 2+ words separated by hyphens (Novi-Sad)

For hitting the endpoint that returns differences between measured and forecast values for dates that have both:

after running the server, hit the endpoint /weather/?place=place_name_you_want 
places with 2+ words separated by hyphens (Novi-Sad)
