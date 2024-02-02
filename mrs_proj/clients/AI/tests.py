from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
import json

API_URL = reverse('result')


class ResultAPITest(APITestCase):
    def test_get(self):
        response = self.client.get(API_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post(self):
        response = self.client.post(API_URL)
        self.assertIn(response.status_code, [status.HTTP_200_OK, status.HTTP_403_FORBIDDEN, status.HTTP_401_UNAUTHORIZED])
        result = json.loads(response.content)['result']
        self.assertIn(result, ["Прогноз: 1", "Прогноз: 2"])
