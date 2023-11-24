# clients/views.py
from django.shortcuts import render, redirect
from .models import Client
from .forms import ClientForm  # Import the form you need to create for adding clients

def client_list(request):
    # Handle GET request to display the list of clients
    clients = Client.objects.all()

    # Handle POST request to add a new client
    if request.method == 'POST':
        form = ClientForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('client_list')  # Redirect to the client list after adding a new client
    else:
        form = ClientForm()

    return render(request, 'client_list.html', {'clients': clients, 'form': form})
