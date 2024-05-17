# web_handler.admin.py
from django.contrib import admin
from .models import Article
from unfold.admin import ModelAdmin


class ArticleAdmin(ModelAdmin):
    list_display = ['title', 'author', 'created_at', 'last_modified_at']
    list_filter = ['created_at', 'last_modified_at', 'author']
    search_fields = ['title', 'content']


admin.site.register(Article, ArticleAdmin)
