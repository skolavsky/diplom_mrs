from django.urls import path
from django.conf.urls.static import static
from django.conf import settings

from .views import ContactsView, LoginView, HomeView

app_name = 'web_handler'

urlpatterns = [
    # Post views
    path("contacts/", ContactsView.as_view(), name='contacts'),
    path("login/", LoginView.as_view(), name='login'),
    path('', HomeView.as_view(), name='home'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)