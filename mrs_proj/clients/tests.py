from django.test import TestCase
import os
from faker import Faker
from clients.models import Client
from django.forms import ValidationError
from django.forms import ModelForm
import secrets
from clients.forms import ClientForm

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "your_project.settings")

class ClientFormTest(TestCase):
    def setUp(self):
        self.fake = Faker()

    def test_valid_form(self):
        data = {
            'first_name': self.fake.first_name(),
            'last_name': self.fake.last_name(),
            'age': self.fake.random_int(min=18, max=99),
            'admission_date': self.fake.date_this_decade(),
            'gender': '1'
            # Добавьте остальные поля модели
        }

        form = ClientForm(data)
        self.assertTrue(form.is_valid(), f'Form errors: {form.errors}')
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        data = {
            'first_name': self.fake.first_name(),
            'last_name': self.fake.last_name(),
            # Недостаточно данных
        }

        form = ClientForm(data)
        self.assertFalse(form.is_valid())


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
                patronymic=fake.last_name(),
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