# project/urls.py
from django.contrib import admin
from django.urls import path
from web_handler.views import HomeView, DashboardView, ContactsView, LoginView, ContactsView
from clients.views import ClientListView, ClientDetailView  # Import the view from the clients app

urlpatterns = [
    path('admin/', admin.site.urls),
    path("contacts/", ContactsView.as_view(), name='contacts'),
    path("login/", LoginView.as_view(), name='login'),
    path('', HomeView.as_view(), name='home'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('client-detail/<str:token>/', ClientDetailView.as_view(), name='client_detail'),

    # Include the 'clients' app view
    path('client-list/', ClientListView.as_view(), name='client_list'),
]
