# web_handler.admin.py
from django.contrib import admin
from .models import Article, Profile


class ArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'created_at', 'last_modified_at']
    list_filter = ['created_at', 'last_modified_at', 'author']
    search_fields = ['title', 'content']


admin.site.register(Article, ArticleAdmin)


class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'bio', 'telegram_id', 'is_white_list', 'location', 'birth_date', 'avatar']
    # Добавьте любые другие поля, которые вы хотите видеть в админке


admin.site.register(Profile, ProfileAdmin)
