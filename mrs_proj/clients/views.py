# views.py
import secrets

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from django.http import HttpResponseBadRequest, HttpResponse
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.decorators.http import require_POST, require_GET

from .forms import PersonalInfoForm, ClientDataForm
from .models import ClientData, PersonalInfo

LOGIN_URL = '/login/'


class ClientGraphDataView(View, LoginRequiredMixin):
    def get(self, request, id):
        client_data = get_object_or_404(ClientData, personal_info__id=id)
        history_entries = client_data.history.all()

        spo2_values = []
        change_dates = []

        previous_spo2_value = None

        for i in range(len(history_entries)):
            version = history_entries[i]

            spo2_value = getattr(version, 'spo2', None)
            if spo2_value is not None and spo2_value != previous_spo2_value:
                spo2_values.append(spo2_value)
                change_dates.append(version.history_date.strftime('%Y-%m-%d %H:%M:%S'))
                previous_spo2_value = spo2_value

        # Reverse the lists so that the latest data appears last
        spo2_values.reverse()
        change_dates.reverse()

        data = {
            'spo2_values': spo2_values,
            'change_dates': change_dates
        }

        return JsonResponse(data)


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
    table_template_name = 'client_table.html'

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

        next_order = 'desc' if order == 'asc' else 'asc'

        if order == 'asc':
            clients_data = clients_data.order_by(f'{sort_by}')
        else:
            clients_data = clients_data.order_by(f'-{sort_by}')

        forecast_threshold = request.GET.get('forecast_threshold')
        ready_in_week = ''
        # Фильтрация по порогу прогноза и result = 0
        if forecast_threshold:
            forecast_threshold = int(forecast_threshold)
            ready_in_week = clients_data.filter(result=0, forecast_for_week__gte=forecast_threshold).count()
            clients_data = clients_data.filter(result=0, forecast_for_week__gte=forecast_threshold)
            print(ready_in_week)

        if search_query:
            clients_data = clients_data.filter(
                Q(personal_info__first_name__icontains=search_query) |
                Q(personal_info__last_name__icontains=search_query) |
                Q(personal_info__patronymic__icontains=search_query)
            )

        paginator = Paginator(clients_data, clients_per_page)
        page_number = int(request.GET.get('page', 1))
        page = paginator.get_page(page_number)

        if 'table_only' in request.GET:
            # Если указан параметр 'table_only', возвращаем только HTML-таблицу
            return render(request, self.table_template_name, {'clients_data': page, 'ready_in_week': ready_in_week, })

        # В противном случае возвращаем полный HTML-шаблон страницы
        client_data_form = ClientDataForm()
        personal_info_form = PersonalInfoForm()

        context = {
            'clients_data': page,
            'sort_by': sort_by,
            'next_order': next_order,
            'search_query': search_query,
            'personal_info_form': personal_info_form,
            'client_data_form': client_data_form,
            'ready_in_week': ready_in_week,
        }

        return render(request, self.template_name, context)

    def post(self, request):
        action = request.POST.get('action', '')
        if action == 'save':

            personal_info_form = PersonalInfoForm(request.POST)
            client_data_form = ClientDataForm(request.POST)
            print(personal_info_form)
            print(client_data_form)

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

                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    messages.success(request, 'Запись успешно добавлена')
                    return JsonResponse({'message': 'ok'})

                # Для обычных запросов перенаправляем на список клиентов
                messages.success(request, 'Запись успешно добавлена')
                return redirect('clients:client_list')

            messages.error(request, 'Ошибка при добавлении записи')
            return redirect('clients:client_list')


class ClientDetailView(View, LoginRequiredMixin):
    template_name = 'client_detail.html'
    table_template_name = 'client_detail_history_table.html'

    def get(self, request, id):
        entries_per_page = 15

        client_data = get_object_or_404(ClientData, personal_info__id=id)
        history_entries = client_data.history.all()
        history_with_changes = []
        client_info = get_object_or_404(PersonalInfo, id=id)
        client_data_form = ClientDataForm(instance=client_data)
        personal_info_form = PersonalInfoForm(instance=client_info)

        fields = ['spo2', 'spo2_fio', 'rox', 'ch_d', 'oxygen_flow', 'ventilation_reserve', 'mvv', 'mv']

        spo2_values = []
        change_dates = []

        previous_spo2_value = None

        for i in range(len(history_entries)):
            version = history_entries[i]
            changes = {}
            has_changes = False
            if i > 0:  # Skip the first item
                prev_version = history_entries[i - 1]
                for field in fields:
                    if getattr(version, field) != getattr(prev_version, field):
                        changes[field] = True
                        has_changes = True
                    else:
                        changes[field] = False
            else:
                changes = {field: False for field in fields}

            if has_changes:  # Добавляем только если есть изменения
                history_with_changes.append({
                    'version': version,
                    'changes': changes
                })

            # Add spo2 value and change date to the lists if spo2 is not None and different from the previous value
            spo2_value = getattr(version, 'spo2', None)
            if spo2_value is not None and spo2_value != previous_spo2_value:
                spo2_values.append(spo2_value)
                change_dates.append(version.history_date.strftime('%Y-%m-%d %H:%M:%S'))
                previous_spo2_value = spo2_value

        # Reverse the lists so that the latest data appears last
        spo2_values.reverse()
        change_dates.reverse()

        # Пагинация после фильтрации
        paginator = Paginator(history_with_changes, entries_per_page)  # Показывать по 15 записей на странице

        page = request.GET.get('page')
        try:
            paginated_history_with_changes = paginator.page(page)
        except PageNotAnInteger:
            paginated_history_with_changes = paginator.page(1)
        except EmptyPage:
            paginated_history_with_changes = paginator.page(paginator.num_pages)

        if 'table_only' in request.GET:
            # Если указан параметр 'table_only', возвращаем только HTML-таблицу
            return render(request, self.table_template_name, {'history_with_changes': paginated_history_with_changes})

        context = {
            'form': client_data_form,
            'form_info': personal_info_form,
            'client_data': client_data,
            'history_with_changes': paginated_history_with_changes,
            'spo2_values': spo2_values,
            'change_dates': change_dates,
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


@login_required
@require_GET
def client_data(request, id):
    if request.user.is_authenticated:
        client_data = get_object_or_404(ClientData, personal_info__id=id)
        form = ClientDataForm(instance=client_data)
        context = {'client_data': client_data, 'form': form}
        print(context)
        return render(request, 'spoiler_form.html', context=context)
        # Генерируем случайное число от 1 до 20
    return JsonResponse({'status': 'error'})


@login_required
@require_POST
def client_data_update(request, id):
    action = request.POST.get('action', '')
    if request.user.is_authenticated:
        if action == 'update_client':
            client_data = get_object_or_404(ClientData, personal_info__id=id)
            form = ClientDataForm(request.POST, instance=client_data)
            if form.is_valid():
                form.save()
                messages.success(request, f'Запись успешно обновлена')
                return HttpResponse(status=204)
            else:
                return JsonResponse({'status': 'error_data'})
