from django.contrib.auth import views as auth_views
from django.urls import path

from .views import CustomPasswordChangeView, EditProfileView


urlpatterns = [
    path('account-edit/', EditProfileView.as_view(), name='account_edit'),
    path('password-change/', CustomPasswordChangeView.as_view(), name='password_change'),
    # reset password urls
    path('password-reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('password-reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(),
         name='password_reset_confirm'),
    path('password-reset/complete/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]
