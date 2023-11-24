from django import forms
from .models import Client


class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        exclude = ['token']
        labels = {
            'first_name': 'Имя',
            'last_name': 'Фамилия',
            'gender': 'Пол',
            'age': 'Возраст',
            'patronymic': 'Отчество',
            'result': 'Исход',
            'admission_date': 'Дата поступления',
            'SPO': 'SPO2',
            'body_mass_index': 'ИМТ',
            # Add labels for other fields
        }

        widgets = {
            'first_name': forms.TextInput(attrs={'style': 'width: 80%;'}),
            # Add widgets for other fields
        }
