from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordChangeView
from django.shortcuts import redirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import View
from django_ratelimit.decorators import ratelimit

from .forms import UserEditForm, ProfileEditForm


class CustomPasswordChangeView(PasswordChangeView, LoginRequiredMixin):
    template_name = 'account/password_change_form.html'  # Указываете путь к вашему шаблону
    success_url = reverse_lazy(
        'account-edit')  # Указываете URL, на который будет перенаправлен пользователь после успешного изменения пароля


class EditProfileView(LoginRequiredMixin, View):
    login_url = '/login/'  # URL для перенаправления, если пользователь не аутентифицирован

    @method_decorator(ratelimit(key='ip', rate='30/m', method='GET', block=True))
    def get(self, request):
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
        return render(request, 'account/edit.html', {'user_form': user_form, 'profile_form': profile_form})

    @method_decorator(ratelimit(key='ip', rate='30/m', method='POST', block=True))
    def post(self, request):
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile, data=request.POST, files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Профиль успешно обновлён')
            return redirect('account_edit')  # Перенаправление на эту же страницу после успешного обновления профиля
        else:
            messages.error(request, 'Ошибка при обновлении профиля')
            return render(request, 'account/edit.html', {'user_form': user_form, 'profile_form': profile_form})
