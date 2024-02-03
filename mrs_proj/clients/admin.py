# clients.admin.py
from django.contrib import admin
from .models import PersonalInfo, ClientData


@admin.register(PersonalInfo)
class ClientDataAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'patronymic', 'gender', 'is_active', 'id', ]
    list_filter = ['gender', 'is_active']
    search_fields = ['first_name', 'last_name', 'patronymic', 'gender']


@admin.register(ClientData)
class PersonalInfoAdmin(admin.ModelAdmin):
    list_display = ['personal_info', 'age', 'body_mass_index', 'spo2', 'admission_date', 'result', 'dayshome', 'rox',
                    'f_test_ex', 'f_test_in', 'comorb_ccc', 'comorb_bl', 'cd_ozhir', 'ch_d', 'lf', 'l_109', 'spo2_fio',
                    'date_added', ]
    list_filter = ['admission_date', 'comorb_ccc', 'comorb_bl', 'cd_ozhir', 'date_added', ]
    search_fields = ['age', 'body_mass_index', 'spo2', 'result']
