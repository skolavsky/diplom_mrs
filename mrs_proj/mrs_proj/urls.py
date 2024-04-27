# project/urls.py
from django.contrib import admin
from django.contrib.auth.views import LogoutView
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('logout/', LogoutView.as_view(next_page='web_handler:home'), name='logout'),
    path('clients/', include('clients.urls')),
    path('', include('web_handler.urls')),

    # API's pathes
    path('api/', include('clients.AI.urls')),
]
