from django.contrib import admin
from .models import Client


class ClientAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'patronymic', 'age', 'gender', 'admission_date')
    search_fields = ('first_name', 'last_name', 'patronymic')
    list_filter = ('gender', 'admission_date')


admin.site.register(Client, ClientAdmin)
