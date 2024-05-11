from django.urls import path

from .views import CustomPasswordChangeView, EditProfileView

app_name = 'account'

urlpatterns = [
    path('edit/', EditProfileView.as_view(), name='account_edit'),
    path('password-change/', CustomPasswordChangeView.as_view(), name='password_change'),
]
