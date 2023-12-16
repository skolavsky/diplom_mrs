from django.test import TestCase
from clients.models import Client
from clients.forms import ClientForm
from faker import Faker
from datetime import date
import os
import secrets
import string

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "your_project.settings")
START_YEAR = 2023  # для admission_date
FIO_FIELDS_MAX_LENGTH = 100


class ClientFormTest(TestCase):
    """
        Класс для тестирования валидности формы ClientForm.

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
            'age': self.fake.random_int(min=0, max=120),
            'admission_date': self.fake.date_between_dates(date(START_YEAR, 1, 1), date.today()),
            'gender': secrets.choice(['0', '1']),
            'body_mass_index': self.fake.pyfloat(min_value=0, max_value=100.0, right_digits=3),
            'spo2': self.fake.random_int(min=0, max=100),
            'spo2_fio': self.fake.pyfloat(min_value=0, max_value=600.0, right_digits=3),
            'ch_d': self.fake.random_int(min=0, max=150),
            'f_test_ex': self.fake.random_int(min=0, max=200),
            'f_test_in': self.fake.random_int(min=0, max=200),
            'rox': self.fake.pyfloat(min_value=0, max_value=50.0, right_digits=3),
            # Можно добавить и другие поля модели
        }
        default_data.update(kwargs)
        return default_data

    def generate_invalid_string(self, spec_numbers: int = 5):
        """
        :type spec_numbers: int
        """
        return ''.join(secrets.choice(string.punctuation + string.digits) for _ in range(spec_numbers))

    def test_valid_form(self):
        """Тест валидности формы с корректными данными."""
        for data in self.data_list:
            form = ClientForm(data)
            self.assertTrue(form.is_valid(), f'Form errors: {form.errors}')

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
            data['first_name'] = str('a' * (FIO_FIELDS_MAX_LENGTH + 1))
            form = ClientForm(data)
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
            data['last_name'] = str('a' * (FIO_FIELDS_MAX_LENGTH + 1))
            form = ClientForm(data)
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
            data['patronymic'] = str('a' * (FIO_FIELDS_MAX_LENGTH + 1))
            form = ClientForm(data)
            self.assertFalse(form.is_valid(), f'Form errors: {form.errors}')

    def test_invalid_first_name(self):
        for data in self.data_list:
            data['first_name'] = data['first_name'] + self.generate_invalid_string()
            form = ClientForm(data)
            self.assertFalse(form.is_valid(), f'Form errors: {form.errors}')

    def test_invalid_last_name(self):
        for data in self.data_list:
            data['last_name'] += self.generate_invalid_string()
            form = ClientForm(data)
            self.assertFalse(form.is_valid(), f'Form errors: {form.errors}')

    def test_invalid_patronymic(self):
        for data in self.data_list:
            data['patronymic'] = data['patronymic'] + self.generate_invalid_string()
            form = ClientForm(data)
            self.assertFalse(form.is_valid(), f'Form errors: {form.errors}')

    def test_first_name_is_string(self):
        """
        Тестирование, что first_name действительно строка.
        """
        for data in self.data_list:
            form = ClientForm(data)
            self.assertTrue(form.is_valid(), f'Form should be valid, but got errors: {form.errors}')
            self.assertIsInstance(data['first_name'], str, 'first_name is not a string')

    def test_last_name_is_string(self):
        """
        Тестирование, что last_name действительно строка.
        """
        for data in self.data_list:
            form = ClientForm(data)
            self.assertTrue(form.is_valid(), f'Form should be valid, but got errors: {form.errors}')
            self.assertIsInstance(data['last_name'], str, 'last_name is not a string')

    def test_patronymic_is_string(self):
        """
        Тестирование, что patronymic действительно строка.
        """
        for data in self.data_list:
            form = ClientForm(data)
            self.assertTrue(form.is_valid(), f'Form should be valid, but got errors: {form.errors}')
            self.assertIsInstance(data['patronymic'], str, 'patronymic is not a string')

    def test_first_name_wrong_type(self):
        """
        Тестирование, что форма не будет работать с неправильным типом first_name.
        """
        for data in self.data_list:
            # Изменяем тип first_name на некорректный
            data['first_name'] = 123  # Пример другого типа
            form = ClientForm(data)
            self.assertFalse(form.is_valid(), f'Form should not be valid, but got errors: {form.errors}')

    def test_last_name_wrong_type(self):
        """
        Тестирование, что форма не будет работать с неправильным типом first_name.
        """
        for data in self.data_list:
            # Изменяем тип last_name на некорректный
            data['last_name'] = 123  # Пример другого типа
            form = ClientForm(data)
            self.assertFalse(form.is_valid(), f'Form should not be valid, but got errors: {form.errors}')

    def test_patronymic_wrong_type(self):
        """
        Тестирование, что форма не будет работать с неправильным типом patronymic.
        """
        for data in self.data_list:
            # Изменяем тип patronymic на некорректный
            data['patronymic'] = 123  # Пример другого типа
            form = ClientForm(data)
            self.assertFalse(form.is_valid(), f'Form should not be valid, but got errors: {form.errors}')


    def test_age_is_negative(self):
        """
        Тестирование валидации возраста.

        Метод создает случайный возраст, отрицательный, заполняет им форму ClientForm
        и проверяет, что форма считается невалидной.

        Asserts:
            assertFalse(bool): Подтверждает, что форма не прошла валидацию из-за
            отрицательного возраста.
        """
        for data in self.data_list:
            data['age'] *= -1
            form = ClientForm(data)
            self.assertFalse(form.is_valid(), f'Form errors: {form.errors}')

    def test_age_max(self):
        """
        Тестирование валидации возраста.

        Метод создает случайный возраст, отрицательный, заполняет им форму ClientForm
        и проверяет, что форма считается невалидной.

        Asserts:
            assertFalse(bool): Подтверждает, что форма не прошла валидацию из-за
            отрицательного возраста.
        """
        for data in self.data_list:
            data['age'] = self.fake.random_int(min=121, max=999),
            form = ClientForm(data)
            self.assertFalse(form.is_valid(), f'Form errors: {form.errors}')

    def test_age_is_int(self):
        """
        Тестирование, что age действительно int.
        """
        for data in self.data_list:
            form = ClientForm(data)
            self.assertTrue(form.is_valid(), f'Form should be valid, but got errors: {form.errors}')
            self.assertIsInstance(data['age'], int, 'age is not a int')

    def test_age_wrong_type(self):
        """
        Тестирование, что форма не будет работать с неправильным типом age.
        """
        for data in self.data_list:
            # Изменяем тип age на некорректный
            data['age'] = '123'  # Пример другого типа
            form = ClientForm(data)
            self.assertFalse(form.is_valid(), f'Form should not be valid, but got errors: {form.errors}')

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
            form = ClientForm(data)
            self.assertFalse(form.is_valid(), f'Form errors: {form.errors}')

    def test_body_mass_index_is_float(self):
        """
        Тестирование, что age действительно float.
        """
        for data in self.data_list:
            form = ClientForm(data)
            self.assertTrue(form.is_valid(), f'Form should be valid, but got errors: {form.errors}')
            self.assertIsInstance(data['body_mass_index'], float, 'age is not a float')

    def test_body_mass_index_wrong_type(self):
        """
        Тестирование, что форма не будет работать с неправильным типом body_mass_index.
        """
        for data in self.data_list:
            # Изменяем тип body_mass_index на некорректный
            data['body_mass_index'] = '123.32'  # Пример другого типа
            form = ClientForm(data)
            self.assertFalse(form.is_valid(), f'Form should not be valid, but got errors: {form.errors}')

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
            form = ClientForm(data)
            self.assertFalse(form.is_valid(), f'Form errors: {form.errors}')

    def test_spo2_is_int(self):
        """
        Тестирование, что age действительно int.
        """
        for data in self.data_list:
            form = ClientForm(data)
            self.assertTrue(form.is_valid(), f'Form should be valid, but got errors: {form.errors}')
            self.assertIsInstance(data['spo2'], int, 'spo2 is not a int')

    def test_spo2_wrong_type(self):
        """
        Тестирование, что форма не будет работать с неправильным типом spo2.
        """
        for data in self.data_list:
            # Изменяем тип spo2 на некорректный
            data['spo2'] = '123'  # Пример другого типа
            form = ClientForm(data)
            self.assertFalse(form.is_valid(), f'Form should not be valid, but got errors: {form.errors}')

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
            form = ClientForm(data)
            self.assertTrue(form.is_valid(), f'Form errors: {form.errors}')

    def test_spo2_fio_is_float(self):
        """
        Тестирование, что spo2_fio действительно float.
        """
        for data in self.data_list:
            form = ClientForm(data)
            self.assertTrue(form.is_valid(), f'Form should be valid, but got errors: {form.errors}')
            self.assertIsInstance(data['spo2_fio'], float, 'age is not a float')

    def test_spo2_fio_wrong_type(self):
        """
        Тестирование, что форма не будет работать с неправильным типом spo2_fio.
        """
        for data in self.data_list:
            # Изменяем тип spo2_fio на некорректный
            data['body_mass_index'] = '123'  # Пример другого типа
            form = ClientForm(data)
            self.assertFalse(form.is_valid(), f'Form should not be valid, but got errors: {form.errors}')

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
            form = ClientForm(data)
            self.assertFalse(form.is_valid(), f'Form errors: {form.errors}')

    def test_f_test_ex_is_int(self):
        """
        Тестирование, что f_test_ex действительно int.
        """
        for data in self.data_list:
            form = ClientForm(data)
            self.assertTrue(form.is_valid(), f'Form should be valid, but got errors: {form.errors}')
            self.assertIsInstance(data['f_test_ex'], int, 'f_test_ex is not a int')

    def test_f_test_ex_wrong_type(self):
        """
        Тестирование, что форма не будет работать с неправильным типом f_test_ex.
        """
        for data in self.data_list:
            # Изменяем тип f_test_ex на некорректный
            data['f_test_ex'] = '123.33'  # Пример другого типа
            form = ClientForm(data)
            self.assertFalse(form.is_valid(), f'Form should not be valid, but got errors: {form.errors}')

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
            form = ClientForm(data)
            self.assertFalse(form.is_valid(), f'Form errors: {form.errors}')

    def test_f_test_in_is_int(self):
        """
        Тестирование, что f_test_in действительно int.
        """
        for data in self.data_list:
            form = ClientForm(data)
            self.assertTrue(form.is_valid(), f'Form should be valid, but got errors: {form.errors}')
            self.assertIsInstance(data['f_test_in'], int, 'f_test_in is not a int')

    def test_f_test_in_wrong_type(self):
        """
        Тестирование, что форма не будет работать с неправильным типом f_test_in.
        """
        for data in self.data_list:
            # Изменяем тип f_test_in на некорректный
            data['spo2'] = '123.331123'  # Пример другого типа
            form = ClientForm(data)
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
            form = ClientForm(data)
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
            form = ClientForm(data)
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
            form = ClientForm(data)
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
            form = ClientForm(data)
            self.assertFalse(form.is_valid(), f'Form errors: {form.errors}')

    def test_ch_d_is_int(self):
        """
        Тестирование, что ch_d действительно int.
        """
        for data in self.data_list:
            form = ClientForm(data)
            self.assertTrue(form.is_valid(), f'Form should be valid, but got errors: {form.errors}')
            self.assertIsInstance(data['ch_d'], int, 'ch_d is not a int')

    def test_ch_d_wrong_type(self):
        """
        Тестирование, что форма не будет работать с неправильным типом spo2.
        """
        for data in self.data_list:
            # Изменяем тип ch_d на некорректный
            data['ch_d'] = '123.23123'  # Пример другого типа
            form = ClientForm(data)
            self.assertFalse(form.is_valid(), f'Form should not be valid, but got errors: {form.errors}')

    def test_rox_is_float(self):
        """
        Тестирование, что age действительно float.
        """
        for data in self.data_list:
            form = ClientForm(data)
            self.assertTrue(form.is_valid(), f'Form should be valid, but got errors: {form.errors}')
            self.assertIsInstance(data['body_mass_index'], float, 'rox is not a float')

    def test_rox_wrong_type(self):
        """
        Тестирование, что форма не будет работать с неправильным типом rox.
        """
        for data in self.data_list:
            # Изменяем тип rox на некорректный
            data['body_mass_index'] = '123'  # Пример другого типа
            form = ClientForm(data)
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
            form = ClientForm(data)
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
            form = ClientForm(data)
            self.assertFalse(form.is_valid(), f'Form errors: {form.errors}')


class ClientModelTest(TestCase):

    @classmethod
    def setUpTestData(cls, num_objects=10):
        """
        Создает num_objects объектов Client с использованием случайных данных от Faker.
        """
        fake = Faker('ru_RU')

        # Создаем num_objects объектов Client с использованием случайных данных от Faker
        for _ in range(num_objects):
            Client.objects.create(
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                patronymic=fake.middle_name(),
                age=fake.random_int(min=18, max=100),
                admission_date=fake.date_between(start_date='-30d', end_date='today'),
                id_token=fake.uuid4(),
                # другие поля модели
            )

    def test_none_values(self):
        """
        Тест проверяет, что поля в объекте Client не являются None.
        """
        clients = Client.objects.all()
        for client in clients:
            # Проверяем поле на NONE
            self.assertIsNotNone(client.first_name)
            self.assertIsNotNone(client.last_name)
            self.assertIsNotNone(client.patronymic)
            self.assertIsNotNone(client.age)
            self.assertIsNotNone(client.admission_date)
            self.assertIsNotNone(client.id_token)

        print(f'test_1_none_values: {len(clients)}')

    def test_str_method(self):
        """
        Тест использует метод __str__ для вывода строкового представления каждого объекта Client.
        """
        clients = Client.objects.all()

        # Используем метод __str__ и выводим строку для каждого объекта
        for client in clients:
            print(str(client))

    def test_token_uniqueness(self):
        """
        Тест для проверки уникальности токенов.
        """
        clients = Client.objects.all()
        tokens = set(client.id_token for client in clients)
        print(f'test_token_uniqueness: {len(tokens)}')
        self.assertEqual(len(clients), len(tokens))

    def test_get_gender_display(self):
        """
        Тест для проверки вывода пола(отображения).
        """
        client = Client.objects.first()
        self.assertEqual(client.get_gender_display(), 'Мужской' if client.gender else 'Женский')
