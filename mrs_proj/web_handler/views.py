from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.http import HttpResponse, HttpResponseBadRequest
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View


class HomeView(LoginRequiredMixin, View):
    login_url = '/login/'

    def get(self, request):
        return render(request, 'home.html')


# @login_required
# def home(request):
#     return render(request, 'home.html')


class DashboardView(LoginRequiredMixin, View):
    login_url = '/login/'

    def get(self, request):
        return render(request, 'dashboard.html')


# @login_required
# def dashboard(request):
#     return render(request, "dashboard.html")

class ContactsView(LoginRequiredMixin, View):
    login_url = '/login/'

    def get(self, request):
        return render(request, 'contacts.html')


# @login_required
# def contacts(request):
#     return render(request, "contacts.html")

class LoginView(LoginRequiredMixin, View):
    login_url = '/login/'

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
                return render(request, 'login.html', {'error': 'Invalid login credentials'})
        else:
            return HttpResponse(status=400)

# def custom_login(request):
#     if request.method == 'POST':
#         username = request.POST.get('username', '')
#         password = request.POST.get('password', '')
#
#         # Use Django's built-in authenticate function to check credentials
#         user = authenticate(request, username=username, password=password)
#
#         if user is not None:
#             # Authentication successful, log in the user
#             login(request, user)
#             return redirect('home')  # Redirect to the home page
#         else:
#             # Authentication failed
#             return render(request, 'login.html', {'error': 'Invalid login credentials'})
#
#     return render(request, 'login.html')
