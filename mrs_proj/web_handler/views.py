from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.http import HttpResponse, HttpResponseBadRequest
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from clients.models import Client
from datetime import timedelta
from django.utils import timezone

LOGIN_URL = '/login/'


class ContactsView(LoginRequiredMixin, View):
    login_url = LOGIN_URL

    def get(self, request):
        # Define your criteria (e.g., no results or no updates for 30 days)
        return render(request, 'contacts.html')


class HomeView(LoginRequiredMixin, View):
    login_url = LOGIN_URL

    def get(self, request):
        # Define your criteria (e.g., no results or no updates for 30 days)
        no_results_patients = Client.objects.filter(result__isnull=True,
                                                    admission_date__lt=timezone.now() - timedelta(days=3))
        more_than_five = no_results_patients.count() > 5

        context = {
            'no_results_patients': no_results_patients,
            'more_than_five': more_than_five,

        }

        return render(request, 'home.html', context)


class DashboardView(LoginRequiredMixin, View):
    login_url = LOGIN_URL

    def get(self, request):
        return render(request, 'dashboard.html')


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
