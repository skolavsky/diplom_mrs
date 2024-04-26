from django.urls import path

from .views import ClientListView, ClientDetailView

app_name = 'clients'

urlpatterns = [
    # Post views
    path('clients-list', ClientListView.as_view(), name='client_list'),

    path('client-detail/<str:id>/', ClientDetailView.as_view(), name='client_detail'),

]
