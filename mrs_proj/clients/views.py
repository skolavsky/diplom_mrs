# views.py
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
import secrets
from .models import ClientData, PersonalInfo
from .forms import PersonalInfoForm, ClientDataForm
from django.http import HttpResponse, HttpResponseBadRequest
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from .AI.serializers import ClientSerializer
import requests

LOGIN_URL = '/login/'


class ClientListView(LoginRequiredMixin, View):
    login_url = LOGIN_URL
    template_name = 'client_list.html'

    def get(self, request):
        clients_per_page = 10
        sort_by = request.GET.get('sort', 'personal_info__last_name')
        order = request.GET.get('order', 'asc')

        search_query = request.GET.get('search', '')
        clients_data = ClientData.objects.select_related('personal_info')

        # Фильтрация по результату
        result_filters = [int(key.split('_')[1]) for key in request.GET.keys() if key.startswith('result_')]
        if result_filters:
            clients_data = clients_data.filter(result__in=result_filters)

        if search_query:
            clients_data = clients_data.filter(
                Q(personal_info__first_name__icontains=search_query) |
                Q(personal_info__last_name__icontains=search_query) |
                Q(personal_info__patronymic__icontains=search_query)
            )

        next_order = 'desc' if order == 'asc' else 'asc'

        if order == 'asc':
            clients_data = clients_data.order_by(f'{sort_by}')
        else:
            clients_data = clients_data.order_by(f'-{sort_by}')

        paginator = Paginator(clients_data, clients_per_page)
        page_number = int(request.GET.get('page', 1))
        page = paginator.get_page(page_number)

        client_data_form = ClientDataForm()
        personal_info_form = PersonalInfoForm()

        context = {
            'clients_data': page,
            'sort_by': sort_by,
            'next_order': next_order,
            'search_query': search_query,
            'personal_info_form': personal_info_form,
            'client_data_form': client_data_form,
        }

        return render(request, self.template_name, context)

    def post(self, request):
        action = request.POST.get('action', '')

        if action == 'save':
            personal_info_form = PersonalInfoForm(request.POST)
            client_data_form = ClientDataForm(request.POST)

            if personal_info_form.is_valid() and client_data_form.is_valid():
                # Создаем и сохраняем PersonalInfo
                new_personal_info = personal_info_form.save()

                # Создаем и сохраняем ClientData с привязкой к PersonalInfo
                new_client_data = client_data_form.save(commit=False)
                new_client_data.personal_info = new_personal_info
                new_client_data.save()

                # Обновляем поля в PersonalInfo и сохраняем его
                new_personal_info.added_user = self.request.user
                new_personal_info.id_token = secrets.token_urlsafe(32)
                new_personal_info.save()

                # Редиректим на страницу с клиентами
                return redirect('client_list')

        return HttpResponse(status=400)


class ClientDetailView(View):
    template_name = 'client_detail.html'

    def get(self, request, id):
        client_data = get_object_or_404(ClientData, personal_info__id=id)
        client_info = get_object_or_404(PersonalInfo, id=id)
        form = ClientDataForm(instance=client_data)
        form_info = PersonalInfoForm(instance=client_info)
        client_serializer = ClientSerializer(client_data)
        result_data = None
        try:
            response = requests.post("http://127.0.0.1:8000/api/result.json/", client_serializer.data)
            response.raise_for_status()  # Поднимает исключение при неудачном запросе (например, 4xx или 5xx)
            result_data = response.json().get('result', '')

            # Дальнейшая обработка успешного запроса
        except requests.RequestException as e:
            print(f"Request failed: {e}")

        context = {
            'client_data': client_data,
            'form': form,
            'form_info': form_info,
            'result': result_data,
            'history_entries': client_data.history.all(),
        }
        return render(request, self.template_name, context)

    def post(self, request, id):
        action = request.POST.get('action', '')

        if action == 'delete_client':
            client = get_object_or_404(PersonalInfo, id=id)
            client.delete()
            return redirect('client_list')

        elif action == 'edit_client_info':
            client_info = get_object_or_404(PersonalInfo, id=id)
            form = PersonalInfoForm(request.POST, instance=client_info)
            if form.is_valid():
                form.save()
                return redirect('client_detail', id=id)
            else:
                client_data = get_object_or_404(ClientData, personal_info__id=id)
                history_entries = client_data.history.all()
                context = {'client_data': client_data, 'history_entries': history_entries, 'form': form}
                return render(request, self.template_name, context)

        elif action == 'edit_client':
            client_data = get_object_or_404(ClientData, personal_info__id=id)
            form = ClientDataForm(request.POST, instance=client_data)
            if form.is_valid():
                form.save()
                return redirect('client_detail', id=id)
            else:
                return HttpResponseBadRequest("Invalid form submission")
        else:
            return HttpResponseBadRequest("Invalid action")