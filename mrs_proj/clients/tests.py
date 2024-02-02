from django.contrib.auth.models import User
from django.test import TestCase, Client
from clients.models import PersonalInfo, ClientData
from clients.forms import PersonalInfoForm, ClientDataForm
from faker import Faker
from datetime import date
import secrets
import string
from django.conf import settings
from django.urls import reverse

LOGIN = '/login/'


class PersonalInfoFormTest(TestCase):
    """
        Класс для тестирования валидности формы PersonalInfoForm.

        Attributes:
            fake (Faker): Объект Faker для генерации случайных данных.

        Methods:
            setUp(self): Метод, вызываемый перед выполнением каждого тестового метода.
            test_valid_form(self): Метод тестирования валидности формы с корректными данными.
            test_invalid_form(self): Метод тестирования формы с некорректными данными.
            test_first_name_length: Метод тестирования корректности ввода по символам
    """
    fake = Faker('ru_RU')

    def setUp(self, num_samples: int = 2):
        # Генерация данных для каждого теста
        self.data_list = [self.generate_data() for _ in range(num_samples)]

    def generate_data(self, **kwargs):
        default_data = {
            'first_name': self.fake.first_name(),
            'last_name': self.fake.last_name(),
            'patronymic': self.fake.middle_name(),
            'gender': self.fake.random_element(elements=[True, False]),
            # Можно добавить и другие поля модели
        }
        default_data.update(kwargs)
        return default_data

    def generate_invalid_string(self, spec_numbers: int = 5):
        """
        :type spec_numbers: int
        """
        return ''.join(secrets.choice(string.punctuation + string.digits) for _ in range(spec_numbers))

    def test_first_name_max_length(self):
        """
        Тестирование корректности ввода длины имени в форме.

        Метод создает случайное имя, превышающее максимальную длину поля в форме,
        заполняет им форму ClientForm и проверяет, что форма считается невалидной.

        Asserts:
            assertFalse(bool): Подтверждает, что форма не прошла валидацию из-за превышения
            длины имени.
        """
        for data in self.data_list:
            data['first_name'] = str('a' * (settings.FIO_MAX_LENGTH + 1))
            print(data['first_name'])
            form = PersonalInfoForm(data)
            self.assertFalse(form.is_valid(), f'Form errors: {form.errors}')

    def test_last_name_max_length(self):
        """
        Тестирование корректности ввода длины имени в форме.

        Метод создает случайное имя, превышающее максимальную длину поля в форме,
        заполняет им форму ClientForm и проверяет, что форма считается невалидной.

        Asserts:
            assertFalse(bool): Подтверждает, что форма не прошла валидацию из-за превышения
            длины имени.
        """
        for data in self.data_list:
            data['last_name'] = str('a' * (settings.FIO_MAX_LENGTH + 1))
            form = PersonalInfoForm(data)
            self.assertFalse(form.is_valid(), f'Form errors: {form.errors}')

    def test_patronymic_max_length(self):
        """
        Тестирование корректности ввода длины имени в форме.

        Метод создает случайное имя, превышающее максимальную длину поля в форме,
        заполняет им форму ClientForm и проверяет, что форма считается невалидной.

        Asserts:
            assertFalse(bool): Подтверждает, что форма не прошла валидацию из-за превышения
            длины имени.
        """
        for data in self.data_list:
            data['patronymic'] = str('a' * (settings.FIO_MAX_LENGTH + 1))
            form = PersonalInfoForm(data)
            self.assertFalse(form.is_valid(), f'Form errors: {form.errors}')

    def test_invalid_string_first_name(self):
        for data in self.data_list:
            data['first_name'] = data['first_name'] + self.generate_invalid_string()
            form = PersonalInfoForm(data)
            self.assertFalse(form.is_valid(), f'Form errors: {form.errors}')

    def test_invalid_string_last_name(self):
        for data in self.data_list:
            data['last_name'] += self.generate_invalid_string()
            form = PersonalInfoForm(data)
            self.assertFalse(form.is_valid(), f'Form errors: {form.errors}')

    def test_invalid_string_patronymic(self):
        for data in self.data_list:
            data['patronymic'] = data['patronymic'] + self.generate_invalid_string()
            form = PersonalInfoForm(data)
            self.assertFalse(form.is_valid(), f'Form errors: {form.errors}')

    def test_first_name_is_string(self):
        """
        Тестирование, что first_name действительно строка.
        """
        for data in self.data_list:
            form = PersonalInfoForm(data)
            self.assertTrue(form.is_valid(), f'Form should be valid, but got errors: {form.errors}')
            self.assertIsInstance(data['first_name'], str, 'first_name is not a string')

    def test_last_name_is_string(self):
        """
        Тестирование, что last_name действительно строка.
        """
        for data in self.data_list:
            form = PersonalInfoForm(data)
            self.assertTrue(form.is_valid(), f'Form should be valid, but got errors: {form.errors}')
            self.assertIsInstance(data['last_name'], str, 'last_name is not a string')

    def test_gender_is_bool(self):
        """
        Тестирование, что patronymic действительно строка.
        """
        for data in self.data_list:
            form = PersonalInfoForm(data)
            self.assertTrue(form.is_valid(), f'Form should be valid, but got errors: {form.errors}')
            self.assertIsInstance(data['gender'], bool, 'gender is not a bool')

    def test_gender_wrong_type(self):
        """
        Тестирование, что форма не будет работать с неправильным типом gender.
        """
        for data in self.data_list:
            # Изменяем тип gender на некорректный
            data['gender'] = 1  # Пример другого типа
            form = PersonalInfoForm(data)
            self.assertFalse(form.is_valid(), f'Form should not be valid, but got errors: {form.errors}')

    def test_patronymic_is_string(self):
        """
        Тестирование, что patronymic действительно строка.
        """
        for data in self.data_list:
            form = PersonalInfoForm(data)
            self.assertTrue(form.is_valid(), f'Form should be valid, but got errors: {form.errors}')
            self.assertIsInstance(data['patronymic'], str, 'patronymic is not a string')

    def test_first_name_wrong_type(self):
        """
        Тестирование, что форма не будет работать с неправильным типом first_name.
        """
        for data in self.data_list:
            # Изменяем тип first_name на некорректный
            data['first_name'] = 123  # Пример другого типа
            form = PersonalInfoForm(data)
            self.assertFalse(form.is_valid(), f'Form should not be valid, but got errors: {form.errors}')

    def test_last_name_wrong_type(self):
        """
        Тестирование, что форма не будет работать с неправильным типом last_name.
        """
        for data in self.data_list:
            # Изменяем тип last_name на некорректный
            data['last_name'] = 123  # Пример другого типа
            form = PersonalInfoForm(data)
            self.assertFalse(form.is_valid(), f'Form should not be valid, but got errors: {form.errors}')

    def test_patronymic_wrong_type(self):
        """
        Тестирование, что форма не будет работать с неправильным типом patronymic.
        """
        for data in self.data_list:
            # Изменяем тип patronymic на некорректный
            data['patronymic'] = 123  # Пример другого типа
            form = PersonalInfoForm(data)
            self.assertFalse(form.is_valid(), f'Form should not be valid, but got errors: {form.errors}')


