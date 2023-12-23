# project/urls.py
from django.contrib import admin
from django.urls import path
from web_handler.views import HomeView, DashboardView, ContactsView, LoginView, ContactsView
from clients.views import ClientListView, ClientDetailView  # Import the view from the clients app
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('admin/', admin.site.urls),
    path("contacts/", ContactsView.as_view(), name='contacts'),
    path("login/", LoginView.as_view(), name='login'),
    path('', HomeView.as_view(), name='home'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('client-detail/<str:id_token>/', ClientDetailView.as_view(), name='client_detail'),
    path('logout/', LogoutView.as_view(next_page='home'), name='logout'),

    # Include the 'clients' app view
    path('client-list/', ClientListView.as_view(), name='client_list'),
]