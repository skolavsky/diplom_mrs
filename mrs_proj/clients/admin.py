# clients.admin.py
from datetime import datetime

from .ClientDataDownloader import ClientDataDownloader
from .models import PersonalInfo, ClientData
from django.contrib import admin
from clients.models import ClientData
from .management.commands.populate_data import Command as PopulateDataCommand
from django.http import HttpResponse, HttpResponseRedirect


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
    file_name = f'{datetime.now().strftime("%Y%m%d-%H%M")}-data'

    list_display = ['personal_info', 'age', 'admission_date', 'result']
    actions = ['download_excel', 'download_csv', 'download_json', 'download_xml']

    def saver_from_id(self, queryset):
        personal_info_ids = [str(obj.personal_info.id) for obj in queryset]
        return ClientDataDownloader(personal_info_ids)

    def download_excel(self, request, queryset):
        downloader = self.saver_from_id(queryset)
        buffer = downloader.generate_excel()
        return self._download_response(buffer, f'{self.file_name}.xlsx',
                                       'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

    def download_csv(self, request, queryset):
        downloader = self.saver_from_id(queryset)
        buffer = downloader.generate_csv()
        return self._download_response(buffer, f'{self.file_name}.csv', 'text/csv')

    def download_json(self, request, queryset):
        downloader = self.saver_from_id(queryset)
        buffer = downloader.generate_json()
        return self._download_response(buffer, f'{self.file_name}.json', 'application/json')

    def download_xml(self, request, queryset):
        downloader = self.saver_from_id(queryset)
        buffer = downloader.generate_xml()
        return self._download_response(buffer, f'{self.file_name}.xml', 'application/xml')

    def _download_response(self, buffer, filename, content_type):
        response = HttpResponse(buffer.getvalue(), content_type=content_type)
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        return response

    download_excel.short_description = "Download selected as Excel"
    download_csv.short_description = "Download selected as CSV"
    download_json.short_description = "Download selected as JSON"
    download_xml.short_description = "Download selected as XML"
