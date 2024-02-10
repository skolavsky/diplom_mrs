# clients.admin.py
from .models import PersonalInfo, ClientData
from django.contrib import admin
from clients.models import ClientData
from .management.commands.populate_data import Command as PopulateDataCommand
from django.core.management import call_command
from io import BytesIO, StringIO
from django.http import HttpResponse, HttpResponseRedirect
from .management.commands.download_client_data import Command as DownloadClientDataCommand
from django.utils.timezone import now
from django.urls import reverse


@admin.register(PersonalInfo)
class PersonalInfoAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'patronymic', 'gender', 'is_active', 'id', ]
    list_filter = ['gender', 'is_active']
    search_fields = ['first_name', 'last_name', 'patronymic', 'gender']
    actions = ['generate_test_data']

    def generate_test_data(self, request, oper_data):
        count = len(oper_data)
        populate_command = PopulateDataCommand()
        populate_command.handle(count=count)
        self.message_user(request, f'Successfully populated the database with {count} Client test data.')

    generate_test_data.short_description = 'Создать тестовых пользователей.'


@admin.register(ClientData)
class ClientDataAdmin(admin.ModelAdmin):
    list_display = ['personal_info', 'age', 'admission_date', 'result']
    actions = ['download_excel', 'download_csv', 'download_json', 'download_xml']

    def download_excel(self, request, queryset):
        return self._download_data(request, queryset, 'excel')

    def download_csv(self, request, queryset):
        return self._download_data(request, queryset, 'csv')

    def download_json(self, request, queryset):
        return self._download_data(request, queryset, 'json')

    def download_xml(self, request, queryset):
        return self._download_data(request, queryset, 'xml')

    def _download_data(self, request, queryset, format_type):
        file_path = f'data.{format_type}'
        # Получаем список UUID из поля id связанных объектов PersonalInfo
        personal_info_ids = [str(obj.personal_info.id) for obj in queryset]

        # Вызываем соответствующую команду для скачивания данных
        call_command('download_client_data', format_type, ' '.join(personal_info_ids))
        self.message_user(request, f'Successfully downloaded selected data as {format_type.upper()}.')

        with open(file_path, 'rb') as file:
            response = HttpResponse(file.read())
            response['Content-Disposition'] = f'attachment; filename="{format_type}data.json"'
            return response

    download_excel.short_description = "Download selected as Excel"
    download_csv.short_description = "Download selected as CSV"
    download_json.short_description = "Download selected as JSON"
    download_xml.short_description = "Download selected as XML"
