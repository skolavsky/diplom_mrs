# views.py
import secrets

import requests
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from django.http import HttpResponseBadRequest
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views import View
from django.views.decorators.http import require_POST

from .AI.serializers import ClientSerializer
from .forms import PersonalInfoForm, ClientDataForm
from .models import ClientData, PersonalInfo

LOGIN_URL = '/login/'


class ClientStatsView(View):
    def post(self, request):
        # Проверяем, что метод запроса POST
        if request.method == 'POST':

            percent = request.GET.get('percent')

            if percent:
                # Если параметр percent был отправлен, рассчитываем количество готовых клиентов
                ready_in_week = ClientData.objects.filter(result=0, forecast_for_week__gte=percent).count()
                stats_data = {
                    'ready_in_week': ready_in_week,  # Пример данных статистики
                }
                return JsonResponse(stats_data)
            # Здесь логика для получения статистики клиентов
            # Возвращаем статистику в формате JSON
            total_clients = ClientData.objects.count()
            active_clients = ClientData.objects.filter(result=0).count()

            stats_data = {
                'total_clients': total_clients,  # Пример данных статистики
                'active_clients': active_clients,
            }
            return JsonResponse(stats_data)
        else:
            # Если запрос не POST, вернуть ошибку
            return JsonResponse({'error': 'Method not allowed'}, status=405)


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
        group_filter = [int(key.split('_')[1]) for key in request.GET.keys() if key.startswith('group_')]
        noted_filter = [int(key.split('_')[1]) for key in request.GET.keys() if key.startswith('noted_')]

        if result_filters:
            clients_data = clients_data.filter(result__in=result_filters)

        if group_filter:
            clients_data = clients_data.filter(group__in=group_filter)

        if noted_filter:
            # Проверяем, есть ли значение 1 в списке фильтров для отслеживаемых записей
            if 1 in noted_filter:
                clients_data = clients_data.filter(users_note=request.user)
            # Проверяем, есть ли значение 0 в списке фильтров для НЕ отслеживаемых записей
            elif 0 in noted_filter:
                clients_data = clients_data.exclude(users_note=request.user)
        else:
            # Если не переданы параметры фильтрации, используем исходные данные без фильтрации
            pass

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
        try:
            posts = paginator.page(page_number)
        except PageNotAnInteger:
            # Если page_number не целое число, то
            # выдать первую страницу
            posts = paginator.page(1)
        except EmptyPage:
            # Если page_number находится вне диапазона, то
            # выдать последнюю страницу
            posts = paginator.page(paginator.num_pages)
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
                messages.success(request, 'Запись успешно добавлена')
                return redirect('clients:client_list')

        messages.error(request, 'Ошибка при добавлении записи')
        return redirect('clients:client_list')


class ClientDetailView(View, LoginRequiredMixin):
    template_name = 'client_detail.html'

    def get(self, request, id):
        client_data = get_object_or_404(ClientData, personal_info__id=id)
        client_info = get_object_or_404(PersonalInfo, id=id)
        form = ClientDataForm(instance=client_data)
        form_info = PersonalInfoForm(instance=client_info)
        client_serializer = ClientSerializer(client_data)
        result_data = None
        try:
            response = requests.post(
                self.request.build_absolute_uri(reverse('result')),
                client_serializer.data,
                headers={
                    'X-CSRFToken': request.COOKIES.get('csrftoken', '')
                },
                cookies=request.COOKIES
            )
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
            messages.success(request, f'Запись {client}успешно удалена')
            return redirect('clients:client_list')

        elif action == 'edit_client_info':
            client_info = get_object_or_404(PersonalInfo, id=id)
            form = PersonalInfoForm(request.POST, instance=client_info)
            if form.is_valid():
                form.save()
                messages.success(request, f'Данные успешно изменены')
                return redirect('clients:client_detail', id=id)
            else:
                client_data = get_object_or_404(ClientData, personal_info__id=id)
                history_entries = client_data.history.all()
                context = {'client_data': client_data, 'history_entries': history_entries, 'form': form}
                messages.error(request, f'Ошибка при изменении записи')
                return render(request, self.template_name, context)

        elif action == 'edit_client':
            client_data = get_object_or_404(ClientData, personal_info__id=id)
            form = ClientDataForm(request.POST, instance=client_data)
            if form.is_valid():
                form.save()
                messages.success(request, f'Запись успешно изменена')
                return redirect('clients:client_detail', id=id)
            else:
                return HttpResponseBadRequest("Invalid form submission")
        else:
            return HttpResponseBadRequest("Invalid action")


@login_required
@require_POST
def client_noted(request):
    if request.user.is_authenticated:
        client_id = request.POST.get('id')
        action = request.POST.get('action')
        if client_id and action:
            try:
                client = ClientData.objects.get(id=client_id)
                if action == 'note':
                    if request.user in client.users_note.all():  # Проверка наличия пользователя в списке
                        client.users_note.remove(request.user)  # Удаление пользователя из списка
                    else:
                        client.users_note.add(request.user)  # Добавление пользователя в список
                    return JsonResponse({'status': 'ok'})
            except ClientData.DoesNotExist:
                pass
    return JsonResponse({'status': 'error'})
