from django import forms
from .models import Client


class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        exclude = ['token']
        labels = {
            'first_name': 'Имя',
            'last_name': 'Фамилия',
            'patronymic': 'Отчество',
            'gender': 'Пол',
            'age': 'Возраст',
            'admission_date': 'Дата поступления',
            'spo2': 'SPO2',
            'body_mass_index': 'ИМТ',
            'result': 'Исход',
            # Add labels for other fields
        }

        widgets = {
            'first_name': forms.TextInput(attrs={'style': 'width: 80%;'}),
            'admission_date': forms.SelectDateWidget(),
            # Add widgets for other fields
        }

    def clean_age(self):
        age = self.cleaned_data.get('age')

        if age and age < 0:
            raise forms.ValidationError("Age must be a non-negative number.")

        return age

    def clean_body_mass_index(self):
        body_mass_index = self.cleaned_data.get('body_mass_index')

        if body_mass_index and body_mass_index < 0:
            raise forms.ValidationError("Body Mass Index must be a non-negative number.")

        return body_mass_index

    def clean_spo2(self):
        spo2 = self.cleaned_data.get('spo2')

        if (spo2 and spo2 < 0) and spo2 <= 100:
            raise forms.ValidationError("spo2 must be a non-negative number and < 100.")

        return spo2

    def clean_lf(self):
        lf = self.cleaned_data.get('lf')

        if lf and lf < 0:
            raise forms.ValidationError("lf must be a non-negative number.")

        return lf