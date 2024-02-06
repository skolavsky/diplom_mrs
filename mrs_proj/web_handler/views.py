from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.http import HttpResponse, HttpResponseBadRequest
from django.views import View
from datetime import timedelta
from django.utils import timezone
from clients.models import ClientData
from .models import Article
from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q

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

        context = {
            'no_results_clients': no_results_clients,
            'more_than_five': more_than_five,
        }

        return render(request, 'home.html', context)


class DashboardView(LoginRequiredMixin, View):
    login_url = LOGIN_URL

    def get(self, request):
        articles = Article.objects.all()
        return render(request, 'dashboard.html', {'articles': articles})

    def load_articles(self, request):
        offset = int(request.GET.get('offset', 0))
        articles = Article.objects.all()[offset:offset + 10]
        data = {'articles': []}
        for article in articles:
            data['articles'].append({
                'id': str(article.id),
                'author': article.author.username,
                'title': article.title,
                'content': article.content,
                'created_at': article.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                'last_modified_at': article.last_modified_at.strftime('%Y-%m-%d %H:%M:%S'),
                'note_id': str(article.note_id),
            })
        return JsonResponse(data)

    def dispatch(self, *args, **kwargs):
        if self.request.headers.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
            return self.load_articles(self.request)
        return super().dispatch(*args, **kwargs)


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
                return redirect('home')  # Redirect to the home page
            else:
                # Authentication failed
                return render(request, 'login.html', {'error': 'Неправильные логин или пароль.'})
        else:
            return HttpResponse(status=400)
