# clients.admin.py
from .models import PersonalInfo, ClientData
from django.contrib import admin
from clients.models import ClientData
from .management.commands.populate_data import Command as PopulateDataCommand
from django.core.management import call_command
from io import BytesIO, StringIO
from django.http import HttpResponse


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
    list_display = ['personal_info', 'age', 'body_mass_index', 'spo2', 'admission_date', 'result', 'dayshome', 'rox',
                    'f_test_ex', 'f_test_in', 'comorb_ccc', 'comorb_bl', 'cd_ozhir', 'ch_d', 'lf', 'l_109', 'spo2_fio',
                    'date_added', ]
    list_filter = ['admission_date', 'comorb_ccc', 'comorb_bl', 'cd_ozhir', 'date_added', ]
    search_fields = ['age', 'body_mass_index', 'spo2', 'result']
