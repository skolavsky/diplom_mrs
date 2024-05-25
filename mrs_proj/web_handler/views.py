from datetime import timedelta

from clients.models import PersonalInfo, ClientData
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import redirect
from django.shortcuts import render
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.http import require_GET
from django_ratelimit.decorators import ratelimit
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas

LOGIN_URL = '/login/'


def is_admin(user):
    return user.is_superuser


@require_GET
@user_passes_test(is_admin)
def generate_pdf(request):
    '''
    Скачать отчёт можно на /report/
    Скачать может только админ
    Содержимое отчёта можно отредактировать тут
    '''
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="report.pdf"'

    p = canvas.Canvas(response, pagesize=letter)
    width, height = letter
    y = height - inch

    p.setFont("Helvetica-Bold", 16)
    p.drawString(inch, y, "Statistics Report")
    y -= inch

    # Статистика по PersonalInfo
    total_personal_info = PersonalInfo.objects.count()
    p.setFont("Helvetica-Bold", 12)
    p.drawString(inch, y, f"Total Personal Info Records: {total_personal_info}")
    y -= 14

    # Статистика по ClientData
    total_client_data = ClientData.objects.count()
    p.drawString(inch, y, f"Total Client Data Records: {total_client_data}")
    y -= 14

    # Статистика по значениям result
    results = [0, 1, 2, 3]
    for result in results:
        count = ClientData.objects.filter(result=result).count()
        p.drawString(inch, y, f"Client Data with Result {result}: {count}")
        y -= 14

    # Статистика по пользователям
    total_users = User.objects.count()
    p.setFont("Helvetica-Bold", 12)
    p.drawString(inch, y, f"Total Users: {total_users}")
    y -= 14

    active_users = User.objects.filter(is_active=True).count()
    p.drawString(inch, y, f"Active Users: {active_users}")
    y -= 14

    # Дополнительная статистика по пользователям
    p.setFont("Helvetica-Bold", 16)
    p.drawString(inch, y, "User Activity Details")
    y -= inch

    users = User.objects.all()
    for user in users:
        p.setFont("Helvetica-Bold", 12)
        p.drawString(inch, y, f"Username: {user.username}")
        y -= 14
        p.setFont("Helvetica", 10)
        last_login = user.last_login.strftime('%Y-%m-%d %H:%M:%S') if user.last_login else "Never"
        p.drawString(inch, y, f"Last Login: {last_login}")
        y -= 14
        date_joined = user.date_joined.strftime('%Y-%m-%d %H:%M:%S')
        p.drawString(inch, y, f"Date Joined: {date_joined}")
        y -= 14
        y -= 10  # Дополнительный отступ между пользователями

        if y <= inch:
            p.showPage()
            p.setFont("Helvetica", 10)
            y = height - inch

    p.showPage()
    p.save()

    return response


class ContactsView(LoginRequiredMixin, View):
    login_url = LOGIN_URL

    @method_decorator(ratelimit(key='ip', rate='30/m', method='GET', block=True))
    def get(self, request):
        # Define your criteria (e.g., no results or no updates for 30 days)
        return render(request, 'contacts.html')


class HomeView(LoginRequiredMixin, View):
    login_url = LOGIN_URL

    @method_decorator(ratelimit(key='ip', rate='30/m', method='GET', block=True))
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

    @method_decorator(ratelimit(key='ip', rate='30/m', method='GET', block=True))
    def get(self, request):
        return render(request, 'contacts.html')


class LoginView(View):
    @method_decorator(ratelimit(key='ip', rate='30/m', method='GET', block=True))
    def get(self, request):
        return render(request, 'login.html')

    @method_decorator(ratelimit(key='ip', rate='30/m', method='POST', block=True))
    def post(self, request):
        action = request.POST.get('action', '')
        print(request.POST)

        if action == 'login':
            username = request.POST.get('username', '')
            password = request.POST.get('password', '')

            # Use Django's built-in authenticate function to check credentials
            user = authenticate(request, username=username, password=password)

            if user is not None:
                # Check if the password needs to be changed
                delta = timezone.now() - user.profile.password_changed_at
                delta_days = delta.days
                if delta_days > settings.MAX_USER_PASSWORD_AGE:
                    # Password expired, redirect to password change page
                    messages.warning(request, 'Ваш пароль истёк. Пожалуйста, измените его.')

                    return redirect('/account/password-reset/')
                elif delta_days < 3:
                    # Warn user that password will expire soon
                    messages.info(request,
                                  'Ваш пароль скоро истечёт. Вы можете изменить его самостоятельно в своём профиле.')

                # Authentication successful, log in the user
                login(request, user)
                return redirect('web_handler:home')  # Redirect to the home page
            else:
                # Authentication failed
                return render(request, 'login.html', {'error': 'Неправильные логин или пароль.'})
        else:
            return HttpResponse(status=400)
