import concurrent
import time
from django.http import HttpResponse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly
import secrets


class ResultAPI(APIView):

    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, format=None):
        return Response(status=status.HTTP_200_OK)

    def post(self, request, format=None):
        condition = secrets.choice([True, False])

        if condition:
            data = {"result": "Прогноз: 1"}
        else:
            data = {"result": "Прогноз: 2"}

        return Response(data=data, status=status.HTTP_200_OK)


def post_test(requests):
    def send_request(url):
        response = requests.post(url, data={"name": "Test", "age": 69})
        if response.status_code == 200:
            return True
        else:
            return False

    url = "http://127.0.0.1:8000/api/"
    concurrency = 700
    total_requests = 700

    start_time = time.time()

    # Send concurrent requests
    with concurrent.futures.ThreadPoolExecutor(max_workers=concurrency) as executor:
        # Create a list of URL copies to send multiple requests concurrently
        urls = [url] * total_requests

        # Submit requests to the executor
        results = executor.map(send_request, urls)

    # Count successful requests
    successful_requests = sum(results)
    failed = 0
    for result in results:
        if result.status_code != 200:
            failed += 1
    return HttpResponse(
        f"Successful requests: {successful_requests}/{total_requests} in {time.time() - start_time}\nfailed: {failed}")
