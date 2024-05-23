from django_ckeditor_5.widgets import CKEditor5Widget
from django import forms

from .models import Post


class SearchForm(forms.Form):
    query = forms.CharField()


class PostAdminForm(forms.ModelForm):
    body = forms.CharField(widget=CKEditor5Widget())

    class Meta:
        model = Post
        fields = '__all__'