class ClientDataFormTest(TestCase):
    """
        Класс для тестирования валидности формы ClientDataForm.

        Attributes:
            fake (Faker): Объект Faker для генерации случайных данных.

        Methods:
            setUp(self): Метод, вызываемый перед выполнением каждого тестового метода.
            test_valid_form(self): Метод тестирования валидности формы с корректными данными.
            test_invalid_form(self): Метод тестирования формы с некорректными данными.
            test_first_name_length: Метод тестирования корректности ввода по символам
    """
    fake = Faker('ru_RU')

    def setUp(self, num_samples: int = 2):
        # Генерация данных для каждого теста
        self.data_list = [self.generate_data() for _ in range(num_samples)]

    def generate_data(self, **kwargs):
        default_data = {
            'age': self.fake.random_int(min=0, max=120),
            'result': self.fake.random_int(min=0, max=3),
            'admission_date': self.fake.date_between_dates(date(settings.START_ADMISSION_DATE, 1, 1), date.today()),
            'comorb_ccc': secrets.choice([True, False]),
            'comorb_bl': secrets.choice([True, False]),
            'cd_ozhir': secrets.choice([True, False]),
            'comorb_all': secrets.choice([True, False]),
            'body_mass_index': self.fake.pyfloat(min_value=0, max_value=100.0, right_digits=3),
            'spo2': self.fake.random_int(min=0, max=100),
            'spo2_fio': self.fake.pyfloat(min_value=0, max_value=600.0, right_digits=3),
            'ch_d': self.fake.random_int(min=0, max=150),
            'dayshome': self.fake.random_int(min=0, max=50),
            'lf': self.fake.pyfloat(min_value=0, max_value=50.0, right_digits=3),
            'f_test_ex': self.fake.random_int(min=0, max=200),
            'f_test_in': self.fake.random_int(min=0, max=200),
            'rox': self.fake.pyfloat(min_value=0, max_value=50.0, right_digits=3),
            'l_109': self.fake.pyfloat(min_value=0, max_value=50.0, right_digits=3),
            # Можно добавить и другие поля модели
        }
        default_data.update(kwargs)
        return default_data

    def test_valid_all_fields_form(self):
        """Тест валидности формы с корректными данными."""
        for data in self.data_list:
            form = ClientDataForm(data)
            self.assertTrue(form.is_valid(), f'Form errors: {form.errors}')

    def test_result_wrong_type(self):
        """
        Тестирование, что форма не будет работать с неправильным типом result.
        """
        for data in self.data_list:
            # Изменяем тип gender на некорректный
            data['result'] = 'variable'  # Пример другого типа
            form = PersonalInfoForm(data)
            self.assertFalse(form.is_valid(), f'Form should not be valid, but got errors: {form.errors}')

    def test_result_is_negative(self):
        """
        Тестирование, что форма не будет работать с отрицательными result.
        """
        for data in self.data_list:
            # Изменяем тип gender на некорректный
            data['result'] = self.fake.random_int(min=-100, max=-1)
            form = PersonalInfoForm(data)
            self.assertFalse(form.is_valid(), f'Form should not be valid, but got errors: {form.errors}')

    def test_result_is_unset_value(self):
        """
        Тестирование, что форма не будет работать с нерегламентированными results.
        """
        for data in self.data_list:
            # Изменяем тип gender на некорректный
            data['result'] = self.fake.random_int(min=4, max=100)
            form = PersonalInfoForm(data)
            self.assertFalse(form.is_valid(), f'Form should not be valid, but got errors: {form.errors}')

    def test_age_is_negative(self):
        """
        Тестирование валидации возраста.

        Метод создает случайный возраст, отрицательный, заполняет им форму ClientDataForm
        и проверяет, что форма считается невалидной.

        Asserts:
            assertFalse(bool): Подтверждает, что форма не прошла валидацию из-за
            отрицательного возраста.
        """
        for data in self.data_list:
            data['age'] = self.fake.random_int(min=-200, max=-1)
            form = ClientDataForm(data)
            self.assertFalse(form.is_valid(), f'Form errors: {form.errors}')

    def test_age_max(self):
        """
        Тестирование валидации возраста.

        Метод создает случайный возраст, отрицательный, заполняет им форму ClientDataForm
        и проверяет, что форма считается невалидной.

        Asserts:
            assertFalse(bool): Подтверждает, что форма не прошла валидацию из-за
            отрицательного возраста.
        """
        for data in self.data_list:
            data['age'] = self.fake.random_int(min=121, max=999),
            form = ClientDataForm(data)
            self.assertFalse(form.is_valid(), f'Form errors: {form.errors}')

    def test_age_is_int(self):
        """
        Тестирование, что age действительно int.
        """
        for data in self.data_list:
            form = ClientDataForm(data)
            self.assertTrue(form.is_valid(), f'Form should be valid, but got errors: {form.errors}')
            self.assertIsInstance(data['age'], int, 'age is not a int')

    def test_age_wrong_type(self):
        """
        Тестирование, что форма не будет работать с неправильным типом age.
        """
        for data in self.data_list:
            # Изменяем тип age на некорректный
            data['age'] = '123'  # Пример другого типа
            form = ClientDataForm(data)
            self.assertFalse(form.is_valid(), f'Form should not be valid, but got errors: {form.errors}')

    def test_admission_date_is_date(self):
        """
        Тестирование, что admission_date является типом дата.
        """
        for data in self.data_list:
            form = ClientDataForm(data)
            self.assertTrue(form.is_valid(), f'Form should be valid, but got errors: {form.errors}')
            self.assertIsInstance(data['admission_date'], date, 'admission_date is not a string')

    def test_admission_date_wrong_type(self):
        """
        Тестирование, что форма не будет работать с неправильным типом admission_date.
        """
        for data in self.data_list:
            # Изменяем тип admission_date на некорректный
            data['admission_date'] = 'string'  # Пример другого типа
            form = ClientDataForm(data)
            self.assertFalse(form.is_valid(), f'Form should not be valid, but got errors: {form.errors}')

    def test_admission_date_not_future(self):
        """
        Тестирование, что admission_date не дальше сегодняшнего дня.
        """
        for data in self.data_list:
            if 'admission_date' in data and isinstance(data['admission_date'], date):
                self.assertLessEqual(data['admission_date'], date.today(), 'admission_date should not be in the future')

    def test_admission_date_not_earlier_than_start_year(self):
        """
        Тестирование, что admission_date не раньше START_YEAR.
        """
        for data in self.data_list:
            if 'admission_date' in data and isinstance(data['admission_date'], date):
                self.assertGreaterEqual(data['admission_date'].year, settings.START_ADMISSION_DATE,
                                        f'admission_date should not be earlier than {settings.START_ADMISSION_DATE}')

    def test_body_mass_index_valid(self):
        """
        Тестирование валидации индекса массы тела.

        Метод создает случайные вес и рост, соответствующие правилам валидации,
        вычисляет индекс массы тела и заполняет им форму ClientForm.
        Проверяет, что форма считается валидной.

        Asserts:
            assertTrue(bool): Подтверждает, что форма прошла валидацию.
        """

        for data in self.data_list:
            data['body_mass_index'] = float(self.fake.random_int(min=0, max=99)),
            form = ClientDataForm(data)
            self.assertFalse(form.is_valid(), f'Form errors: {form.errors}')

    def test_body_mass_index_is_float(self):
        """
        Тестирование, что age действительно float.
        """
        for data in self.data_list:
            form = ClientDataForm(data)
            self.assertTrue(form.is_valid(), f'Form should be valid, but got errors: {form.errors}')
            self.assertIsInstance(data['body_mass_index'], float, 'age is not a float')

    def test_body_mass_index_wrong_type(self):
        """
        Тестирование, что форма не будет работать с неправильным типом body_mass_index.
        """
        for data in self.data_list:
            # Изменяем тип body_mass_index на некорректный
            data['body_mass_index'] = '123.32'  # Пример другого типа
            form = ClientDataForm(data)
            self.assertFalse(form.is_valid(), f'Form should not be valid, but got errors: {form.errors}')

    def test_body_mass_index_negative(self):
        """
        Тестирование валидации body_mass_index.

        Метод создает случайное значение rox, соответствующее правилам валидации,
        и заполняет им форму ClientForm. Проверяет, что форма считается валидной.

        Asserts:
            assertTrue(bool): Подтверждает, что форма прошла валидацию.
        """

        for data in self.data_list:
            data['body_mass_index'] = self.fake.pyfloat(min_value=-100.1, max_value=-0.1, right_digits=3),
            form = ClientDataForm(data)
            self.assertFalse(form.is_valid(), f'Form errors: {form.errors}')

    def test_body_mass_index_max(self):
        """
        Тестирование валидации body_mass_index.

        Метод создает случайное значение f_test_in, соответствующее правилам валидации,
        и заполняет им форму ClientForm. Проверяет, что форма считается валидной.

        Asserts:
            assertTrue(bool): Подтверждает, что форма прошла валидацию.
        """

        for data in self.data_list:
            data['body_mass_index'] = self.fake.pyfloat(min_value=100.1, max_value=200.1, right_digits=3),
            form = ClientDataForm(data)
            self.assertFalse(form.is_valid(), f'Form errors: {form.errors}')

    def test_spo2_valid(self):
        """
        Тестирование валидации spo2.

        Метод создает случайное значение spo2, соответствующее правилам валидации,
        и заполняет им форму ClientForm. Проверяет, что форма считается валидной.

        Asserts:
            assertTrue(bool): Подтверждает, что форма прошла валидацию.
        """
        for data in self.data_list:
            data['spo2'] = self.fake.random_int(min=0, max=100),
            form = ClientDataForm(data)
            self.assertFalse(form.is_valid(), f'Form errors: {form.errors}')

    def test_spo2_is_int(self):
        """
        Тестирование, что age действительно int.
        """
        for data in self.data_list:
            form = ClientDataForm(data)
            self.assertTrue(form.is_valid(), f'Form should be valid, but got errors: {form.errors}')
            self.assertIsInstance(data['spo2'], int, 'spo2 is not a int')

    def test_spo2_wrong_type(self):
        """
        Тестирование, что форма не будет работать с неправильным типом spo2.
        """
        for data in self.data_list:
            # Изменяем тип spo2 на некорректный
            data['spo2'] = '123'  # Пример другого типа
            form = ClientDataForm(data)
            self.assertFalse(form.is_valid(), f'Form should not be valid, but got errors: {form.errors}')

    def test_spo2_is_negative(self):
        """
        Тестирование валидации возраста.

        Метод создает случайный возраст, отрицательный, заполняет им форму ClientForm
        и проверяет, что форма считается невалидной.

        Asserts:
            assertFalse(bool): Подтверждает, что форма не прошла валидацию из-за
            отрицательного возраста.
        """
        for data in self.data_list:
            data['spo2'] = self.fake.random_int(min=-200, max=-1),
            form = ClientDataForm(data)
            self.assertFalse(form.is_valid(), f'Form errors: {form.errors}')

    def test_spo2_max(self):
        """
        Тестирование валидации возраста.

        Метод создает случайный возраст, отрицательный, заполняет им форму ClientForm
        и проверяет, что форма считается невалидной.

        Asserts:
            assertFalse(bool): Подтверждает, что форма не прошла валидацию из-за
            отрицательного возраста.
        """
        for data in self.data_list:
            data['spo2'] = self.fake.random_int(min=101, max=999),
            form = ClientDataForm(data)
            self.assertFalse(form.is_valid(), f'Form errors: {form.errors}')

    def test_spo2_fio_valid(self):
        """
        Тестирование валидации spo2_fio.

        Метод создает случайное значение spo2_fio, соответствующее правилам валидации,
        и заполняет им форму ClientForm. Проверяет, что форма считается валидной.

        Asserts:
            assertTrue(bool): Подтверждает, что форма прошла валидацию.
        """

        for data in self.data_list:
            data['spo2_fio'] = self.fake.random_int(min=0, max=600)
            form = ClientDataForm(data)
            self.assertTrue(form.is_valid(), f'Form errors: {form.errors}')

    def test_spo2_fio_is_float(self):
        """
        Тестирование, что spo2_fio действительно float.
        """
        for data in self.data_list:
            form = ClientDataForm(data)
            self.assertTrue(form.is_valid(), f'Form should be valid, but got errors: {form.errors}')
            self.assertIsInstance(data['spo2_fio'], float, 'age is not a float')

    def test_spo2_fio_wrong_type(self):
        """
        Тестирование, что форма не будет работать с неправильным типом spo2_fio.
        """
        for data in self.data_list:
            # Изменяем тип spo2_fio на некорректный
            data['spo2_fio'] = 'spo2fio'  # Пример другого типа
            form = ClientDataForm(data)
            self.assertFalse(form.is_valid(), f'Form should not be valid, but got errors: {form.errors}')

    def test_spo2_fio_negative(self):
        """
        Тестирование валидации spo2_fio.

        Метод создает случайное значение rox, соответствующее правилам валидации,
        и заполняет им форму ClientForm. Проверяет, что форма считается валидной.

        Asserts:
            assertTrue(bool): Подтверждает, что форма прошла валидацию.
        """

        for data in self.data_list:
            data['spo2_fio'] = self.fake.pyfloat(min_value=-100.1, max_value=-0.1, right_digits=3),
            form = ClientDataForm(data)
            self.assertFalse(form.is_valid(), f'Form errors: {form.errors}')

    def test_spo2_fio_max(self):
        """
        Тестирование валидации spo2_fio.

        Метод создает случайное значение spo2_fio, соответствующее правилам валидации,
        и заполняет им форму ClientForm. Проверяет, что форма считается валидной.

        Asserts:
            assertTrue(bool): Подтверждает, что форма прошла валидацию.
        """

        for data in self.data_list:
            data['spo2_fio'] = self.fake.pyfloat(min_value=600.1, max_value=999.1, right_digits=3),
            form = ClientDataForm(data)
            self.assertFalse(form.is_valid(), f'Form errors: {form.errors}')

    def test_f_test_ex_valid(self):
        """
        Тестирование валидации f_test_ex.

        Метод создает случайное значение f_test_ex, соответствующее правилам валидации,
        и заполняет им форму ClientForm. Проверяет, что форма считается валидной.

        Asserts:
            assertTrue(bool): Подтверждает, что форма прошла валидацию.
        """

        for data in self.data_list:
            data['f_test_ex'] = self.fake.random_int(min=0, max=200),
            form = ClientDataForm(data)
            self.assertFalse(form.is_valid(), f'Form errors: {form.errors}')

    def test_f_test_ex_is_int(self):
        """
        Тестирование, что f_test_ex действительно int.
        """
        for data in self.data_list:
            form = ClientDataForm(data)
            self.assertTrue(form.is_valid(), f'Form should be valid, but got errors: {form.errors}')
            self.assertIsInstance(data['f_test_ex'], int, 'f_test_ex is not a int')

    def test_f_test_ex_wrong_type(self):
        """
        Тестирование, что форма не будет работать с неправильным типом f_test_ex.
        """
        for data in self.data_list:
            # Изменяем тип f_test_ex на некорректный
            data['f_test_ex'] = '123.33'  # Пример другого типа
            form = ClientDataForm(data)
            self.assertFalse(form.is_valid(), f'Form should not be valid, but got errors: {form.errors}')

    def test_f_test_ex_negative(self):
        """
        Тестирование валидации f_test_ex.

        Метод создает случайное значение f_test_in, соответствующее правилам валидации,
        и заполняет им форму ClientForm. Проверяет, что форма считается валидной.

        Asserts:
            assertTrue(bool): Подтверждает, что форма прошла валидацию.
        """

        for data in self.data_list:
            data['f_test_ex'] = self.fake.random_int(min=-200, max=-1),
            form = ClientDataForm(data)
            self.assertFalse(form.is_valid(), f'Form errors: {form.errors}')

    def test_f_test_ex_max(self):
        """
        Тестирование валидации f_test_ex.

        Метод создает случайное значение f_test_in, соответствующее правилам валидации,
        и заполняет им форму ClientForm. Проверяет, что форма считается валидной.

        Asserts:
            assertTrue(bool): Подтверждает, что форма прошла валидацию.
        """

        for data in self.data_list:
            data['f_test_ex'] = self.fake.random_int(min=201, max=999),
            form = ClientDataForm(data)
            self.assertFalse(form.is_valid(), f'Form errors: {form.errors}')

    def test_f_test_in_valid(self):
        """
        Тестирование валидации f_test_in.

        Метод создает случайное значение f_test_in, соответствующее правилам валидации,
        и заполняет им форму ClientForm. Проверяет, что форма считается валидной.

        Asserts:
            assertTrue(bool): Подтверждает, что форма прошла валидацию.
        """

        for data in self.data_list:
            data['f_test_in'] = self.fake.random_int(min=0, max=200),
            form = ClientDataForm(data)
            self.assertFalse(form.is_valid(), f'Form errors: {form.errors}')

    def test_f_test_in_is_int(self):
        """
        Тестирование, что f_test_in действительно int.
        """
        for data in self.data_list:
            form = ClientDataForm(data)
            self.assertTrue(form.is_valid(), f'Form should be valid, but got errors: {form.errors}')
            self.assertIsInstance(data['f_test_in'], int, 'f_test_in is not a int')

    def test_f_test_in_wrong_type(self):
        """
        Тестирование, что форма не будет работать с неправильным типом f_test_in.
        """
        for data in self.data_list:
            # Изменяем тип f_test_in на некорректный
            data['spo2'] = '123.331123'  # Пример другого типа
            form = ClientDataForm(data)
            self.assertFalse(form.is_valid(), f'Form should not be valid, but got errors: {form.errors}')

    def test_f_test_in_negative(self):
        """
        Тестирование валидации f_test_in.

        Метод создает случайное значение f_test_in, соответствующее правилам валидации,
        и заполняет им форму ClientForm. Проверяет, что форма считается валидной.

        Asserts:
            assertTrue(bool): Подтверждает, что форма прошла валидацию.
        """

        for data in self.data_list:
            data['f_test_in'] = self.fake.random_int(min=-200, max=-1),
            form = ClientDataForm(data)
            self.assertFalse(form.is_valid(), f'Form errors: {form.errors}')

    def test_f_test_in_max(self):
        """
        Тестирование валидации f_test_in.

        Метод создает случайное значение f_test_in, соответствующее правилам валидации,
        и заполняет им форму ClientForm. Проверяет, что форма считается валидной.

        Asserts:
            assertTrue(bool): Подтверждает, что форма прошла валидацию.
        """

        for data in self.data_list:
            data['f_test_in'] = self.fake.random_int(min=201, max=999),
            form = ClientDataForm(data)
            self.assertFalse(form.is_valid(), f'Form errors: {form.errors}')

    def test_ch_d_negative(self):
        """
        Тестирование валидации f_test_in.

        Метод создает случайное значение f_test_in, соответствующее правилам валидации,
        и заполняет им форму ClientForm. Проверяет, что форма считается валидной.

        Asserts:
            assertTrue(bool): Подтверждает, что форма прошла валидацию.
        """

        for data in self.data_list:
            data['ch_d'] = self.fake.random_int(min=-100, max=-1),
            form = ClientDataForm(data)
            self.assertFalse(form.is_valid(), f'Form errors: {form.errors}')

    def test_ch_d_max(self):
        """
        Тестирование валидации ch_d.

        Метод создает случайное значение ch_d, соответствующее правилам валидации,
        и заполняет им форму ClientForm. Проверяет, что форма считается валидной.

        Asserts:
            assertTrue(bool): Подтверждает, что форма прошла валидацию.
        """

        for data in self.data_list:
            data['ch_d'] = self.fake.random_int(min=151, max=999),
            form = ClientDataForm(data)
            self.assertFalse(form.is_valid(), f'Form errors: {form.errors}')

    def test_ch_d_is_int(self):
        """
        Тестирование, что ch_d действительно int.
        """
        for data in self.data_list:
            form = ClientDataForm(data)
            self.assertTrue(form.is_valid(), f'Form should be valid, but got errors: {form.errors}')
            self.assertIsInstance(data['ch_d'], int, 'ch_d is not a int')

    def test_ch_d_wrong_type(self):
        """
        Тестирование, что форма не будет работать с неправильным типом spo2.
        """
        for data in self.data_list:
            # Изменяем тип ch_d на некорректный
            data['ch_d'] = '123.23123'  # Пример другого типа
            form = ClientDataForm(data)
            self.assertFalse(form.is_valid(), f'Form should not be valid, but got errors: {form.errors}')

    def test_rox_is_float(self):
        """
        Тестирование, что age действительно float.
        """
        for data in self.data_list:
            form = ClientDataForm(data)
            self.assertTrue(form.is_valid(), f'Form should be valid, but got errors: {form.errors}')
            self.assertIsInstance(data['body_mass_index'], float, 'rox is not a float')

    def test_rox_wrong_type(self):
        """
        Тестирование, что форма не будет работать с неправильным типом rox.
        """
        for data in self.data_list:
            # Изменяем тип rox на некорректный
            data['body_mass_index'] = '123'  # Пример другого типа
            form = ClientDataForm(data)
            self.assertFalse(form.is_valid(), f'Form should not be valid, but got errors: {form.errors}')

    def test_rox_negative(self):
        """
        Тестирование валидации rox.

        Метод создает случайное значение rox, соответствующее правилам валидации,
        и заполняет им форму ClientForm. Проверяет, что форма считается валидной.

        Asserts:
            assertTrue(bool): Подтверждает, что форма прошла валидацию.
        """

        for data in self.data_list:
            data['rox'] = self.fake.pyfloat(min_value=-100.1, max_value=-0.1, right_digits=3),
            form = ClientDataForm(data)
            self.assertFalse(form.is_valid(), f'Form errors: {form.errors}')

    def test_rox_max(self):
        """
        Тестирование валидации f_test_in.

        Метод создает случайное значение f_test_in, соответствующее правилам валидации,
        и заполняет им форму ClientForm. Проверяет, что форма считается валидной.

        Asserts:
            assertTrue(bool): Подтверждает, что форма прошла валидацию.
        """

        for data in self.data_list:
            data['rox'] = self.fake.pyfloat(min_value=50.1, max_value=100.1, right_digits=3),
            form = ClientDataForm(data)
            self.assertFalse(form.is_valid(), f'Form errors: {form.errors}')

    def test_l_109_is_float(self):
        """
        Тестирование, что age действительно float.
        """
        for data in self.data_list:
            form = ClientDataForm(data)
            self.assertTrue(form.is_valid(), f'Form should be valid, but got errors: {form.errors}')
            self.assertIsInstance(data['l_109'], float, 'l_109 is not a float')

    def test_l_109_wrong_type(self):
        """
        Тестирование, что форма не будет работать с неправильным типом rox.
        """
        for data in self.data_list:
            # Изменяем тип rox на некорректный
            data['l_109'] = '_string_'  # Пример другого типа
            form = ClientDataForm(data)
            self.assertFalse(form.is_valid(), f'Form should not be valid, but got errors: {form.errors}')

    def test_l_109_negative(self):
        """
        Тестирование валидации rox.

        Метод создает случайное значение rox, соответствующее правилам валидации,
        и заполняет им форму ClientForm. Проверяет, что форма считается валидной.

        Asserts:
            assertTrue(bool): Подтверждает, что форма прошла валидацию.
        """

        for data in self.data_list:
            data['l_109'] = self.fake.pyfloat(min_value=-100.1, max_value=-0.1, right_digits=3),
            form = ClientDataForm(data)
            self.assertFalse(form.is_valid(), f'Form errors: {form.errors}')

    def test_l_109_max(self):
        """
        Тестирование валидации l_109.

        Метод создает случайное значение l_109, соответствующее правилам валидации,
        и заполняет им форму ClientForm. Проверяет, что форма считается валидной.

        Asserts:
            assertTrue(bool): Подтверждает, что форма прошла валидацию.
        """

        for data in self.data_list:
            data['l_109'] = self.fake.pyfloat(min_value=50.1, max_value=100.1, right_digits=3),
            form = ClientDataForm(data)
            self.assertFalse(form.is_valid(), f'Form errors: {form.errors}')

    def test_lf_negative(self):
        """
        Тестирование валидации lf.

        Метод создает случайное значение lf, соответствующее правилам валидации,
        и заполняет им форму ClientForm. Проверяет, что форма считается валидной.

        Asserts:
            assertTrue(bool): Подтверждает, что форма прошла валидацию.
        """

        for data in self.data_list:
            data['lf'] = self.fake.random_int(min=-100, max=-1),
            form = ClientDataForm(data)
            self.assertFalse(form.is_valid(), f'Form errors: {form.errors}')

    def test_lf_max(self):
        """
        Тестирование валидации lf.

        Метод создает случайное значение lf, соответствующее правилам валидации,
        и заполняет им форму ClientForm. Проверяет, что форма считается валидной.

        Asserts:
            assertTrue(bool): Подтверждает, что форма прошла валидацию.
        """

        for data in self.data_list:
            data['lf'] = self.fake.random_int(min=51, max=999),
            form = ClientDataForm(data)
            self.assertFalse(form.is_valid(), f'Form errors: {form.errors}')

    def test_lf_is_float(self):
        """
        Тестирование, что lf действительно float.
        """
        for data in self.data_list:
            form = ClientDataForm(data)
            self.assertTrue(form.is_valid(), f'Form should be valid, but got errors: {form.errors}')
            self.assertIsInstance(data['lf'], float, 'lf is not a float')

    def test_lf_wrong_type(self):
        """
        Тестирование, что форма не будет работать с неправильным типом lf.
        """
        for data in self.data_list:
            # Изменяем тип lf на некорректный
            data['lf'] = '_str'  # Пример другого типа
            form = ClientDataForm(data)
            self.assertFalse(form.is_valid(), f'Form should not be valid, but got errors: {form.errors}')

    def test_comorb_ccc_is_bool(self):
        """
        Тестирование, что comorb_ccc действительно строка.
        """
        for data in self.data_list:
            form = ClientDataForm(data)
            self.assertTrue(form.is_valid(), f'Form should be valid, but got errors: {form.errors}')
            self.assertIsInstance(data['comorb_ccc'], bool, 'comorb_ccc is not a bool')

    def test_comorb_all_is_bool(self):
        """
        Тестирование, что comorb_all действительно строка.
        """
        for data in self.data_list:
            form = ClientDataForm(data)
            self.assertTrue(form.is_valid(), f'Form should be valid, but got errors: {form.errors}')
            self.assertIsInstance(data['comorb_all'], bool, 'comorb_all is not a bool')

    def test_comorb_bl_is_bool(self):
        """
        Тестирование, что comorb_bl действительно строка.
        """
        for data in self.data_list:
            form = ClientDataForm(data)
            self.assertTrue(form.is_valid(), f'Form should be valid, but got errors: {form.errors}')
            self.assertIsInstance(data['comorb_bl'], bool, 'comorb_bl is not a bool')

    def test_cd_ozhir_is_bool(self):
        """
        Тестирование, что cd_ozhir действительно строка.
        """
        for data in self.data_list:
            form = ClientDataForm(data)
            self.assertTrue(form.is_valid(), f'Form should be valid, but got errors: {form.errors}')
            self.assertIsInstance(data['cd_ozhir'], bool, 'cd_ozhir is not a bool')

    def test_dayshome_negative(self):
        """
        Тестирование валидации dayshome.

        Метод создает случайное значение dayshome, соответствующее правилам валидации,
        и заполняет им форму ClientForm. Проверяет, что форма считается валидной.

        Asserts:
            assertTrue(bool): Подтверждает, что форма прошла валидацию.
        """

        for data in self.data_list:
            data['dayshome'] = self.fake.random_int(min=-20, max=-1),
            form = ClientDataForm(data)
            self.assertFalse(form.is_valid(), f'Form errors: {form.errors}')

    def test_dayshome_max(self):
        """
        Тестирование валидации dayshome.

        Метод создает случайное значение dayshome, соответствующее правилам валидации,
        и заполняет им форму ClientForm. Проверяет, что форма считается валидной.

        Asserts:
            assertTrue(bool): Подтверждает, что форма прошла валидацию.
        """

        for data in self.data_list:
            data['dayshome'] = self.fake.random_int(min=51, max=999),
            form = ClientDataForm(data)
            self.assertFalse(form.is_valid(), f'Form errors: {form.errors}')

    def test_dayshome_is_int(self):
        """
        Тестирование, что dayshome действительно int.
        """
        for data in self.data_list:
            form = ClientDataForm(data)
            self.assertTrue(form.is_valid(), f'Form should be valid, but got errors: {form.errors}')
            self.assertIsInstance(data['dayshome'], int, 'dayshome is not a int')

    def test_dayshome_wrong_type(self):
        """
        Тестирование, что форма не будет работать с неправильным типом spo2.
        """
        for data in self.data_list:
            # Изменяем тип dayshome на некорректный
            data['dayshome'] = 'days'  # Пример другого типа
            form = ClientDataForm(data)
            self.assertFalse(form.is_valid(), f'Form should not be valid, but got errors: {form.errors}')


