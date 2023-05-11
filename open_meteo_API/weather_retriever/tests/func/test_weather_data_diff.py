import pytest
from django.urls import reverse
from urllib.parse import urlencode
import json

@pytest.mark.django_db
def test_weather_data_diff_endpoint(client, create_weather_data):
    url = reverse('data_diff')
    query_params = {'place':'TestPlace'}
    url_with_query_params = f"{url}?{urlencode(query_params)}"
    response = client.get(url_with_query_params)
    content = response.content.decode('utf-8')
    data = json.loads(content)
    assert response.status_code == 200
    assert '2022-01-01' in data[0]['date']
    assert 'max_temp_diff' in data[0].keys()

def test_weather_data_diff_endpoint_invalid_request(client):
    url = reverse('data_diff')
    query_params = {'place':'TestPlace'}
    url_with_query_params = f"{url}?{urlencode(query_params)}"
    response = client.post(url_with_query_params)
    assert response.status_code == 405
 