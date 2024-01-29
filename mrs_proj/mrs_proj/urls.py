# project/urls.py
from django.contrib import admin
from django.urls import path, include
from web_handler.views import HomeView, DashboardView, ContactsView, LoginView, ContactsView
from django.contrib.auth.views import LogoutView
from clients.views import ClientListView, ClientDetailView

urlpatterns = [
    path('admin/', admin.site.urls),
    path("contacts/", ContactsView.as_view(), name='contacts'),
    path("login/", LoginView.as_view(), name='login'),
    path('', HomeView.as_view(), name='home'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('load_articles/', DashboardView.as_view(), name='load_articles'), # ajax for dashboard path

    path('logout/', LogoutView.as_view(next_page='home'), name='logout'),
    path('client-detail/<str:id>/', ClientDetailView.as_view(), name='client_detail'),

    path('client-list/', ClientListView.as_view(), name='client_list'),

    #API's pathes
    path('api/', include('clients.AI.urls')),
]
