from django.urls import path
from .views import ClientListView, ClientDetailView, ClientStatsView

app_name = 'clients'

urlpatterns = [
    # Post views
    path('clients-list', ClientListView.as_view(), name='client_list'),
    path('clients-stat', ClientStatsView.as_view(), name='client_stats'),
    path('client-detail/<str:id>/', ClientDetailView.as_view(), name='client_detail'),
]
