from django.contrib import admin
from clients.models import Client
from .management.commands.populate_data import Command as PopulateDataCommand


class ClientAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'patronymic', 'age', 'gender', 'admission_date')
    search_fields = ('first_name', 'last_name', 'patronymic')
    list_filter = ('gender', 'admission_date', 'spo2')

    actions = ['generate_test_data']

    def generate_test_data(self, request, oper_data):
        count = len(oper_data)
        populate_command = PopulateDataCommand()
        populate_command.handle(count=count)
        self.message_user(request, f'Successfully populated the database with {count} Client test data.')

    generate_test_data.short_description = 'Generate Test Data'


admin.site.register(Client, ClientAdmin)
