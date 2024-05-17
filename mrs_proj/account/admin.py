from django.contrib import admin
from .models import Profile
from unfold.admin import ModelAdmin


@admin.register(Profile)
class ProfileAdmin(ModelAdmin):
    list_display = ['user', 'date_of_birth', 'photo']
    raw_id_fields = ['user']