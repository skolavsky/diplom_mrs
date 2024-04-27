from django.urls import path

from .views import DashboardView, ContactsView, LoginView, HomeView

app_name = 'web_handler'

urlpatterns = [
    # Post views
    path("contacts/", ContactsView.as_view(), name='contacts'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('load_articles/', DashboardView.as_view(), name='load_articles'),  # ajax for dashboard path
    path("login/", LoginView.as_view(), name='login'),
    path('', HomeView.as_view(), name='home'),

]
