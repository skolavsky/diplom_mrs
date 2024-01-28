# project/urls.py
from django.urls import path
from clients.AI.views import ResultAPI
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    #APIs
    path('result', ResultAPI.as_view(), name='result'),
]

urlpatterns = format_suffix_patterns(urlpatterns)