from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from .views import ContactsView, LoginView, HomeView, generate_pdf, HelpView

app_name = 'web_handler'

urlpatterns = [
    # Post views
    path("contacts/", ContactsView.as_view(), name='contacts'),
    path("login/", LoginView.as_view(), name='login'),
    path('', HomeView.as_view(), name='home'),
    path('report/', generate_pdf, name='report'),
    path('help/', HelpView.as_view(), name='help'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
