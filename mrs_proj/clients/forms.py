from django import forms
from .models import Client


class ClientForm(forms.ModelForm):
    class Meta:
        model = Client

        fields = ['first_name', 'last_name', 'patronymic', 'gender', 'age', 'admission_date', 'spo2', 'body_mass_index',
                  'result', 'f_test_ex', 'f_test_in', 'comorb_ccc', 'comorb_bl', 'cd_ozhir', 'comorb_all', 'l_109',
                  'lf', 'rox', 'spo2_fio', 'ch_d']

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
            'ch_d': 'Частота дыхания',
            'cd_ozhir': 'Сахарный диабет или ожирение'
            # Add labels for other fields
        }

        widgets = {
            'first_name': forms.TextInput(attrs={'style': 'width: 80%;'}),
            'admission_date': forms.SelectDateWidget(),
            # Add widgets for other fields
        }

    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')

        max_length = 100
        if first_name and len(first_name) > max_length:
            raise forms.ValidationError(f"Длина имени не должна превышать {max_length} символов.")

        return first_name

    def clean_age(self):
        age = self.cleaned_data.get('age')

        if age and age < 0:
            raise forms.ValidationError("Возраст не может быть отрицательным числом.")

        return age

    def clean_body_mass_index(self):
        body_mass_index = self.cleaned_data.get('body_mass_index')

        if body_mass_index and body_mass_index < 0:
            raise forms.ValidationError("ИМТ не может быть отрицательным числом.")

        return body_mass_index

    def clean_spo2(self):
        spo2 = self.cleaned_data.get('spo2')

        if spo2 is not None and (spo2 < 0 or spo2 > 100):
            raise forms.ValidationError("SPO2 должен быть в пределах от 0 до 100.")

        return spo2

    def clean_lf(self):
        lf = self.cleaned_data.get('lf')

        if lf is not None and lf < 0:
            raise forms.ValidationError("lf не может быть отрицательным числом.")

        return lf
