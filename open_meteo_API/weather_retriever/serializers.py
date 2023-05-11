from rest_framework import serializers


class WeatherDataDiffSerializer(serializers.Serializer):
    date = serializers.DateField()
    max_temp_forecast = serializers.CharField()
    max_temp_measured = serializers.CharField()
    max_temp_diff = serializers.CharField()
    min_temp_forecast = serializers.CharField()
    min_temp_measured = serializers.CharField()
    min_temp_diff = serializers.CharField()
    max_wind_speed_forecast = serializers.CharField()
    max_wind_speed_measured = serializers.CharField()
    max_wind_speed_diff = serializers.CharField()
    precipitation_sum_forecast = serializers.CharField()
    precipitation_sum_measured = serializers.CharField()
    precipitation_sum_diff = serializers.CharField()

class UserParameterSerializer(serializers.Serializer):
    city_name = serializers.CharField()