from rest_framework.views import APIView, Response, status
from .models import WeatherData
from .serializers import WeatherDataDiffSerializer, UserParameterSerializer
from .app_utils import get_measured_and_forecast_on_same_date, calculate_weather_data_diff
# Create your views here.


class WeatherDataDiffView(APIView):
    """
    APIView that returns the difference between the latest forecast and latest measured weather data
    for a specific city.

    The endpoint takes a 'place' query parameter as input. UserParameterSerializer validates the query parameter.

    """
    def get(self, request):
        city_name = request.query_params.get('place', '')
        parameter_serializer = UserParameterSerializer(data={'city_name': city_name})
        if parameter_serializer.is_valid():
            city_name = city_name.replace('-', ' ')
        else:
            return Response(parameter_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        measured_and_forecast_on_dates = get_measured_and_forecast_on_same_date(
                                                        WeatherData, city_name)

        weather_data_diff = calculate_weather_data_diff(measured_and_forecast_on_dates)
        serializer = WeatherDataDiffSerializer(weather_data_diff.values(), many=True)
        return Response(serializer.data) 