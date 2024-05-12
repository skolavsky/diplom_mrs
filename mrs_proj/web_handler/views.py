from datetime import timedelta

from clients.models import ClientData
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import redirect
from django.shortcuts import render
from django.utils import timezone
from django.views import View

LOGIN_URL = '/login/'


class ContactsView(LoginRequiredMixin, View):
    login_url = LOGIN_URL

    def get(self, request):
        # Define your criteria (e.g., no results or no updates for 30 days)
        return render(request, 'contacts.html')


class HomeView(LoginRequiredMixin, View):
    login_url = LOGIN_URL

    def get(self, request):
        # Определите ваши критерии (например, результат 0 и отсутствие обновлений в течение 3 дней)
        three_days_ago = timezone.now() - timedelta(days=3)
        no_results_clients = ClientData.objects.filter(result=0, admission_date__lt=three_days_ago)

        # Проверка на количество найденных записей
        more_than_five = no_results_clients.count() > 5

        # Если найдено более 5 записей, ограничить их до 5
        if more_than_five:
            no_results_clients = no_results_clients[:5]
            messages.info(request, 'Много записей без результатов')

        # Получаем отмеченные записи текущего пользователя
        noted_clients = ClientData.objects.filter(users_note=request.user)[:3]
        noted_clients_more = 'False'

        # Проверяем, есть ли у текущего пользователя отмеченные записи
        if noted_clients:
            # Отправляем сообщение, если у пользователя больше 3 отмеченных записей
            if noted_clients.count() > 3:
                noted_clients_more = 'True'
                messages.info(request, 'У вас больше трёх отмеченных записей')

        context = {
            'no_results_clients': no_results_clients,
            'more_than_five': more_than_five,
            'noted_clients': noted_clients,
            'noted_clients_more': noted_clients_more,
        }

        return render(request, 'home.html', context)


class ContactsView(LoginRequiredMixin, View):
    login_url = LOGIN_URL

    def get(self, request):
        return render(request, 'contacts.html')


class LoginView(View):

    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        action = request.POST.get('action', '')
        print(request.POST)

        if action == 'login':

            username = request.POST.get('username', '')
            password = request.POST.get('password', '')

            # Use Django's built-in authenticate function to check credentials
            user = authenticate(request, username=username, password=password)

            if user is not None:
                # Authentication successful, log in the user
                login(request, user)
                return redirect('web_handler:home')  # Redirect to the home page
            else:
                # Authentication failed
                return render(request, 'login.html', {'error': 'Неправильные логин или пароль.'})
        else:
            return HttpResponse(status=400)
