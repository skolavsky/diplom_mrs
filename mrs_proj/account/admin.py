from django.contrib import admin
from .models import Profile
from unfold.admin import ModelAdmin


@admin.register(Profile)
class ProfileAdmin(ModelAdmin):
    list_display = ['user', 'date_of_birth', 'photo']
    autocomplete_fields = ['user']  # Добавление автокомплита для поля user
