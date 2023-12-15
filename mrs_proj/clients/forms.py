from django import forms
from .models import Client
from django.utils import timezone
import re
from datetime import date

FIO_RE_VALIDATION = "^[A-Za-zА-Яа-яЁё' -]+$"
FIO_MAX_LENGTH = 100


class ClientForm(forms.ModelForm):
    class Meta:
        model = Client

        fields = ['first_name', 'last_name', 'patronymic', 'gender', 'age', 'admission_date', 'spo2', 'body_mass_index',
                  'result', 'f_test_ex', 'f_test_in', 'comorb_ccc', 'comorb_bl', 'cd_ozhir', 'comorb_all', 'l_109',
                  'lf', 'rox', 'spo2_fio', 'ch_d', 'dayshome']

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
            'cd_ozhir': 'Сахарный диабет или ожирение',
            'spo2_fio': 'Fraction of inspired oxygen',
            'rox': 'Rox-?',
            'lf': 'Lung function',
            'l_109': 'Level_109',
            'comorb_all': 'аллергии?',
            'comorb_ccc': 'comorb_ccc?',
            'f_test_in': 'внутренний',
            'f_test_ex': 'внешний',
            'comorb_bl': 'коморбидность',
            'dayshome': 'дней дома',
            # Add labels for other fields
        }

        widgets = {
            'first_name': forms.TextInput(attrs={'style': 'width: 80%;'}),
            'admission_date': forms.SelectDateWidget(),
            'comorb_ccc': forms.CheckboxInput(attrs={'class': 'checkbox-input'}),
        }

    def validate_type(self, value, expected_type, field_name):
        if value is not None and not isinstance(value, expected_type):
            raise forms.ValidationError(
                f"Значение {self.fields[field_name].label} должно быть {expected_type.__name__}.")

    def validate_length(self, value, max_length, field_name):
        if value is not None and len(str(value)) > max_length:
            raise forms.ValidationError(
                f"Длина значения {self.fields[field_name].label} не должна превышать {max_length} символов.")

    def validate_regex(self, value, regex, field_name):
        if value is not None and not re.match(regex, str(value)):
            raise forms.ValidationError(f"Значение {self.fields[field_name].label} содержит недопустимые символы.")

    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')

        self.validate_type(first_name, str, 'first_name')

        # Проверка на длину не более 100 символов
        self.validate_length(first_name, max_length=FIO_MAX_LENGTH, field_name='first_name')

        # Проверка на наличие цифр, знаков, кроме апострофа и дефиса
        self.validate_regex(first_name, FIO_RE_VALIDATION, field_name='first_name')

        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name')

        self.validate_type(last_name, str, 'last_name')

        # Проверка на длину не более 100 символов
        self.validate_length(last_name, max_length=FIO_MAX_LENGTH, field_name='last_name')

        # Проверка на наличие цифр, знаков, кроме апострофа и дефиса
        self.validate_regex(last_name, FIO_RE_VALIDATION, field_name='last_name')

        return last_name

    def clean_patronymic(self):
        patronymic = self.cleaned_data.get('patronymic')

        if patronymic is not None:
            self.validate_type(patronymic, str, 'patronymic')

            # Проверка на длину не более 100 символов
            self.validate_length(patronymic, max_length=FIO_MAX_LENGTH, field_name='patronymic')

            # Проверка на наличие цифр, знаков, кроме апострофа и дефиса
            self.validate_regex(patronymic, FIO_RE_VALIDATION, field_name='patronymic')

        return patronymic

    def clean_age(self):
        age = self.cleaned_data.get('age')

        if age is not None:

            # Проверка на соответствие типу
            self.validate_type(age, int, 'body_mass_index')

            # Проверка на кол-во и наличие
            if age < 0 or age > 120:
                raise forms.ValidationError(
                    f"Значение {self.fields['age'].label} должно быть в пределах от 0 до 120.")

        return age

    def clean_body_mass_index(self):
        body_mass_index = self.cleaned_data.get('body_mass_index')

        if body_mass_index is not None:

            # Проверка на соответствие типу
            self.validate_type(body_mass_index, float, 'body_mass_index')

            # Проверка на кол-во и наличие
            if body_mass_index < 0 or body_mass_index > 100.0:
                raise forms.ValidationError(
                    f"Значение {self.fields['body_mass_index'].label} должно быть в пределах от 0 до 100.0.")

                # Проверка на количество знаков после запятой (не более 3)
            if isinstance(body_mass_index, float):
                _, _, fraction = str(body_mass_index).partition('.')
                if len(fraction) > 3:
                    raise (forms.ValidationError
                           (f"{self.fields['body_mass_index'].label} не может иметь не более 3 знаков после запятой."))

        return body_mass_index

    def clean_spo2(self):
        spo2 = self.cleaned_data.get('spo2')

        if spo2 is not None:

            # Проверка на соответствие типу
            self.validate_type(spo2, int, 'spo2')

            # Проверка на кол-во и наличие
            if spo2 < 0 or spo2 > 100:
                raise forms.ValidationError(
                    f"Значение {self.fields['spo2'].label} должно быть в пределах от 0 до 100.")

        return spo2

    def clean_dayshome(self):
        dayshome = self.cleaned_data.get('dayshome')

        if dayshome is not None:

            # Проверка на соответствие типу
            self.validate_type(dayshome, int, 'dayshome')

            # Проверка на кол-во и наличие
            if dayshome < 0 or dayshome > 50:
                raise forms.ValidationError(
                    f"Значение {self.fields['dayshome'].label} должно быть в пределах от 0 до 50.")

        return dayshome

    def clean_lf(self):
        lf = self.cleaned_data.get('lf')

        if lf is not None:

            # Проверка на соответствие типу
            self.validate_type(lf, float, 'lf')

            # Проверка на кол-во и наличие
            if lf < 0 or lf > 50.0:
                raise forms.ValidationError(
                    f"Значение {self.fields['lf'].label} должно быть в пределах от 0 до 50.0.")

        return lf

    def clean_admission_date(self):
        admission_date = self.cleaned_data.get('admission_date')

        if admission_date is not None:

            # Проверка формата даты
            self.validate_type(admission_date, date, 'admission_date')

            # Проверка временного периода
            if admission_date > timezone.now().date() or admission_date.year < 2023:
                raise forms.ValidationError("Дата поступления должна быть не позднее сегодня и не ранее 2023 года.")

        return admission_date

    def clean_ch_d(self):
        ch_d = self.cleaned_data.get('ch_d')

        if ch_d is not None:

            # Проверка на соответствие типу
            self.validate_type(ch_d, int, 'ch_d')

            # Проверка на кол-во и наличие
            if ch_d < 0 or ch_d > 150:
                raise forms.ValidationError(
                    f"Значение {self.fields['ch_d'].label} должно быть в пределах от 0 до 200.")

        return ch_d

    def clean_f_test_ex(self):
        f_test_ex = self.cleaned_data.get('f_test_ex')

        if f_test_ex is not None:

            # Проверка на соответствие типу
            self.validate_type(f_test_ex, int, 'f_test_ex')

            # Проверка на кол-во и наличие
            if f_test_ex < 0 or f_test_ex > 200:
                raise forms.ValidationError(
                    f"Значение {self.fields['f_test_ex'].label} должно быть в пределах от 0 до 200.")

        return f_test_ex

    def clean_f_test_in(self):
        f_test_in = self.cleaned_data.get('f_test_in')

        if f_test_in is not None:

            # Проверка на соответствие типу
            self.validate_type(f_test_in, int, 'f_test_in')

            # Проверка на кол-во и наличие
            if f_test_in < 0 or f_test_in > 200:
                raise forms.ValidationError(
                    f"Значение {self.fields['f_test_in'].label} должно быть в пределах от 0 до 200.")

        return f_test_in

    def clean_l_109(self):
        l_109 = self.cleaned_data.get('l_109')

        if l_109 is not None:

            # Проверка на соответствие типу
            self.validate_type(l_109, float, 'l_109')

            # Проверка на кол-во и наличие
            if l_109 < 0 or l_109 > 50.0:
                raise forms.ValidationError(
                    f"Значение {self.fields['l_109'].label} должно быть в пределах от 0 до 50.0.")

        return l_109

    def clean_lf(self):
        lf = self.cleaned_data.get('lf')

        if lf is not None:

            # Проверка на соответствие типу
            self.validate_type(lf, int, 'lf')

            # Проверка на кол-во и наличие
            if lf < 0 or lf > 50:
                raise forms.ValidationError(
                    f"Значение {self.fields['lf'].label} должно быть в пределах от 0 до 50.")

        return lf

    def clean_rox(self):
        rox = self.cleaned_data.get('rox')

        if rox is not None:

            # Проверка на соответствие типу
            self.validate_type(rox, float, 'rox')

            # Проверка на кол-во и наличие
            if rox < 0 or rox > 50.0:
                raise forms.ValidationError(
                    f"Значение {self.fields['rox'].label} должно быть в пределах от 0 до 50.0")

        return rox

    def clean_spo2_fio(self):
        spo2_fio = self.cleaned_data.get('spo2_fio')

        if spo2_fio is not None:

            # Проверка на соответствие типу
            self.validate_type(spo2_fio, float, 'rox')

            # Проверка на кол-во и наличие
            if spo2_fio < 0 or spo2_fio > 600.0:
                raise forms.ValidationError(
                    f"Значение {self.fields['spo2_fio'].label} должно быть в пределах от 0 до 600.0")

        return spo2_fio