class ClientModelTest(TestCase):

    @classmethod
    def setUpTestData(cls, num_objects=10):
        """
        Создает num_objects объектов Client с использованием случайных данных от Faker.
        """
        fake = Faker('ru_RU')

        # Создаем num_objects объектов Client с использованием случайных данных от Faker
        for _ in range(num_objects):
            PersonalInfo.objects.create(
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                patronymic=fake.middle_name(),
                id=fake.uuid4(),
                gender=fake.random_element(elements=[True, False]),
                # другие поля модели
            )

    def test_none_values(self):
        """
        Тест проверяет, что поля в объекте Client не являются None.
        """
        clients = PersonalInfo.objects.all()
        for client in clients:
            # Проверяем поле на NONE
            self.assertIsNotNone(client.first_name)
            self.assertIsNotNone(client.last_name)
            self.assertIsNotNone(client.patronymic)
            self.assertIsNotNone(client.id)

        print(f'test_1_none_values: {len(clients)}')

    def test_str_method(self):
        """
        Тест использует метод __str__ для вывода строкового представления каждого объекта Client.
        """
        clients = PersonalInfo.objects.all()

        # Используем метод __str__ и выводим строку для каждого объекта
        for client in clients:
            print(str(client))

    def test_token_uniqueness(self):
        """
        Тест для проверки уникальности токенов.
        """
        clients = PersonalInfo.objects.all()
        tokens = set(client.id for client in clients)
        print(f'test_token_uniqueness: {len(tokens)}')
        self.assertEqual(len(clients), len(tokens))

    def test_get_gender_display(self):
        """
        Тест для проверки вывода пола(отображения).
        """
        client = PersonalInfo.objects.first()
        self.assertEqual(client.get_gender_display(), 'Мужской' if client.gender else 'Женский')


