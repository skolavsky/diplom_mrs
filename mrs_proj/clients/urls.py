from django.urls import path

from .views import ClientListView, ClientDetailView, ClientStatsView, client_noted, client_data, client_data_update

app_name = 'clients'

urlpatterns = [
    # Post views
    path('clients-list', ClientListView.as_view(), name='client_list'),
    path('clients-stat', ClientStatsView.as_view(), name='client_stats'),
    path('client-detail/<str:id>/', ClientDetailView.as_view(), name='client_detail'),
    path('client-data/<str:id>/', client_data, name='client_data'),
    path('client-data-update/<str:id>/', client_data_update, name='client_data_update'),
    path('note/', client_noted, name='note'),

]
