# project/urls.py
from django.contrib import admin
from django.urls import path
from web_handler.views import HomeView, DashboardView, ContactsView, LoginView
from clients.views import Client_list_view, Client_detail_view  # Import the view from the clients app

urlpatterns = [
    path('admin/', admin.site.urls),
    path("contacts/", ContactsView.as_view()),
    path("login/", LoginView.as_view(), name='login'),
    path('', HomeView.as_view(), name='home'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('client-detail/<str:token>/', Client_detail_view.as_view(), name='client_detail_by_token'),

    # Include the 'clients' app view
    path('client-list/', Client_list_view.as_view(), name='client_list'),
]
