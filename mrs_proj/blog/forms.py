from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django import forms

from .models import Post


class SearchForm(forms.Form):
    query = forms.CharField()


class PostAdminForm(forms.ModelForm):
    body = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model = Post
        fields = '__all__'
