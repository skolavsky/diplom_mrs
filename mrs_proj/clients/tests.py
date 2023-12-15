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
            'body_mass_index': self.fake.pyfloat(min_value=0, max_value=100, right_digits=3),
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


    def test_age_negative(self):
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
        Тестирование валидации f_test_in.

        Метод создает случайное значение f_test_in, соответствующее правилам валидации,
        и заполняет им форму ClientForm. Проверяет, что форма считается валидной.

        Asserts:
            assertTrue(bool): Подтверждает, что форма прошла валидацию.
        """

        for data in self.data_list:
            data['ch_d'] = self.fake.random_int(min=151, max=999),
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
