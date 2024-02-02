from rest_framework.test import APITestCase, APIClient, force_authenticate
from rest_framework import status
from django.urls import reverse
from django.contrib.auth.models import User
import json

API_URL = reverse('result')


class ResultAPITest(APITestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        user = User.objects.create_user(username='testuser', password='testpass')
        self.client.force_authenticate(user=user)

    def test_get(self):
        response = self.client.get(API_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post(self):
        response = self.client.post(API_URL)
        self.assertIn(
            response.status_code,
            [status.HTTP_200_OK,
             status.HTTP_403_FORBIDDEN,
             status.HTTP_401_UNAUTHORIZED]
             )
        result = json.loads(response.content).get('result')
        self.assertIn(result, ["Прогноз: 1", "Прогноз: 2"])