class ClientListViewTests(TestCase):
    def setUp(self):
        # Создаем пользователя и логинимся
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')

        # Инициализируем Faker
        fake = Faker('ru_RU')

        # Создаем PersonalInfo для теста с использованием Faker
        self.personal_info = PersonalInfo.objects.create(
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            patronymic=fake.first_name(),
            # Добавьте другие необходимые поля
        )

        # Создаем ClientData для теста с использованием Faker
        self.client_data = ClientData.objects.create(
            personal_info=self.personal_info,
            # Добавьте другие необходимые поля
        )

        # URL для просмотра списка клиентов
        self.url = reverse('client_list')

    def test_view_url_exists_at_desired_location(self):
        # Проверяем, доступен ли URL для списка клиентов
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        # Проверяем, что представление использует правильный шаблон
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'client_list.html')

    def test_view_returns_clients_data(self):
        # Проверяем, что представление возвращает данные о клиентах
        response = self.client.get(self.url)
        self.assertContains(response, self.client_data.personal_info.first_name)


class ClientDetailViewTests(TestCase):
    '''
    Test the client detail(view)
    тестим вьюху client-detail
    '''

    def setUp(self):
        # Создаем пользователя и логинимся
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')

        # Инициализируем Faker
        self.faker = Faker('ru_RU')

        # Создаем PersonalInfo для теста с использованием Faker
        self.personal_info = PersonalInfo.objects.create(
            first_name=self.faker.first_name(),
            last_name=self.faker.last_name(),
            patronymic=self.faker.first_name(),
            # Добавьте другие необходимые поля
        )

        # Создаем ClientData для теста с использованием Faker
        self.client_data = ClientData.objects.create(
            personal_info=self.personal_info,
            # Добавьте другие необходимые поля
        )

        # URL для просмотра деталей клиента
        self.url = reverse('client_detail', args=[str(self.personal_info.id)])

    def test_view_url_exists_at_desired_location(self):
        # Проверяем, доступен ли URL для деталей клиента
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        # Проверяем, что представление использует правильный шаблон
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'client_detail.html')

    def test_view_returns_correct_data(self):
        # Проверяем, что представление возвращает правильные данные о клиенте
        response = self.client.get(self.url)
        self.assertContains(response, self.client_data.personal_info.first_name)
        # Добавьте другие проверки на необходимые поля

    def test_view_can_edit_client_data(self):
        # Проверяем, что представление может редактировать данные о клиенте
        new_result = 3  # Новое значение для результата
        data = {'action': 'edit_client', 'result': new_result}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 302)  # Ожидаем перенаправление после успешного редактирования
        self.client_data.refresh_from_db()  # Обновляем данные из базы
        self.assertEqual(self.client_data.result, new_result)
