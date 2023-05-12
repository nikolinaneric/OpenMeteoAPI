call python -m venv venv
call %PROJECT_DIRECTORY%\venv\Scripts\activate.bat
call pip install -r requirements.txt
call python manage.py makemigrations
call python manage.py migrate
call pytest --ds=open_meteo_API.test_settings

