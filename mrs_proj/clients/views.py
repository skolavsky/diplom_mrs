# clients/views.py
from django.shortcuts import render, redirect, get_object_or_404
from .models import Client
from .forms import ClientForm
import secrets
from django.views import View
from django.http import HttpResponse, HttpResponseBadRequest
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse


class ClientListView(LoginRequiredMixin, View):
    login_url = '/login/'

    def get(self, request):
        clients = Client.objects.all()
        form = ClientForm()
        context = {'clients': clients, 'form': form}
        return render(request, 'client_list.html', context)

    def post(self, request):
        action = request.POST.get('action', '')
        print(request.POST)

        if action == 'save':
            form = ClientForm(request.POST)
            if form.is_valid():
                # Create a new Client instance with the form data
                new_client = form.save(commit=False)

                # Set added_user to the currently logged-in user
                new_client.added_user = self.request.user  # Use self.request.user

                # Set token to a new random value
                new_client.token = secrets.token_urlsafe(32)

                # Save the new client to the database
                new_client.save()
                # Redirect to the client list page
                return redirect('client_list')
        else:
            HttpResponse(status=408)

        return HttpResponse(status=400)


class ClientDetailView(LoginRequiredMixin, View):
    login_url = '/login/'

    def get(self, request, token):
        client = get_object_or_404(Client, token=token)
        form = ClientForm(instance=client)
        context = {'client': client, 'form': form}
        return render(request, 'client_detail.html', context)

    def post(self, request, token):
        action = request.POST.get('action', '')

        print(request.POST)

        if action == 'delete_client':
            client = get_object_or_404(Client, token=token)
            # Delete the client and redirect to the client list
            client.delete()
            return redirect('client_list')
        elif action == 'edit_client':
            client = get_object_or_404(Client, token=token)
            form = ClientForm(request.POST, instance=client)  # Use ClientForm for editing
            if form.is_valid():
                form.save()
                return redirect('client_detail', token=token)
            else:
                return HttpResponseBadRequest("Invalid form submission")
        else:
            return HttpResponseBadRequest("Invalid action")

        return HttpResponse(status=400)
