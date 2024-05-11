from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordChangeView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import View

from .forms import UserEditForm, ProfileEditForm


class CustomPasswordChangeView(PasswordChangeView, LoginRequiredMixin):
    template_name = 'account/password_change_form.html'  # Указываете путь к вашему шаблону
    success_url = reverse_lazy('account:account_edit')  # Указываете URL, на который будет перенаправлен пользователь после успешного изменения пароля


class EditProfileView(LoginRequiredMixin, View):
    login_url = '/login/'  # URL для перенаправления, если пользователь не аутентифицирован

    def get(self, request):
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
        return render(request, 'account/edit.html', {'user_form': user_form, 'profile_form': profile_form})

    def post(self, request):
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile, data=request.POST, files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Profile updated successfully')
            return redirect('account:edit')  # Перенаправление на эту же страницу после успешного обновления профиля
        else:
            messages.error(request, 'Error updating your profile')
            return render(request, 'account/edit.html', {'user_form': user_form, 'profile_form': profile_form})

