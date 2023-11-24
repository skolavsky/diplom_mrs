from django.http import HttpResponse, HttpResponseNotFound, HttpResponseForbidden, HttpResponseBadRequest, JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login


@login_required
def home(request):
    return render(request, 'home.html')


@login_required
def dashboard(request):
    return render(request, "dashboard.html")


@login_required
def contacts(request):
    return render(request, "contacts.html")


def custom_login(request):
    if request.method == 'POST':
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

    return render(request, 'login.html')


@login_required
def index(request):
    if request.method == "POST":
        name = request.POST.get("name")
        age = request.POST.get("age")
        time = request.POST.get("time")
        password = request.POST.get("password")
        radio = request.POST.get("radio")
        print(radio)
        print(password)
        return HttpResponse(f"<h2>Привет, {name}, твой возраст: {age}, time: {time}</h2>")
    else:
        return render(request, "index.html")
