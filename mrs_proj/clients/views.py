# clients/views.py
from django.shortcuts import render, redirect, get_object_or_404
from .models import Client
from .forms import ClientForm
import secrets
from django.views import View
from django.http import HttpResponse, HttpResponseBadRequest
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.db import models

LOGIN_URL = '/login/'


class ClientListView(LoginRequiredMixin, View):
    login_url = LOGIN_URL

    def get(self, request):
        clients_per_page = 10
        sort_by = request.GET.get('sort', 'last_name')
        order = request.GET.get('order', 'asc')
        form = ClientForm()

        search_query = request.GET.get('search', '')
        clients = Client.objects.all()

        if search_query:
            clients = clients.filter(
                models.Q(first_name__icontains=search_query) |
                models.Q(last_name__icontains=search_query) |
                models.Q(patronymic__icontains=search_query)
            )

        next_order = 'desc' if order == 'asc' else 'asc'

        if order == 'asc':
            clients = clients.order_by(sort_by)
        else:
            clients = clients.order_by(f'-{sort_by}')

        paginator = Paginator(clients, clients_per_page)
        page_number = request.GET.get('page')
        page = paginator.get_page(page_number)

        context = {
            'clients': page,
            'sort_by': sort_by,
            'next_order': next_order,
            'form': form,
            'search_query': search_query,
        }

        return render(request, 'client_list.html', context)

    def post(self, request):
        action = request.POST.get('action', '')

        if action == 'save':
            form = ClientForm(request.POST)
            if form.is_valid():
                # Create a new Client instance with the form data
                new_client = form.save(commit=False)

                # Set added_user to the currently logged-in user
                new_client.added_user = self.request.user  # Use self.request.user

                # Set token to a new random value
                new_client.id_token = secrets.token_urlsafe(32)

                # Save the new client to the database
                new_client.save()
                # Redirect to the client list page
                return redirect('client_list')

        return HttpResponse(status=400)


class ClientDetailView(LoginRequiredMixin, View):
    login_url = LOGIN_URL

    def get(self, request, id_token):
        client = get_object_or_404(Client, id_token=id_token)
        history_entries = client.history.all()
        print(history_entries)
        form = ClientForm(instance=client)
        context = {'client': client, 'history_entries': history_entries, 'form': form}
        return render(request, 'client_detail.html', context)

    def post(self, request, id_token):
        action = request.POST.get('action', '')

        if action == 'delete_client':
            client = get_object_or_404(Client, id_token=id_token)
            # Delete the client and redirect to the client list
            client.delete()
            return redirect('client_list')
        elif action == 'edit_client':
            client = get_object_or_404(Client, id_token=id_token)
            form = ClientForm(request.POST, instance=client)  # Use ClientForm for editing
            if form.is_valid():
                form.save()
                return redirect('client_detail', id_token=id_token)
            else:
                return HttpResponseBadRequest("Invalid form submission")
        else:
            return HttpResponseBadRequest("Invalid action")
