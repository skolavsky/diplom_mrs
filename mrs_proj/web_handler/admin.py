# web_handler.admin.py
from django.contrib import admin
from .models import Article
from .models import Profile


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'telegram_id', 'is_white_list')  # Определите поля для отображения в списке объектов


admin.site.register(Profile, ProfileAdmin)


class ArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'created_at', 'last_modified_at']
    list_filter = ['created_at', 'last_modified_at', 'author']
    search_fields = ['title', 'content']


admin.site.register(Article, ArticleAdmin)
