# clients/views.py
from django.shortcuts import render, redirect, get_object_or_404
from .models import Client
from .forms import ClientForm
from django.contrib.auth.decorators import login_required
import secrets


@login_required
def client_list(request):
    clients = Client.objects.all()

    if request.method == 'POST':
        form = ClientForm(request.POST)
        if form.is_valid():
            # Create a new Client instance with the form data
            new_client = form.save(commit=False)

            # Set added_user to the currently logged-in user
            new_client.added_user = request.user

            # Set token to a new random value
            new_client.token = secrets.token_urlsafe(32)

            # Save the new client to the database
            new_client.save()

            # Redirect to the client list page
            return redirect('client_list')
    else:
        form = ClientForm()

    context = {'clients': clients, 'form': form}
    return render(request, 'client_list.html', context)


@login_required
def client_detail_by_token(request, token):
    client = get_object_or_404(Client, token=token)
    return render(request, 'client_detail.html', {'client': client})
