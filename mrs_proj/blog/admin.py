from django_ckeditor_5.widgets import CKEditor5Widget
from django import forms
from django.contrib import admin
from unfold.admin import ModelAdmin

from .models import Post


class PostAdminForm(forms.ModelForm):
    body = forms.CharField(widget=CKEditor5Widget())

    class Meta:
        model = Post
        fields = '__all__'


@admin.register(Post)
class PostAdmin(ModelAdmin):
    form = PostAdminForm
    list_display = ['title', 'slug', 'author', 'publish', 'status']
    list_filter = ['status', 'created', 'publish', 'author']
    search_fields = ['title', 'body']
    prepopulated_fields = {'slug': ('title',)}
    autocomplete_fields = ['author']  # Добавление автокомплита для поля автор
    date_hierarchy = 'publish'
    ordering = ['status', 'publish']
